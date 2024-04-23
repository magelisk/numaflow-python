# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from . import mapbatch_pb2 as mapbatch__pb2


class MapBatchStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.MapBatchFn = channel.unary_unary(
                '/mapbatch.v1.MapBatch/MapBatchFn',
                request_serializer=mapbatch__pb2.MapBatchRequest.SerializeToString,
                response_deserializer=mapbatch__pb2.MapBatchResponse.FromString,
                )
        self.IsReady = channel.unary_unary(
                '/mapbatch.v1.MapBatch/IsReady',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=mapbatch__pb2.ReadyResponse.FromString,
                )


class MapBatchServicer(object):
    """Missing associated documentation comment in .proto file."""

    def MapBatchFn(self, request, context):
        """MapBatchFn applies a function to mulitple elements at once
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def IsReady(self, request, context):
        """IsReady is the heartbeat endpoint for gRPC.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MapBatchServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'MapBatchFn': grpc.unary_unary_rpc_method_handler(
                    servicer.MapBatchFn,
                    request_deserializer=mapbatch__pb2.MapBatchRequest.FromString,
                    response_serializer=mapbatch__pb2.MapBatchResponse.SerializeToString,
            ),
            'IsReady': grpc.unary_unary_rpc_method_handler(
                    servicer.IsReady,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=mapbatch__pb2.ReadyResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'mapbatch.v1.MapBatch', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class MapBatch(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def MapBatchFn(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mapbatch.v1.MapBatch/MapBatchFn',
            mapbatch__pb2.MapBatchRequest.SerializeToString,
            mapbatch__pb2.MapBatchResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def IsReady(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mapbatch.v1.MapBatch/IsReady',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            mapbatch__pb2.ReadyResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)