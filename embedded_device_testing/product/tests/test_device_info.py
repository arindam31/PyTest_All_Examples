import allure
from google.protobuf.empty_pb2 import Empty
from product.proto import device_pb2
from product.proto import device_pb2_grpc


@allure.title("Test software info service")
@allure.description("This test verifies SW info service returns correct information.")
@allure.tag("Device Info")
@allure.severity(allure.severity_level.NORMAL)
@allure.testcase("TC-105")
def test_get_sw_info(grpc_channel):    
    stub = device_pb2_grpc.DeviceServiceStub(grpc_channel)

    response = stub.GetSWInfo(Empty())

    assert isinstance(response, device_pb2.SWInfoResponse)
    assert response.version != ""
    assert response.build_date != ""
    assert response.description != ""

@allure.title("Test hardware info service")
@allure.description("This test verifies HW info service returns correct information.")
@allure.tag("Device Info")
@allure.severity(allure.severity_level.NORMAL)
@allure.testcase("TC-106")
def test_get_hw_info(grpc_channel):
    stub = device_pb2_grpc.DeviceServiceStub(grpc_channel)

    response = stub.GetHWInfo(Empty())

    assert isinstance(response, device_pb2.HWInfoResponse)
    assert response.sensor_version == "10.20.30"
    assert response.model_type == "Alpha"
    assert response.serial_number == "VIRT-123456789"