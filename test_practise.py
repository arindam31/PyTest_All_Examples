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

@pytest.mark.rbx
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
