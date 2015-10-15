import mock
import responses
from apiwrapper.handler import APIWrapper


def test_load_scenario(wrapper, create_scenario_response):
    with responses.RequestsMock() as rsps:
        rsps.add(**create_scenario_response)
        scenario = wrapper.create_scenario()
    assert scenario.id == 82431


def test_test_config(wrapper, create_scenario_response, create_config_response):
    with responses.RequestsMock() as rsps:
        rsps.add(**create_scenario_response)
        rsps.add(**create_config_response)
        config = wrapper.create_test_config()


def test_wrapper_create_scenario():
    wrapper = APIWrapper('tests/sample.jmx')
    wrapper.client = mock.Mock()
    wrapper.create_scenario()
    expected='{"GET", "http://test.loadimpact.com/"}'
    value = wrapper.client.create_user_scenario.call_args[0][0]['load_script']
    assert expected in value


def test_wrapper_data():
    wrapper = APIWrapper('tests/sample.jmx')
    wrapper.create_scenario()
    assert wrapper.data


def test_wrapper_data():
    wrapper = APIWrapper('tests/sample.jmx')
    wrapper.create_scenario = mock.Mock(**{'return_value.id': 333})
    with responses.RequestsMock() as rsps:
        mock_create_test_config = mock.Mock()
        wrapper.client.create_test_config = mock_create_test_config
        wrapper.create_test_config()
    assert mock_create_test_config.call_args[0][0] == dict(
        {
            'name': wrapper.data['test_plan_name'],
            'url': 'http://%s/' % wrapper.data['domain'],
            'config': {
                "user_type": "sbu",
                "load_schedule": [{"users": 10, "duration": 10}],
                "tracks": [{
                    "clips": [{
                        "user_scenario_id": 333,
                        "percent": 100
                    }],
                    "loadzone": 'amazon:us:ashburn'
                }]
            }
        }
    )
