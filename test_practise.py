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
def test_rbx():
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
def test_deviceX_1():
    """
    request has a few properties.
    request.module.__name__: this will be the name of the test script calling.
    request.scope: O/P can be 'function'
    request.session: This gives a lot of information. Like exitstatus, testsfailed, testscollected
                    You can print (request.session.testcollected)
    request.node: Gives a lot of extra handles. E.g:
                request.node - Will give you name of test.
                request.node.fixturenames - Will give name list of fixtures used now.
                request.node
    """
    assert 0

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