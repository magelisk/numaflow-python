from collections.abc import AsyncIterable
import asyncio
from google.protobuf import empty_pb2 as _empty_pb2
from collections import deque
from datetime import datetime, timedelta

from pynumaflow.mapstreamer import Datum, Message
from pynumaflow.mapstreamer._dtypes import MapStreamCallable
from pynumaflow.proto.mapstreamer import mapstream_pb2_grpc, mapstream_pb2
from pynumaflow.types import NumaflowServicerContext
from pynumaflow._constants import _LOGGER

async def datum_generator(
    request_iterator: AsyncIterable[mapstream_pb2.MapStreamRequest],
) -> AsyncIterable[Datum]:
    # i = 0
    async for d in request_iterator:
        # print(f"Loop {i} -- {d=}")
        # i += 1
        datum = Datum(
            keys=list(d.keys),
            value=d.value,
            event_time=d.event_time.ToDatetime(),
            watermark=d.watermark.ToDatetime(),
            headers=dict(d.headers),
        )
        yield datum


class AsyncMapStreamServicerBase(mapstream_pb2_grpc.MapStreamServicer):
    """
    This class is used to create a new grpc Map Stream Servicer instance.
    It implements the SyncMapServicer interface from the proto
    mapstream_pb2_grpc.py file.
    Provides the functionality for the required rpc methods.
    """

    def __init__(
        self,
        handler: MapStreamCallable,
    ):
        self._map_stream_handler: MapStreamCallable = handler


    async def MapStreamFn(
        self,
        request: mapstream_pb2.MapStreamRequest,
        context: NumaflowServicerContext,
    ) -> AsyncIterable[mapstream_pb2.MapStreamResponse]:
        # TODO: Ditch this
        raise NotImplementedError("Gonna get rid of this!")


    async def IsReady(
        self, request: _empty_pb2.Empty, context: NumaflowServicerContext
    ) -> mapstream_pb2.ReadyResponse:
        """
        IsReady is the heartbeat endpoint for gRPC.
        The pascal case function name comes from the proto mapstream_pb2_grpc.py file.
        """
        return mapstream_pb2.ReadyResponse(ready=True)


    async def MapStreamBatchFn(
        self,
        request_iterator: AsyncIterable[mapstream_pb2.MapStreamRequest],
        context: NumaflowServicerContext,
    ) -> AsyncIterable[mapstream_pb2.MapStreamResponse]:
        """
        Flatmap one
        """
        # _LOGGER.info("MDW: Flatmap handler")
        print("MDW: Stream Handler")
        datum_iterator = datum_generator(request_iterator=request_iterator)

        try:
            async for msg in self.present_data(datum_iterator, context):
                yield msg
        #     async for msg in datum_iterator:
        #         async for to_ret in self._process_one_flatmap(msg):
        #             yield to_ret
        except Exception as err:
            _LOGGER.critical("UDFError, re-raising the error", exc_info=True)
            raise err
        
class StreamFlatMap(AsyncMapStreamServicerBase):
    async def present_data(
        self,
        datum_iterator: AsyncIterable[Datum],
        context: NumaflowServicerContext,
    ) -> AsyncIterable[Message]:
        print("MDW: flatmap:present_data")
        try:
            async for msg in datum_iterator:
                async for to_ret in self._process_one_flatmap(msg):
                    yield to_ret
        except Exception as err:
            _LOGGER.critical("UDFError, re-raising the error", exc_info=True)
            raise err
        
    async def _process_one_flatmap(self, msg: Datum):
        # msg_id = msg.msg_id

        try:
            results = []
            # async for result in self._map_stream_handler.handler_stream(msg):
            async for result in self._map_stream_handler.handler(msg.keys, msg):
                results.append(result)
            
            # We intentially store results and send at completion of callback to ensure no partial returns
            for result in results:
                yield mapstream_pb2.MapStreamResponse(
                    result=mapstream_pb2.MapStreamResponse.Result(
                        keys=result.keys, value=result.value, tags=result.tags  # MDW: 
                    )
                )
            
            # TODO: Send completion message for given msg_id
        except Exception as err:
            err_msg = "UDFError, re-raising the error: %r" % err
            _LOGGER.critical(err_msg, exc_info=True)
            raise err
        

class StreamBatchMap(AsyncMapStreamServicerBase):
    def __init__(self, 
                 handler: MapStreamCallable,
                 batch_size:int=10):
        super().__init__(handler)
        
        self._batch_size = batch_size

    async def present_data(
        self,
        datum_iterator: AsyncIterable[Datum],
        context: NumaflowServicerContext,
        batch_size: int = 10,
        timeout: int = 5
    ) -> AsyncIterable[Message]:
        buffer: deque[Datum] = deque()
        start_time = datetime.now()

        keep_going = True
        # print("MDW: batch:present_data GPT")
        async def fetch_next_datum():
            nonlocal keep_going
            try:
                return await asyncio.wait_for(datum_iterator.__anext__(), timeout)
            except asyncio.TimeoutError:
                return None
            except StopAsyncIteration:
                keep_going = False
                return None
            
        while keep_going:
            datum = await fetch_next_datum()
            if datum:
                buffer.append(datum)
                if len(buffer) >= batch_size:
                    # print("MDW: Process because full")
                    async for message in self._process_stream_map(buffer):
                        yield message
                    buffer.clear()
                    start_time = datetime.now()
            else:
                if buffer:
                    # print("MDW: Process because timeout but no data")
                    async for message in self._process_stream_map(buffer):
                        yield message
                    buffer.clear()
                    start_time = datetime.now()

            # Check if the timeout has been exceeded
            if (datetime.now() - start_time).total_seconds() >= timeout:
                # print("MDW: What happens here?")
                if buffer:
                    async for message in self._process_stream_map(buffer):
                        yield message
                    buffer.clear()
                    start_time = datetime.now()

            # if datum is None and not buffer:
            #     break

    async def _process_stream_map(self, msgs: list[Datum]):

        try:
            results = []
            # async for result in self._map_stream_handler.handler_stream(msg):
            async for result in self._map_stream_handler.handler(msgs):
                results.append(result)
            
            # We intentially store results and send at completion of callback to ensure no partial returns
            # TOOD: Move this to base class?
            for result in results:
                yield mapstream_pb2.MapStreamResponse(
                    result=mapstream_pb2.MapStreamResponse.Result(
                        keys=result.keys, value=result.value, tags=result.tags  # MDW: 
                    )
                )
            
            # TODO: Send completion message for given msg_id
        except Exception as err:
            err_msg = "UDFError, re-raising the error: %r" % err
            _LOGGER.critical(err_msg, exc_info=True)
            raise err