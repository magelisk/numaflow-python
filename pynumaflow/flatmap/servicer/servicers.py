from collections.abc import AsyncIterable
import asyncio
from google.protobuf import empty_pb2 as _empty_pb2
from collections import deque
from datetime import datetime, timedelta
import time

from pynumaflow.mapstreamer import Datum, Message, DROP
from pynumaflow.mapstreamer._dtypes import MapStreamCallable
from pynumaflow.proto.flatmap import flatmap_pb2_grpc, flatmap_pb2
from pynumaflow.types import NumaflowServicerContext
from pynumaflow._constants import _LOGGER

async def datum_generator(
    request_iterator: AsyncIterable[flatmap_pb2.MapRequest],
) -> AsyncIterable[Datum]:
    async for d in request_iterator:
        datum = Datum(
            uuid=d.uuid,
            keys=list(d.keys),
            value=d.value,
            event_time=d.event_time.ToDatetime(),
            watermark=d.watermark.ToDatetime(),
            headers=dict(d.headers),
        )
        yield datum


class FlatmapServicerBase(flatmap_pb2_grpc.FlatmapServicer):
    """
    This class is used to create a new grpc Map Stream Servicer instance.
    It implements the SyncMapServicer interface from the proto
    flatmap_pb2_grpc.py file.
    Provides the functionality for the required rpc methods.
    """

    def __init__(
        self,
        handler: MapStreamCallable,
    ):
        self._map_stream_handler: MapStreamCallable = handler


    async def IsReady(
        self, request: _empty_pb2.Empty, context: NumaflowServicerContext
    ) -> flatmap_pb2.ReadyResponse:
        """
        IsReady is the heartbeat endpoint for gRPC.
        The pascal case function name comes from the proto mapstream_pb2_grpc.py file.
        """
        return flatmap_pb2.ReadyResponse(ready=True)


    async def MapFn(
        self,
        request_iterator: AsyncIterable[flatmap_pb2.MapRequest],
        context: NumaflowServicerContext,
    ) -> AsyncIterable[flatmap_pb2.MapResponse]:
        """
        Flatmap one
        """
        _LOGGER.info("MDW: Flatmap handler")
        print("MDW: Flatmap MapFn")
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
        
class FlatMapServer(FlatmapServicerBase):
    async def present_data(
        self,
        datum_iterator: AsyncIterable[Datum],
        context: NumaflowServicerContext,
    ) -> AsyncIterable[Message]:
        print("MDW: flatmap:present_data")
        try:
            print("MDW flatmap:present_data - Waiting for message")
            async for msg in datum_iterator:
                print(f"MDW flatmap:present_data -got {msg=}")
                async for to_ret in self._process_one_flatmap(msg):
                    yield to_ret
        except Exception as err:
            _LOGGER.critical("UDFError, re-raising the error", exc_info=True)
            raise err
        
    async def _process_one_flatmap(self, msg: Datum):
        msg_id = msg.uuid

        try:
            results = []
            # async for result in self._map_stream_handler.handler_stream(msg):
            async for result in self._map_stream_handler.handler(msg.keys, msg):
                results.append(result)
            
            # We intentially store results and send at completion of callback to ensure no partial returns
            for result in results:
                yield flatmap_pb2.MapResponse(
                    result=flatmap_pb2.MapResponse.Result(
                        keys=result.keys, value=result.value, tags=result.tags, uuid=msg_id
                    )
                )
            
            # TODO: Send completion message for given msg_id
        except Exception as err:
            err_msg = "UDFError, re-raising the error: %r" % err
            _LOGGER.critical(err_msg, exc_info=True)
            raise err
        

class FlatMapBatchMapServer(FlatmapServicerBase):
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
        next_awaiting = None
        print("MDW: batch:present_data GPT")
        async def fetch_next_datum():
            nonlocal keep_going
            nonlocal next_awaiting
            try:
                print(1)
                if next_awaiting is None:
                    print(1.1)
                    next_awaiting = asyncio.ensure_future(datum_iterator.__anext__())
                    print(1.2)

                item = await asyncio.wait_for(
                    asyncio.shield(next_awaiting),
                    timeout=timeout
                )
                next_awaiting = None
                return item
                # return await asyncio.wait_for(datum_iterator.__anext__(), timeout)
            except asyncio.TimeoutError:
                print(2)
                return None
            except StopAsyncIteration:
                print(3)
                keep_going = False
                return None

        # async def fetch_next_datum():
        #     nonlocal keep_going
        #     try:
        #         print(f"{time.time()} 1")
        #         x=  await anext(datum_iterator)
        #         print(f"{time.time()} 1.1")
        #         return x
        #     except asyncio.TimeoutError:
        #         print(2)
        #         return None
        #     except StopAsyncIteration:
        #         print(3)
        #         keep_going = False
        #         return None
            
        while keep_going:
            print("MDW: START fetch_next_datum")
            datum = await fetch_next_datum()
            print(f"MDW: DONE fetch_next_datum with {datum=}")
            if datum:
                buffer.append(datum)
                if len(buffer) >= batch_size:
                    print("MDW: Process because full")
                    async for message in self._process_stream_map(buffer):
                        yield message
                    buffer.clear()
                    start_time = datetime.now()
            else:
                if buffer:
                    print("MDW: Process because timeout but no data")
                    async for message in self._process_stream_map(buffer):
                        yield message
                    buffer.clear()
                    start_time = datetime.now()

            # Check if the timeout has been exceeded
            if (datetime.now() - start_time).total_seconds() >= timeout:
                print("MDW: What happens here?")
                if buffer:
                    print("   MDW: Finish processing final messages")
                    async for message in self._process_stream_map(buffer):
                        yield message
                    buffer.clear()
                    start_time = datetime.now()

            # if datum is None and not buffer:
            #     break

    async def _process_stream_map(self, msgs_deque: deque[Datum]):
        msgs = [msg for msg in msgs_deque]
        try:
            msg_id = msgs[0].uuid  # TODO: How to deal with mulitple messages at onces

            results = []
            # async for result in self._map_stream_handler.handler_stream(msg):
            async for result in self._map_stream_handler.handler(msgs):
                results.append(result)
            
            # We intentially store results and send at completion of callback to ensure no partial returns
            # TOOD: Move this to base class?
            print(f"MDW: Respond for {len(results)} messages")
            for result in results:
                # print(f"\tDropped message looks like {result}")
                # xx =  flatmap_pb2.MapResponse(
                #     result=flatmap_pb2.MapResponse.Result(
                #         keys=result.keys, value=result.value, tags=result.tags, uuid=msg_id
                #     )
                # )
                # print(f"\tDropped response looks like {xx}")
                # yield xx
                yield flatmap_pb2.MapResponse(
                    result=flatmap_pb2.MapResponse.Result(
                        keys=result.keys, value=result.value, tags=result.tags, uuid=msg_id
                    )
                )


            print(f"\tMDW: Send Drops {len(msgs)=}")
            # TODO: Send completion message for used message UUIDs
            # "Drop" all the non-first messages to indicate there is completion
            if len(msgs) >= 2:
                print(f"{msgs=}")
                for msg in msgs[1:]:
                    yield flatmap_pb2.MapResponse(
                            result=flatmap_pb2.MapResponse.Result(
                                keys=None, value=b"", tags=[DROP], uuid=msg.uuid
                            )
                        )

        except Exception as err:
            err_msg = "UDFError, re-raising the error: %r" % err
            _LOGGER.critical(err_msg, exc_info=True)
            raise err