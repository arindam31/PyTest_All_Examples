from unittest.mock import MagicMock, patch
import target
import unittest

def test_demo_mock():
    # This is a demo of mock using magicmock
    target.some_random_function = MagicMock()
    target.some_random_function.return_value = {
        "stored": True,
        "location": "target_log"
    }
    result = target.my_new_function()
    assert "images" in result

class TestTarget(unittest.TestCase):
    @patch('target.some_random_function')
    def test_my_function(self, mock_read):
        mock_read.return_value = {
            "stored": True,
            "location": "target_log"
        }
        result = target.my_new_function()
        assert "images" in result
