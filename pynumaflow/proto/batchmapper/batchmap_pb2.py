# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: batchmap.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x0e\x62\x61tchmap.proto\x12\x0b\x62\x61tchmap.v1\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1fgoogle/protobuf/timestamp.proto"\x85\x02\n\x0f\x42\x61tchMapRequest\x12\x0c\n\x04keys\x18\x01 \x03(\t\x12\r\n\x05value\x18\x02 \x01(\x0c\x12.\n\nevent_time\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12-\n\twatermark\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12:\n\x07headers\x18\x05 \x03(\x0b\x32).batchmap.v1.BatchMapRequest.HeadersEntry\x12\n\n\x02id\x18\x06 \x01(\t\x1a.\n\x0cHeadersEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01"\x8a\x01\n\x10\x42\x61tchMapResponse\x12\x35\n\x07results\x18\x01 \x03(\x0b\x32$.batchmap.v1.BatchMapResponse.Result\x12\n\n\x02id\x18\x02 \x01(\t\x1a\x33\n\x06Result\x12\x0c\n\x04keys\x18\x01 \x03(\t\x12\r\n\x05value\x18\x02 \x01(\x0c\x12\x0c\n\x04tags\x18\x03 \x03(\t"\x1e\n\rReadyResponse\x12\r\n\x05ready\x18\x01 \x01(\x08\x32\x98\x01\n\x08\x42\x61tchMap\x12=\n\x07IsReady\x12\x16.google.protobuf.Empty\x1a\x1a.batchmap.v1.ReadyResponse\x12M\n\nBatchMapFn\x12\x1c.batchmap.v1.BatchMapRequest\x1a\x1d.batchmap.v1.BatchMapResponse(\x01\x30\x01\x42<Z:github.com/numaproj/numaflow-go/pkg/apis/proto/batchmap/v1b\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "batchmap_pb2", _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals["DESCRIPTOR"]._loaded_options = None
    _globals[
        "DESCRIPTOR"
    ]._serialized_options = b"Z:github.com/numaproj/numaflow-go/pkg/apis/proto/batchmap/v1"
    _globals["_BATCHMAPREQUEST_HEADERSENTRY"]._loaded_options = None
    _globals["_BATCHMAPREQUEST_HEADERSENTRY"]._serialized_options = b"8\001"
    _globals["_BATCHMAPREQUEST"]._serialized_start = 94
    _globals["_BATCHMAPREQUEST"]._serialized_end = 355
    _globals["_BATCHMAPREQUEST_HEADERSENTRY"]._serialized_start = 309
    _globals["_BATCHMAPREQUEST_HEADERSENTRY"]._serialized_end = 355
    _globals["_BATCHMAPRESPONSE"]._serialized_start = 358
    _globals["_BATCHMAPRESPONSE"]._serialized_end = 496
    _globals["_BATCHMAPRESPONSE_RESULT"]._serialized_start = 445
    _globals["_BATCHMAPRESPONSE_RESULT"]._serialized_end = 496
    _globals["_READYRESPONSE"]._serialized_start = 498
    _globals["_READYRESPONSE"]._serialized_end = 528
    _globals["_BATCHMAP"]._serialized_start = 531
    _globals["_BATCHMAP"]._serialized_end = 683
# @@protoc_insertion_point(module_scope)
