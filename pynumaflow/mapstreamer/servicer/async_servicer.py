from collections.abc import AsyncIterable

from google.protobuf import empty_pb2 as _empty_pb2

from pynumaflow.mapstreamer import Datum
from pynumaflow.mapstreamer._dtypes import MapStreamCallable
from pynumaflow.proto.mapstreamer import mapstream_pb2_grpc, mapstream_pb2
from pynumaflow.types import NumaflowServicerContext
from pynumaflow._constants import _LOGGER


async def datum_generator(
    request_iterator: AsyncIterable[mapstream_pb2.MapStreamRequest],
) -> AsyncIterable[Datum]:
    i = 0
    async for d in request_iterator:
        print(f"Loop {i}")
        datum = Datum(
            keys=list(d.keys),
            sink_msg_id=d.id,
            value=d.value,
            event_time=d.event_time.ToDatetime(),
            watermark=d.watermark.ToDatetime(),
            headers=dict(d.headers),
        )
        yield datum

class AsyncMapStreamServicer(mapstream_pb2_grpc.MapStreamServicer):
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
        self.__map_stream_handler: MapStreamCallable = handler

    async def MapStreamFn(
        self,
        request:  AsyncIterable[mapstream_pb2.MapStreamRequest],
        context: NumaflowServicerContext,
    ) -> AsyncIterable[mapstream_pb2.MapStreamResponse]:
        """
        Applies a map function to a datum stream in streaming mode.
        The pascal case function name comes from the proto mapstream_pb2_grpc.py file.
        """
        print('======= MDW ========')
        print(request)
        print(dir(request))
        datum_iterator = datum_generator(request_iterator=request)
        print(f"{datum_iterator}")
        print('======= MDW end========')
        async for res in self.__invoke_map_stream(
            [],
            datum_iterator
        ):
            yield mapstream_pb2.MapStreamResponse(result=res)

    async def __invoke_map_stream(self, keys: list[str], req: Datum):
        try:
            print(f"{req=}")
            print(f"{self.__map_stream_handler}")
            async for msg in self.__map_stream_handler(keys, req):
                yield mapstream_pb2.MapStreamResponse.Result(
                    keys=msg.keys, value=msg.value, tags=msg.tags
                )
        except Exception as err:
            print(f"{err=}")
            _LOGGER.critical("UDFError, re-raising the error", exc_info=True)
            raise err

    async def IsReady(
        self, request: _empty_pb2.Empty, context: NumaflowServicerContext
    ) -> mapstream_pb2.ReadyResponse:
        """
        IsReady is the heartbeat endpoint for gRPC.
        The pascal case function name comes from the proto mapstream_pb2_grpc.py file.
        """
        return mapstream_pb2.ReadyResponse(ready=True)
