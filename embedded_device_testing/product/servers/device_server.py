import grpc
import time
from datetime import date
from concurrent import futures

import proto.device_pb2 as device_pb2
import proto.device_pb2_grpc as device_pb2_grpc


class DeviceService(device_pb2_grpc.DeviceServiceServicer):

    def GetSWInfo(self, request, context):
        # Return a dummy info
        return device_pb2.SWInfoResponse(
            version="1.0.0",
            build_date=str(date.today()),
            description="Virtual device firmware v1.0.0"
        )
    
    def GetHWInfo(self, request, context):
        return device_pb2.HWInfoResponse(
            sensor_version="10.20.30",
            model_type="Alpha",
            serial_number="VIRT-123456789"
        )
    
def start_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    device_pb2_grpc.add_DeviceServiceServicer_to_server(servicer=DeviceService(), server=server)
    # listen on port 50051

    print('Starting server. Listening on port 50051.')
    server.add_insecure_port('[::]:50051')
    server.start()

    print("gRPC server running on port 50051...")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

    
if __name__ == "__main__":
    start_server()