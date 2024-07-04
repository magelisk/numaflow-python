from collections.abc import AsyncIterable
import grpc
from google.protobuf import empty_pb2 as _empty_pb2

from pynumaflow.batchmapper._dtypes import Datum
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


class AsyncBatchMapServicer(batchmap_pb2_grpc.BatchMapServicer):
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
