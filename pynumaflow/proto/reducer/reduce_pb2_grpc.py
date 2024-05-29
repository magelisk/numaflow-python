# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from . import reduce_pb2 as reduce__pb2

GRPC_GENERATED_VERSION = '1.64.0'
GRPC_VERSION = grpc.__version__
EXPECTED_ERROR_RELEASE = '1.65.0'
SCHEDULED_RELEASE_DATE = 'June 25, 2024'
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    warnings.warn(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in reduce_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class ReduceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ReduceFn = channel.stream_stream(
                '/reduce.v1.Reduce/ReduceFn',
                request_serializer=reduce__pb2.ReduceRequest.SerializeToString,
                response_deserializer=reduce__pb2.ReduceResponse.FromString,
                _registered_method=True)
        self.IsReady = channel.unary_unary(
                '/reduce.v1.Reduce/IsReady',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=reduce__pb2.ReadyResponse.FromString,
                _registered_method=True)


class ReduceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ReduceFn(self, request_iterator, context):
        """ReduceFn applies a reduce function to a request stream.
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


def add_ReduceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ReduceFn': grpc.stream_stream_rpc_method_handler(
                    servicer.ReduceFn,
                    request_deserializer=reduce__pb2.ReduceRequest.FromString,
                    response_serializer=reduce__pb2.ReduceResponse.SerializeToString,
            ),
            'IsReady': grpc.unary_unary_rpc_method_handler(
                    servicer.IsReady,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=reduce__pb2.ReadyResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'reduce.v1.Reduce', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('reduce.v1.Reduce', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class Reduce(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ReduceFn(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(
            request_iterator,
            target,
            '/reduce.v1.Reduce/ReduceFn',
            reduce__pb2.ReduceRequest.SerializeToString,
            reduce__pb2.ReduceResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

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
        return grpc.experimental.unary_unary(
            request,
            target,
            '/reduce.v1.Reduce/IsReady',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            reduce__pb2.ReadyResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
