import pytest 
import grpc

@pytest.fixture(scope="module")
def grpc_channel():
    """Fixture to connect/disconnect to device server."""
    channel = grpc.insecure_channel("localhost:50051")
    yield channel
    channel.close()
