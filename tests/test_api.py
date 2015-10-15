import mock
from liapi.handler import Handler


def test_load_scenario(handler):
    assert handler.scenario.id == 82431


def test_test_config(handler, create_config_response):
    with create_config_response:
        config = handler.create_test_config()


def test_init_handler_with_file():
    with mock.patch.object(Handler, 'get_client') as mock_get_client:
        mock_client = mock.Mock()
        mock_get_client.return_value = mock_client
        handler = Handler('tests/sample.jmx')
        expected=(
            'http.request_batch({{"GET", "http://test.loadimpact.com/"}})'
        )
        value = mock_client.create_user_scenario.call_args[0][0]['load_script']
        assert value == expected
