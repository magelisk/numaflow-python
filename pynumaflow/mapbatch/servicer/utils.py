import grpc
from pynumaflow.mapbatch._dtypes import MapBatchSyncCallable

from pynumaflow.mapbatch._dtypes import Datum
from pynumaflow.proto.mapbatch import mapbatch_pb2
from pynumaflow.types import NumaflowServicerContext
from pynumaflow._constants import _LOGGER


def _map_fn_util(
    __map_handler: MapBatchSyncCallable, request: mapbatch_pb2.MapBatchRequest, context: NumaflowServicerContext
) -> mapbatch_pb2.MapBatchResponse:
    # proto repeated field(keys) is of type google._upb._message.RepeatedScalarContainer
    # we need to explicitly convert it to list
    try:
        print(request)
        grouped = [Datum(
                keys=list(req.keys),
                value=req.value,
                event_time=req.event_time.ToDatetime(),
                watermark=req.watermark.ToDatetime(),
                headers=dict(req.headers),
            ) for req in request.messages]
        msgs = __map_handler(grouped)
        print(f"MDW: Got messages {msgs}")
        # msgs = __map_handler(
        #     list(request.keys),
        #     Datum(
        #         keys=list(request.keys),
        #         value=request.value,
        #         event_time=request.event_time.ToDatetime(),
        #         watermark=request.watermark.ToDatetime(),
        #         headers=dict(request.headers),
        #     ),
        # )
    except Exception as err:
        _LOGGER.critical("UDFError, re-raising the error", exc_info=True)
        context.set_code(grpc.StatusCode.UNKNOWN)
        context.set_details(str(err))
        return mapbatch_pb2.MapBatchResponse(results=[])

    datums = []

    for msg in msgs:
        datums.append(mapbatch_pb2.MapBatchResponse.Result(keys=msg.keys, value=msg.value, tags=msg.tags))

    print(f"MDW: Send back datums:: {datums}")
    return mapbatch_pb2.MapBatchResponse(results=datums)
