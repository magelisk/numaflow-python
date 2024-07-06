# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: reduce.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x0creduce.proto\x12\treduce.v1\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1fgoogle/protobuf/timestamp.proto"\x98\x04\n\rReduceRequest\x12\x31\n\x07payload\x18\x01 \x01(\x0b\x32 .reduce.v1.ReduceRequest.Payload\x12;\n\toperation\x18\x02 \x01(\x0b\x32(.reduce.v1.ReduceRequest.WindowOperation\x1a\x9e\x01\n\x0fWindowOperation\x12=\n\x05\x65vent\x18\x01 \x01(\x0e\x32..reduce.v1.ReduceRequest.WindowOperation.Event\x12"\n\x07windows\x18\x02 \x03(\x0b\x32\x11.reduce.v1.Window"(\n\x05\x45vent\x12\x08\n\x04OPEN\x10\x00\x12\t\n\x05\x43LOSE\x10\x01\x12\n\n\x06\x41PPEND\x10\x04\x1a\xf5\x01\n\x07Payload\x12\x0c\n\x04keys\x18\x01 \x03(\t\x12\r\n\x05value\x18\x02 \x01(\x0c\x12.\n\nevent_time\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12-\n\twatermark\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12>\n\x07headers\x18\x05 \x03(\x0b\x32-.reduce.v1.ReduceRequest.Payload.HeadersEntry\x1a.\n\x0cHeadersEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01"j\n\x06Window\x12)\n\x05start\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\'\n\x03\x65nd\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0c\n\x04slot\x18\x03 \x01(\t"\xa7\x01\n\x0eReduceResponse\x12\x30\n\x06result\x18\x01 \x01(\x0b\x32 .reduce.v1.ReduceResponse.Result\x12!\n\x06window\x18\x02 \x01(\x0b\x32\x11.reduce.v1.Window\x12\x0b\n\x03\x45OF\x18\x03 \x01(\x08\x1a\x33\n\x06Result\x12\x0c\n\x04keys\x18\x01 \x03(\t\x12\r\n\x05value\x18\x02 \x01(\x0c\x12\x0c\n\x04tags\x18\x03 \x03(\t"\x1e\n\rReadyResponse\x12\r\n\x05ready\x18\x01 \x01(\x08\x32\x8a\x01\n\x06Reduce\x12\x43\n\x08ReduceFn\x12\x18.reduce.v1.ReduceRequest\x1a\x19.reduce.v1.ReduceResponse(\x01\x30\x01\x12;\n\x07IsReady\x12\x16.google.protobuf.Empty\x1a\x18.reduce.v1.ReadyResponseb\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "reduce_pb2", _globals)
if _descriptor._USE_C_DESCRIPTORS is False:
    DESCRIPTOR._options = None
    _globals["_REDUCEREQUEST_PAYLOAD_HEADERSENTRY"]._options = None
    _globals["_REDUCEREQUEST_PAYLOAD_HEADERSENTRY"]._serialized_options = b"8\001"
    _globals["_REDUCEREQUEST"]._serialized_start = 90
    _globals["_REDUCEREQUEST"]._serialized_end = 626
    _globals["_REDUCEREQUEST_WINDOWOPERATION"]._serialized_start = 220
    _globals["_REDUCEREQUEST_WINDOWOPERATION"]._serialized_end = 378
    _globals["_REDUCEREQUEST_WINDOWOPERATION_EVENT"]._serialized_start = 338
    _globals["_REDUCEREQUEST_WINDOWOPERATION_EVENT"]._serialized_end = 378
    _globals["_REDUCEREQUEST_PAYLOAD"]._serialized_start = 381
    _globals["_REDUCEREQUEST_PAYLOAD"]._serialized_end = 626
    _globals["_REDUCEREQUEST_PAYLOAD_HEADERSENTRY"]._serialized_start = 580
    _globals["_REDUCEREQUEST_PAYLOAD_HEADERSENTRY"]._serialized_end = 626
    _globals["_WINDOW"]._serialized_start = 628
    _globals["_WINDOW"]._serialized_end = 734
    _globals["_REDUCERESPONSE"]._serialized_start = 737
    _globals["_REDUCERESPONSE"]._serialized_end = 904
    _globals["_REDUCERESPONSE_RESULT"]._serialized_start = 853
    _globals["_REDUCERESPONSE_RESULT"]._serialized_end = 904
    _globals["_READYRESPONSE"]._serialized_start = 906
    _globals["_READYRESPONSE"]._serialized_end = 936
    _globals["_REDUCE"]._serialized_start = 939
    _globals["_REDUCE"]._serialized_end = 1077
# @@protoc_insertion_point(module_scope)
