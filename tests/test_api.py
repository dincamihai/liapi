import mock
from apiwrapper.handler import APIWrapper


def test_load_scenario(handler):
    assert handler.scenario.id == 82431


def test_test_config(handler, create_config_response):
    with create_config_response:
        config = handler.create_test_config()


def test_init_handler_with_file():
    with mock.patch('apiwrapper.handler.loadimpact.ApiTokenClient') as mock_ApiTokenClient:
        mock_client = mock.Mock()
        mock_ApiTokenClient.return_value = mock_client
        handler = APIWrapper('tests/sample.jmx')
        expected='{"GET", "http://test.loadimpact.com/"}'
        value = mock_client.create_user_scenario.call_args[0][0]['load_script']
        assert expected in value


def test_handler_data(load_scenario_response):
    with load_scenario_response:
        handler = APIWrapper('tests/sample.jmx')
    assert handler.data


def test_handler_data(load_scenario_response):
    with load_scenario_response:
        handler = APIWrapper('tests/sample.jmx')
    handler.client = mock.Mock()
    handler.create_test_config()
    assert handler.client.create_test_config.call_args[0][0] == dict(
        {
            'name': handler.data['test_plan_name'],
            'url': 'http://%s/' % handler.data['domain'],
            'config': {
                "user_type": "sbu",
                "load_schedule": [{"users": 10, "duration": 10}],
                "tracks": [{
                    "clips": [{
                        "user_scenario_id": handler.scenario.id,
                        "percent": 100
                    }],
                    "loadzone": 'amazon:us:ashburn'
                }]
            }
        }
    )
