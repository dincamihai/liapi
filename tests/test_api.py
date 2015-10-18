import mock
import json
import pytest
import responses
from apiwrapper.handler import JMXHandler
from apiwrapper import exceptions


@pytest.fixture(scope='function')
def create_scenario_response_400(request):
    return dict(
        method=responses.POST,
        url='https://api.loadimpact.com/v2/user-scenarios',
        status=400,
        content_type='application/json',
        body=json.dumps(
            {u'message': u'JSON parse error - No JSON object could be decoded'}
        )
    )


def test_create_scenario_400(wrapper, create_scenario_response_400):
    with pytest.raises(exceptions.BadRequestException) as exc:
        with responses.RequestsMock() as rsps:
            rsps.add(**create_scenario_response_400)
            wrapper.create_scenario()
    assert exc.value.message == "Could not create scenario. Bad payload."


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
