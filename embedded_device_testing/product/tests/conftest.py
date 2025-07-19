import pytest
import allure
import grpc
from product.proto import actions_pb2_grpc
from product.proto import device_pb2_grpc
from google.protobuf.empty_pb2 import Empty


@pytest.fixture(scope="module")
def grpc_channel():
    """Fixture to connect/disconnect to device server."""
    channel = grpc.insecure_channel("localhost:50051")
    yield channel
    channel.close()


@pytest.fixture
@allure.title("Create a stub for Device Action Services")
def actions_stub(grpc_channel):
    return actions_pb2_grpc.DeviceActionsStub(grpc_channel)

@pytest.fixture
@allure.title("Create a stub for General Servies")
def device_stub(grpc_channel):
    return device_pb2_grpc.DeviceServiceStub(grpc_channel)

@pytest.fixture(autouse=True, scope="function")
@allure.title("Auto reset device states befoe every test.")
def reset_device_state(actions_stub):
    actions_stub.ResetState(Empty())