# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from . import transform_pb2 as transform__pb2

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
        + f' but the generated code in transform_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class SourceTransformStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SourceTransformFn = channel.unary_unary(
                '/sourcetransformer.v1.SourceTransform/SourceTransformFn',
                request_serializer=transform__pb2.SourceTransformRequest.SerializeToString,
                response_deserializer=transform__pb2.SourceTransformResponse.FromString,
                _registered_method=True)
        self.IsReady = channel.unary_unary(
                '/sourcetransformer.v1.SourceTransform/IsReady',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=transform__pb2.ReadyResponse.FromString,
                _registered_method=True)


class SourceTransformServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SourceTransformFn(self, request, context):
        """SourceTransformFn applies a function to each request element.
        In addition to map function, SourceTransformFn also supports assigning a new event time to response.
        SourceTransformFn can be used only at source vertex by source data transformer.
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


def add_SourceTransformServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SourceTransformFn': grpc.unary_unary_rpc_method_handler(
                    servicer.SourceTransformFn,
                    request_deserializer=transform__pb2.SourceTransformRequest.FromString,
                    response_serializer=transform__pb2.SourceTransformResponse.SerializeToString,
            ),
            'IsReady': grpc.unary_unary_rpc_method_handler(
                    servicer.IsReady,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=transform__pb2.ReadyResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'sourcetransformer.v1.SourceTransform', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('sourcetransformer.v1.SourceTransform', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class SourceTransform(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SourceTransformFn(request,
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
            '/sourcetransformer.v1.SourceTransform/SourceTransformFn',
            transform__pb2.SourceTransformRequest.SerializeToString,
            transform__pb2.SourceTransformResponse.FromString,
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
            '/sourcetransformer.v1.SourceTransform/IsReady',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            transform__pb2.ReadyResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
