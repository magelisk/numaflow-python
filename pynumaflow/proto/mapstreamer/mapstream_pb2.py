# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mapstream.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fmapstream.proto\x12\x0cmapstream.v1\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\xfc\x01\n\x10MapStreamRequest\x12\x0c\n\x04keys\x18\x01 \x03(\t\x12\r\n\x05value\x18\x02 \x01(\x0c\x12.\n\nevent_time\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12-\n\twatermark\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12<\n\x07headers\x18\x05 \x03(\x0b\x32+.mapstream.v1.MapStreamRequest.HeadersEntry\x1a.\n\x0cHeadersEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\x80\x01\n\x11MapStreamResponse\x12\x36\n\x06result\x18\x01 \x01(\x0b\x32&.mapstream.v1.MapStreamResponse.Result\x1a\x33\n\x06Result\x12\x0c\n\x04keys\x18\x01 \x03(\t\x12\r\n\x05value\x18\x02 \x01(\x0c\x12\x0c\n\x04tags\x18\x03 \x03(\t\"\x1e\n\rReadyResponse\x12\r\n\x05ready\x18\x01 \x01(\x08\x32\x9d\x01\n\tMapStream\x12P\n\x0bMapStreamFn\x12\x1e.mapstream.v1.MapStreamRequest\x1a\x1f.mapstream.v1.MapStreamResponse0\x01\x12>\n\x07IsReady\x12\x16.google.protobuf.Empty\x1a\x1b.mapstream.v1.ReadyResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mapstream_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _MAPSTREAMREQUEST_HEADERSENTRY._options = None
  _MAPSTREAMREQUEST_HEADERSENTRY._serialized_options = b'8\001'
  _globals['_MAPSTREAMREQUEST']._serialized_start=96
  _globals['_MAPSTREAMREQUEST']._serialized_end=348
  _globals['_MAPSTREAMREQUEST_HEADERSENTRY']._serialized_start=302
  _globals['_MAPSTREAMREQUEST_HEADERSENTRY']._serialized_end=348
  _globals['_MAPSTREAMRESPONSE']._serialized_start=351
  _globals['_MAPSTREAMRESPONSE']._serialized_end=479
  _globals['_MAPSTREAMRESPONSE_RESULT']._serialized_start=428
  _globals['_MAPSTREAMRESPONSE_RESULT']._serialized_end=479
  _globals['_READYRESPONSE']._serialized_start=481
  _globals['_READYRESPONSE']._serialized_end=511
  _globals['_MAPSTREAM']._serialized_start=514
  _globals['_MAPSTREAM']._serialized_end=671
# @@protoc_insertion_point(module_scope)
