from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SWInfoResponse(_message.Message):
    __slots__ = ("version", "build_date", "description")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    BUILD_DATE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    version: str
    build_date: str
    description: str
    def __init__(self, version: _Optional[str] = ..., build_date: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class HWInfoResponse(_message.Message):
    __slots__ = ("sensor_version", "model_type", "serial_number")
    SENSOR_VERSION_FIELD_NUMBER: _ClassVar[int]
    MODEL_TYPE_FIELD_NUMBER: _ClassVar[int]
    SERIAL_NUMBER_FIELD_NUMBER: _ClassVar[int]
    sensor_version: str
    model_type: str
    serial_number: str
    def __init__(self, sensor_version: _Optional[str] = ..., model_type: _Optional[str] = ..., serial_number: _Optional[str] = ...) -> None: ...
