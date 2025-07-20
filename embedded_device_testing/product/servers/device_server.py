import grpc
import time
from datetime import date
from concurrent import futures

from google.protobuf.empty_pb2 import Empty
from grpc_health.v1 import health_pb2
from grpc_health.v1 import health, health_pb2_grpc
import proto.device_pb2 as device_pb2
import proto.device_pb2_grpc as device_pb2_grpc
import proto.actions_pb2 as actions_pb2
import proto.actions_pb2_grpc as actions_pb2_grpc


device_state = {
    "services": {"bluetooth": True, "wifi": True},
    "logs": ["Device started"],
    "boot_count": 0,
}



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
    
class ActionService(actions_pb2_grpc.DeviceActionsServicer):

    def GetDeviceLog(self, request, context):
        return actions_pb2.LogResponse(lines=device_state["logs"])
    
    def Reboot(self, request, context):
        device_state["logs"].append("Rebooting device...")
        device_state["boot_count"] += 1
        device_state["logs"].append(f"Boot count: {device_state['boot_count']}")
        return Empty()
    
    def ResetState(self, request, context):
        device_state["logs"] = ["Device started"]
        device_state["boot_count"] = 0
        device_state["services"] = {"bluetooth": False, "wifi": False}
        return Empty()

    def DoSoftReset(self, request, context):
        device_state["logs"].append("Soft reset initiated.")
        device_state["services"]["bluetooth"] = True
        return Empty()

    def DoHardReset(self, request, context):
        self.ResetState(request, context)
        return Empty()
    
    def ToggleService(self, request, context):
        service_name = request.service_name.lower()
        service = device_state["services"].get(service_name, None)
        if service is None:
            return actions_pb2.ToggleResponse("Invalid Service name")
        
        if service:
            device_state["services"].get(service_name, not service)
        return actions_pb2.ToggleResponse(status="Done")
    
def start_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    health_servicer = health.HealthServicer()
    health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)
    device_pb2_grpc.add_DeviceServiceServicer_to_server(servicer=DeviceService(), server=server)
    actions_pb2_grpc.add_DeviceActionsServicer_to_server(servicer=ActionService(), server=server)

    # Set status for health check
    health_servicer.set("", health_pb2.HealthCheckResponse.SERVING)

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