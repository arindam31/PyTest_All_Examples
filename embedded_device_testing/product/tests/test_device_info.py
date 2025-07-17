import grpc
import pytest
from google.protobuf.empty_pb2 import Empty
from product.proto import device_pb2
from product.proto import device_pb2_grpc


def test_get_sw_info(grpc_channel):
    stub = device_pb2_grpc.DeviceServiceStub(grpc_channel)

    response = stub.GetSWInfo(Empty())

    assert isinstance(response, device_pb2.SWInfoResponse)
    assert response.version != ""
    assert response.build_date != ""
    assert response.description != ""

def test_get_hw_info(grpc_channel):
    stub = device_pb2_grpc.DeviceServiceStub(grpc_channel)

    response = stub.GetHWInfo(Empty())

    assert isinstance(response, device_pb2.HWInfoResponse)
    assert response.sensor_version == "10.20.30"
    assert response.model_type == "Alpha"
    assert response.serial_number == "VIRT-123456789"