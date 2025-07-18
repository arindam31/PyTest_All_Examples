import grpc
import pytest
from google.protobuf.empty_pb2 import Empty
from product.proto import actions_pb2


@pytest.mark.usefixtures("grpc_channel")
class TestDeviceActions:
    def test_get_logs(self, actions_stub):
        response = actions_stub.GetDeviceLog(Empty())

        assert isinstance(response, actions_pb2.LogResponse)
        assert response.lines == ["Device started"]

    def test_reboot(self, actions_stub):
        response = actions_stub.Reboot(Empty())
        assert isinstance(response, Empty), "Reboot should return an Empty response"

        # Fetch Device logs
        logs_response = actions_stub.GetDeviceLog(Empty())
        logs = logs_response.lines

        # Assert: Log must end with "Rebooting..." and boot count 1
        logs_expected = ["Rebooting device...", "Boot count: 1"]
        assert len(logs) >= 2, "Logs should contain at least two entries"
        assert logs[-2:] == logs_expected, f"Expected last logs: {logs_expected}, got: {logs[-2:]}"
    
    def test_soft_reset(self, actions_stub):
        response = actions_stub.DoSoftReset(Empty())
        assert isinstance(response, Empty), "DoSoftReset should return an Empty response"

        # Fetch Device logs
        logs_response = actions_stub.GetDeviceLog(Empty())
        logs = logs_response.lines

        # Assert: Log must end with "Rebooting..." and boot count 1
        log_expected = "Soft reset initiated."
        assert len(logs) >= 1, "Logs should contain at least two entries"
        assert logs[-1] == log_expected, f"Expected last log: {log_expected}, got: {logs[-1]}"
    
    def test_hard_reset(self, actions_stub):
        response = actions_stub.DoHardReset(Empty())
        assert isinstance(response, Empty), "DoSoftReset should return an Empty response"

        # Fetch Device logs
        logs_response = actions_stub.GetDeviceLog(Empty())
        logs = logs_response.lines

        # Assert: default one log should be present after Hard reset.
        assert len(logs) == 1, "Logs should be reset to default"
        
    def test_toggle_valid_service(self, actions_stub):
        response = actions_stub.ToggleService(actions_pb2.ToggleRequest(service_name="bluetooth", enable=False))
        assert isinstance(response, actions_pb2.ToggleResponse), "ToggleService should return a ToggleResponse"
        assert response.status == "Done"
