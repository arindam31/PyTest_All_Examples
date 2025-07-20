import time
import grpc
from grpc_health.v1 import health_pb2_grpc, health_pb2

MAX_RETRIES = 5
DELAY = 1  # seconds
TARGET = "localhost:50051"  # Change port if needed

def wait_for_grpc():
    for attempt in range(MAX_RETRIES):
        try:
            with grpc.insecure_channel(TARGET) as channel:
                stub = health_pb2_grpc.HealthStub(channel)
                response = stub.Check(health_pb2.HealthCheckRequest(service=""))
                if response.status == health_pb2.HealthCheckResponse.SERVING:
                    print("⭐ gRPC server is healthy!")
                    return True
        except Exception as e:
            print(f"Attempt {attempt + 1}: gRPC not ready ({e})")
        time.sleep(DELAY)

    print("💔 gRPC server did not become healthy in time.")
    return False

if __name__ == "__main__":
    success = wait_for_grpc()
    exit(0 if success else 1)
