import mock
from liapi.handler import APIWrapper


def test_load_scenario(handler):
    assert handler.scenario.id == 82431


def test_test_config(handler, create_config_response):
    with create_config_response:
        config = handler.create_test_config()


def test_init_handler_with_file():
    with mock.patch('liapi.handler.loadimpact.ApiTokenClient') as mock_ApiTokenClient:
        mock_client = mock.Mock()
        mock_ApiTokenClient.return_value = mock_client
        handler = APIWrapper('tests/sample.jmx')
        expected='{"GET", "http://test.loadimpact.com/"}'
        value = mock_client.create_user_scenario.call_args[0][0]['load_script']
        assert expected in value
