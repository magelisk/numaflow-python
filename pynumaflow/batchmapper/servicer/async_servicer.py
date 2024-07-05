import asyncio
from collections import deque
from collections.abc import AsyncIterable
from datetime import datetime, timedelta

import grpc
from google.protobuf import empty_pb2 as _empty_pb2

from pynumaflow.batchmapper._dtypes import Datum, Message, Messages, BatchResponses
from pynumaflow.batchmapper._dtypes import MapBatchAsyncHandlerCallable
from pynumaflow.proto.batchmapper import batchmap_pb2, batchmap_pb2_grpc
from pynumaflow.types import NumaflowServicerContext
from pynumaflow._constants import _LOGGER


async def datum_generator(
    request_iterator: AsyncIterable[batchmap_pb2.BatchMapRequest],
) -> AsyncIterable[Datum]:
    async for d in request_iterator:
        datum = Datum(
            id=d.id,
            keys=list(d.keys),
            value=d.value,
            event_time=d.event_time.ToDatetime(),
            watermark=d.watermark.ToDatetime(),
            headers=dict(d.headers),
        )
        yield datum


class AsyncBatchMapServicerBase(batchmap_pb2_grpc.BatchMapServicer):
    """
    This class is used to create a new grpc Async Map Servicer instance.
    It implements the SyncMapServicer interface from the proto map.proto file.
    Provides the functionality for the required rpc methods.
    """

    def __init__(
        self,
        handler: MapBatchAsyncHandlerCallable,
    ):
        self.__map_batch_handler: MapBatchAsyncHandlerCallable = handler


    async def IsReady(
        self, request: _empty_pb2.Empty, context: NumaflowServicerContext
    ) -> batchmap_pb2.ReadyResponse:
        """
        IsReady is the heartbeat endpoint for gRPC.
        The pascal case function name comes from the proto batchmap_pb2_grpc.py file.
        """
        return batchmap_pb2.ReadyResponse(ready=True)

    async def BatchMapFn(
        self,
        request_iterator: AsyncIterable[batchmap_pb2.BatchMapRequest],
        context: NumaflowServicerContext,
    ) -> AsyncIterable[batchmap_pb2.BatchMapResponse]:
        """
        Applies a sink function to a list of datum elements.
        The pascal case function name comes from the proto sink_pb2_grpc.py file.
        """
        datum_iterator = datum_generator(request_iterator=request_iterator)

        try:
            async for msg in self.__invoke_stream_batch(datum_iterator):
                yield msg
        except Exception as err:
            _LOGGER.critical("UDFError, re-raising the error", exc_info=True)
            raise err

    async def __invoke_stream_batch(self, datum_iterator: AsyncIterable[Datum]):
        try:
            
            async for response_msgs in self.__map_batch_handler.handler(datum_iterator):
                # Implicitly ensure we have a list
                yield batchmap_pb2.BatchMapResponse(
                    results=[batchmap_pb2.BatchMapResponse.Result(
                        keys=msg.keys, value=msg.value, tags=msg.tags
                    ) for msg in response_msgs.messages],
                    id=response_msgs.id
                )
        except Exception as err:
            err_msg = "UDSinkError: %r" % err
            _LOGGER.critical(err_msg, exc_info=True)

            async for _datum in datum_iterator:
                yield batchmap_pb2.BatchMapResponse(
                    batchmap_pb2.BatchMapResponse.Result.as_failure(_datum.id, err_msg)
                )

#----
class StreamFlatMap(AsyncBatchMapServicerBase):
    """Operates a async-asynchronus unary style prentation. Does not provide batching,
    but a streamlined interface for individual message handling that can be used in place of `mapper.MapAsyncServer`"""
    async def present_data(
        self,
        datum_iterator: AsyncIterable[Datum],
        context: NumaflowServicerContext,
    ) -> AsyncIterable[batchmap_pb2.BatchMapResponse]:
        print("MDW: flatmap:present_data")
        try:
            async for msg in datum_iterator:
                async for to_ret in self._process_one_flatmap(msg):
                    yield to_ret
        except Exception as err:
            _LOGGER.critical("UDFError, re-raising the error", exc_info=True)
            raise err
        
    async def _process_one_flatmap(self, msg: Datum):
        msg_id = msg.id

        try:
            results: Message = []
            # async for result in self._map_stream_handler.handler_stream(msg):
            async for result in self._map_stream_handler.handler(msg.keys, msg):
                if isinstance(result, Message):
                    results.append(result)
                else:
                    results.append([m for m in result])
            
            # We intentially store results and send at completion of callback to ensure no partial returns
            yield batchmap_pb2.BatchMapResponse(
                results=results,
                id=msg_id
            )
            
        except Exception as err:
            err_msg = "UDFError, re-raising the error: %r" % err
            _LOGGER.critical(err_msg, exc_info=True)
            raise err
        

class StreamBatchMap(AsyncBatchMapServicerBase):
    def __init__(self, 
                 handler: MapBatchAsyncHandlerCallable,
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
            async for response_msgs in self.__map_batch_handler.handler(msgs):
                # Implicitly ensure we have a list
                yield batchmap_pb2.BatchMapResponse(
                    results=[batchmap_pb2.BatchMapResponse.Result(
                        keys=msg.keys, value=msg.value, tags=msg.tags
                    ) for msg in response_msgs.messages],
                    id=response_msgs.id
                )
        except Exception as err:
            err_msg = "UDSinkError: %r" % err
            _LOGGER.critical(err_msg, exc_info=True)

            async for _datum in msgs:
                yield batchmap_pb2.BatchMapResponse(
                    batchmap_pb2.BatchMapResponse.Result.as_failure(_datum.id, err_msg)
                )

        #     results = []
        #     # async for result in self._map_stream_handler.handler_stream(msg):
        #     async for result in self._map_stream_handler.handler(msgs):
        #         results.append(result)
            
        #     # We intentially store results and send at completion of callback to ensure no partial returns
        #     # TOOD: Move this to base class?
        #     for result in results:
        #         yield mapstream_pb2.MapStreamResponse(
        #             result=mapstream_pb2.MapStreamResponse.Result(
        #                 keys=result.keys, value=result.value, tags=result.tags  # MDW: 
        #             )
        #         )
            
        #     # TODO: Send completion message for given msg_id
        # except Exception as err:
        #     err_msg = "UDFError, re-raising the error: %r" % err
        #     _LOGGER.critical(err_msg, exc_info=True)
        #     raise err