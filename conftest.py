import configparser
from datetime import datetime
import random

from pathlib import Path

import pytest
from _pytest.runner import runtestprotocol
from py.xml import html

from jinja2 import Environment, FileSystemLoader

version = "1.2.3"

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

template = env.get_template('summary.html')
res_list = []
tests_count = 0


def pytest_runtestloop(session):
    """
    This function gets us details about the tests that are collected before running.
    """
    global tests_count
    tests_count = session.testscollected


def pytest_runtest_protocol(item, nextitem):
    """
    This function is used to catch current status of test running.
    """

    reports = runtestprotocol(item, nextitem=nextitem)
    for report in reports:
        if report.outcome == 'skipped':
            evalxfail = getattr(item, '_evalxfail', None)
            if evalxfail:
                report.wasxfail = evalxfail.getexplanation()
            res_list.append({'test': item, 'result': report})
        if report.when == 'call':
            test_details = {'test': item, 'result': report}
            res_list.append(test_details)

    write_using_jinja(res_list)
    return True


def write_using_jinja(result_list):
    html_output = template.render(result_list=result_list, tests_count=tests_count)
    with open("reports/my_report.html", 'w') as fow:
        fow.write(html_output)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()

    extra = getattr(report, 'extra', [])
    envi = getattr(report, 'environment', [])
    # extra.append(pytest_html.extras.html("This gets added after every test item"))
    report.extra = extra


def pytest_html_report_title(report):
    report.title = "My very own title!"


def pytest_html_results_summary(prefix):
    prefix.extend([html.h1("Version: %s" % version)])


def pytest_configure(config):
    if not config.option.htmlpath:
        now = datetime.now()

        # reports_dir = Path('reports', now.strftime('%Y%m%d'))
        reports_dir = Path('reports')

        # This will make a new directory under reports with folder name as yearMonthDate
        # reports_dir.mkdir(parents=True, exist_ok=True)

        # This will be the report name
        # report = reports_dir / f"report_{now.strftime('%Y%m%d_%H%M')}.html"
        report = reports_dir / "report.html"

        config.option.htmlpath = report
        config.option.self_contained_html = True

    config._metadata["Image Version"] = version
    config._metadata["Branch"] = "Branch"


# *************************************************************************
# The below 2 functions are used to create command line argument . 
# In this case, a user can rovide a custom config file

def pytest_addoption(parser):
    parser.addoption("--cfg", action="store", default="config.ini", help="Name of config file")


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

@pytest.fixture(autouse=False)
def auto_skip_if_incorrect_device(request):
    marker_names = {m.name for m in request.node.iter_markers()}
    data = request.getfixturevalue('read_config')
    if marker_names and data['DEVICE']['name'] not in marker_names:
        pytest.skip("This device is not supported for this test")


# *************************************************************************
# This fixture is an example of scope: module
# The module scoped fixture is only once called and the
# value stays throughout the test.


@pytest.fixture(scope="module")
def my_special_random_number():
    return random.randint(1, 100)


@pytest.fixture(autouse=True)
def check_device_type(request, read_config):
    """Fixture functions can accept the request object to
    introspect the “requesting” test function, class or module context.

    This is also an example of how request can be used:

    request has a few properties which can be used. -----
    *******************************************************
    request.module.__name__: this will be the name of the test script calling.
    request.scope: O/P can be 'function'
    request.session: This gives a lot of information. Like exitstatus, testsfailed, testscollected
                    You can print (request.session.testcollected)
    request.node: Gives a lot of extra handles. E.g:
                request.node - Will give you name of test.
                request.node.fixturenames - Will give name list of fixtures used now.
                request.node

    """
    device = read_config['DEVICE']['name']
    marker = request.node.get_closest_marker('device_check')
    if marker:
        if marker.args[0] != device:
            msg = marker.kwargs.get("msg")
            pytest.skip(f"Skipped because: {msg}")
