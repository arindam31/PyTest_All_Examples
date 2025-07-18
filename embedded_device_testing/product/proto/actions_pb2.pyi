from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ToggleRequest(_message.Message):
    __slots__ = ("service_name", "enable")
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    ENABLE_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    enable: bool
    def __init__(self, service_name: _Optional[str] = ..., enable: bool = ...) -> None: ...

class ToggleResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: str
    def __init__(self, status: _Optional[str] = ...) -> None: ...

class LogResponse(_message.Message):
    __slots__ = ("lines",)
    LINES_FIELD_NUMBER: _ClassVar[int]
    lines: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, lines: _Optional[_Iterable[str]] = ...) -> None: ...
