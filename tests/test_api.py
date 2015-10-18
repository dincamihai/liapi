import mock
import pytest
import responses
from apiwrapper.handler import JMXHandler
from apiwrapper import exceptions


def test_create_scenario(wrapper, create_scenario_response):
    with responses.RequestsMock() as rsps:
        rsps.add(**create_scenario_response)
        scenario_id = wrapper.create_scenario()
    assert scenario_id == 82431


def test_create_config(wrapper, create_config_response):
    with responses.RequestsMock() as rsps:
        rsps.add(**create_config_response)
        config_id = wrapper.create_test_config(1)
        assert config_id == 3204290


def test_wrapper_data():
    wrapper = JMXHandler('tests/sample.jmx')
    assert wrapper.data
