import pytest
import allure
from google.protobuf.empty_pb2 import Empty
from product.proto import actions_pb2


@pytest.mark.usefixtures("grpc_channel")
class TestDeviceActions:
    @allure.title("Get logs from the device")
    @allure.description("This test attempts to get logs stored from the device.")
    @allure.tag("Logs", "DeviceActionTests")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.testcase("TC-100")
    def test_get_logs(self, actions_stub):
        response = actions_stub.GetDeviceLog(Empty())

        assert isinstance(response, actions_pb2.LogResponse)
        assert response.lines == ["Device started"]

    @allure.title("Test reboot behaviour")
    @allure.description("This test verifies parameters after a reboot.")
    @allure.tag("Boot Test", "DeviceActionTests")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.testcase("TC-101")
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
    
    @allure.title("Test soft reset behavior")
    @allure.description("This test verifies parameters after a soft reset.")
    @allure.tag("Reset Test", "DeviceActionTests")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.testcase("TC-102")
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
    
    @allure.title("Test hard reset behavior")
    @allure.description("This test verifies parameters after a hard reset.")
    @allure.tag("Reset Test", "DeviceActionTests")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.testcase("TC-103")
    def test_hard_reset(self, actions_stub):
        response = actions_stub.DoHardReset(Empty())
        assert isinstance(response, Empty), "DoSoftReset should return an Empty response"

        # Fetch Device logs
        logs_response = actions_stub.GetDeviceLog(Empty())
        logs = logs_response.lines

        # Assert: default one log should be present after Hard reset.
        assert len(logs) == 1, "Logs should be reset to default"
        
    @allure.title("Test service toggling")
    @allure.description("This test verifies toggling of services work.")
    @allure.tag("Service Toggle Test", "DeviceActionTests")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.testcase("TC-104")
    def test_toggle_valid_service(self, actions_stub):
        response = actions_stub.ToggleService(actions_pb2.ToggleRequest(service_name="bluetooth", enable=False))
        assert isinstance(response, actions_pb2.ToggleResponse), "ToggleService should return a ToggleResponse"
        assert response.status == "Done"
