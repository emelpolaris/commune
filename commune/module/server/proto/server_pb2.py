# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: server.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cserver.proto\"G\n\tDataBlock\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\x0c\x12\x10\n\x08metadata\x18\x02 \x01(\x0c\x12\x1a\n\x06\x62locks\x18\x03 \x03(\x0b\x32\n.DataBlock2-\n\x06Server\x12#\n\x07\x46orward\x12\n.DataBlock\x1a\n.DataBlock\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'server_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _globals['_DATABLOCK']._serialized_start=16
  _globals['_DATABLOCK']._serialized_end=87
  _globals['_SERVER']._serialized_start=89
  _globals['_SERVER']._serialized_end=134
# @@protoc_insertion_point(module_scope)