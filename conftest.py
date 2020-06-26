import os
import configparser
import random
from py.xml import html
import pytest
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader
import pdb


#file_loader = FileSystemLoader('templates')
#env = Environment(loader=file_loader)

#template = env.get_template('summary.html')

version = "1.2.3"

#
#def template_report():
#	tm = template.render({'sw_version': version})
#	return tm

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
	pytest_html = item.config.pluginmanager.getplugin('html')
	outcome = yield
	report = outcome.get_result()
	extra = getattr(report, 'extra', [])
	#msg = template_report()


	#extra.append(pytest_html.extras.html(msg))
	extra.append(pytest_html.extras.html("This gets added after every test item"))
	report.extra = extra

def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend([html.p("foo: bar")])


# *************************************************************************
# The below 2 functions are used to create command line argument . user can
# provide a custom config file: pytest --cfg=config1.ini test_practise.py
def pytest_addoption(parser):
    parser.addoption("--cfg", action="store", default=None, help="Name of DUT type")

# *************************************************************************
# Custom Marker usage: In this fixture, we see that
# when all test are run, the config value is checked if it exists in
# the markers list includes the value. If yes, we execute the test.
# Else, we skip it.

@pytest.fixture(autouse=False)
def auto_skip_if_incorrect_device(request):
    marker_names = {m.name for m in request.node.iter_markers()}
    data = request.getfixturevalue('read_config')
    if marker_names and data['DEVICE']['name'] not in marker_names:
        pytest.skip("This device is not supported for this test")

# ************************************ END *********************************
# This fixture is an example of scope: module
# The module scoped fixture is only once called and the
# value stays througout the test.


@pytest.fixture(scope="module")
def my_special_random_number():
    return random.randint(1,100)

# *************************************************************************
@pytest.fixture(autouse=False)
def cfg(request):
    return request.config.getoption("cfg")
        
# *************************************************************************
@pytest.fixture(autouse=False)
def read_config(cfg):
    if cfg:
        assert os.path.exists(cfg), 'Config file:{} not found'.format(cfg)
        config = configparser.ConfigParser()
        config.read(cfg)
        return config
    else:
        raise Exception('No config file provided. Must provide one, for running tests with marker "device_check".')

# ********************************* END ***********************************

@pytest.fixture(autouse=False)
def check_device_type(request, read_config):
    """Fixture functions can accept the request object to
    introspect the “requesting” test function, class or module context.
    The request fixture is a special fixture providing information of the requesting test function.

    This is also an example of how request can be used:

    request has a few properties which can be used. -----
    *******************************************************
    Refer: https://docs.pytest.org/en/latest/reference.html

    request.module.__name__: this will be the name of the test script calling.
    request.scope: Scope string, one of “function”, “class”, “module”, “session”
    request.session: This gives a lot of information. Like exitstatus, testsfailed, testscollected
                    You can print (request.session.testcollected)
    request.node: Gives a lot of extra handles. E.g:
                request.node - Will give you name of test.
                request.node.fixturenames - Will give name list of fixtures used now.
                request.node.get_closest_marker(name) - Will give the marker matching closest.
                request.node.config.getini('markers') - Will return list of markers in pytest.ini file.
    request.config: All about config used.
                request.config.getoption('cfg')
    request.fixturenames: All fixtures used when the test is run.
                E.g o/p for test_deviceX_1: ['check_device_type', 'request', 'read_config', 'cfg']
    request.getfixturevalue: Gets the output of fixture. E.g:
                request.getfixturevalue('cfg')
                request.getfixturevalue('read_config')['DEVICE']
    """
    
    # marker is an object of class 'Mark'.
    # It has attributes: 'args', 'combined_with', 'kwargs', 'name'
    marker = request.node.get_closest_marker('device_check')
    import pdb
    pdb.set_trace()

    if read_config.has_option('DEVICE', 'name'):
        device_name = read_config['DEVICE']['name']
    else:
        raise Exception('Missing DEVICE name in config file.')

    if marker:
        if marker.args[0] != device_name:
            msg = marker.kwargs.get("msg")
            pytest.skip(f"Skipped because: {msg}")
