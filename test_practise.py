import pytest
import os
import pdb

def test_name():
    name = "Somename"
    assert name == name.title()

@pytest.mark.parametrize("name, expected", [('The', 'The'), ('game', 'Game')])
def test_for_matches(name, expected):
    assert name == expected

@pytest.mark.parametrize("name", ['Sir', 'Madam', 'John'])
def test_for_titles(name):
    assert name == name.title()

@pytest.mark.skipif(10 > 0, reason="Skipped since 10 > 0")
def test_skip_with_condition():
	assert 1 == 1

def test_using_command_line_arg_cfg(cfg):
	assert(os.path.exists(cfg)), "Config file name incorrect"

@pytest.mark.device_check("rbx", msg="Test for only rbx")
def test_rbx(check_device_type):
	print ("This is an RBX test")


@pytest.mark.mbx
def test_mbx():
	print ("This is an MBX test")

def test_random_no1(my_special_random_number):
    print(my_special_random_number)
    assert True

def test_random_no2(my_special_random_number):
    print(my_special_random_number)
    assert True

@pytest.mark.device_check("DeviceX", msg="Test for only DeviceX")
def test_deviceX_1(check_device_type):
    """
    Test to check the device_check fixture.

    To test this one, if we run the command:
        pytest -v -m "device_check" test_practise.py::test_deviceX_1  --cfg=config1.ini

        # Result: Pass (if your config file has 'name' value same as 'DeviceX')

    Also we can run this test like this too:
        pytest -m "device_check" test_practise.py

        # This will run all tests that have a device_check marker

    """
    assert 1

dict_dev = [
            ('a', {'x':True, 'y': False}),
            ('b',{'x':True, 'y': True}),
            ('c', {'x':True, 'y': True}),
            ]

@pytest.mark.parametrize("name, properties", dict_dev)
def test_dev_props(name, properties):
    print(name, properties)
    assert properties['x'] == True
    assert properties['y'] == True

@pytest.mark.resets_device
def test_some_reset():
    assert True