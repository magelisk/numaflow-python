from google.protobuf import empty_pb2 as _empty_pb2

from pynumaflow.mapbatch._dtypes import MapBatchSyncCallable
from pynumaflow.proto.mapbatch import mapbatch_pb2, mapbatch_pb2_grpc
from pynumaflow.mapbatch.servicer.utils import _map_fn_util
from pynumaflow.types import NumaflowServicerContext


class SyncBatchMapServicer(mapbatch_pb2_grpc.MapBatchServicer):
    """
    This class is used to create a new grpc Map Servicer instance.
    It implements the SyncMapServicer interface from the proto map.proto file.
    Provides the functionality for the required rpc methods.
    """

    def __init__(
        self,
        handler: MapBatchSyncCallable,
    ):
        self.__map_handler: MapBatchSyncCallable = handler

    def MapBatchFn(
        self, request: mapbatch_pb2.MapBatchRequest, context: NumaflowServicerContext
    ) -> mapbatch_pb2.MapBatchResponse:
        """
        Applies a function to each datum element.
        The pascal case function name comes from the proto map_pb2_grpc.py file.
        """
        return _map_fn_util(self.__map_handler, request, context)

    def IsReady(
        self, request: _empty_pb2.Empty, context: NumaflowServicerContext
    ) -> mapbatch_pb2.ReadyResponse:
        """
        IsReady is the heartbeat endpoint for gRPC.
        The pascal case function name comes from the proto map_pb2_grpc.py file.
        """
        return mapbatch_pb2.ReadyResponse(ready=True)
