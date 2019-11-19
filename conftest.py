import configparser
import random
from py.xml import html
import pytest
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader



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
# provide a custom config file
def pytest_addoption(parser):
    parser.addoption("--cfg", action="store", default="XYZ", help="Name of DUT type")

@pytest.fixture
def cfg(request):
    return request.config.getoption("--cfg")


# *************************************************************************
@pytest.fixture
def read_config(cfg):
    config = configparser.ConfigParser()
    config.read(cfg)
    return config

# *************************************************************************
# Custom Marker usage: In this fixture, we see that
# when all test are run, the config value is checked if it exists in 
# the markers list includes the value. If yes, we execute the test.
# Else, we skip it.

@pytest.fixture(autouse=True)
def auto_skip_if_incorrect_device(request):
    marker_names = {m.name for m in request.node.iter_markers()}
    data = request.getfixturevalue('read_config')
    if marker_names and data['DEVICE']['name'] not in marker_names:
        pytest.skip("This device is not supported for this test")

# *************************************************************************
# This fixture is an example of scope: module
# The module scoped fixture is only once called and the
# value stays througout the test.


@pytest.fixture(scope="module")
def my_special_random_number():
    return random.randint(1,100)
    


