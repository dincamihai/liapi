import pytest
import responses
import json
import os


@pytest.fixture
def targets():
    return [
        {
            'path': '/',
            'method': 'GET'
        },
        {
            'path': '/news.php',
            'method': 'GET'
        },
        {
            'path': '/',
            'method': 'GET'
        },
        {
            'path': '/flip_coin.php',
            'method': 'GET'
        },
        {
            'path': '/flip_coin.php',
            'method': 'GET',
            'arguments': [{'name': 'bet', 'value': 'heads'}]
        }
    ]


@pytest.fixture
def data(targets):
    return {
        "domain": "test.loadimpact.com",
        "targets": targets
    }


@pytest.fixture
def set_LOAD_IMPACT_TOKEN():
    os.environ['LOAD_IMPACT_TOKEN'] = '123fake456'


@pytest.fixture()
def wrapper(set_LOAD_IMPACT_TOKEN):
    from apiwrapper.handler import JMXHandler
    return JMXHandler('tests/sample.jmx')


@pytest.fixture(scope='session')
def activate_responses(request):
    rsps =  responses.RequestsMock()
    rsps.start()
    request.addfinalizer(rsps.stop)


@pytest.fixture(scope='function')
def create_scenario_response(request):
    return dict(
        method=responses.POST,
        url='https://api.loadimpact.com/v2/user-scenarios',
        status=201,
        content_type='application/json',
        body=json.dumps(
            {
                "created": "2015-08-18T10:08:48+00:00",
                "id": 82431,
                "load_script": "I'm a string",
                "name": "Name of resource",
                "script_type": "lua",
                "updated": "2015-08-18T10:08:48+00:00"
            }
        )
    )


@pytest.fixture(scope='function')
def create_config_response(request):
    return dict(
        method=responses.POST,
        url='https://api.loadimpact.com/v2/test-configs',
        body=json.dumps({
            'config': {
                u'new_relic_applications': [],
                u'network_emulation': {
                    u'client': u'li', u'network': u'unlimited'
                },
                u'user_type': u'sbu',
                u'server_metric_agents': [],
                u'tracks': [
                    {
                        u'clips': [
                            {u'user_scenario_id': 3214711, u'percent': 100}
                        ],
                        u'loadzone': u'amazon:us:ashburn'
                    }
                ],
                u'load_schedule': [
                    {u'duration': 10, u'users': 10}
                ],
                u'source_ips': 0
            },
            'created': "2015-08-18T10:08:48+00:00",
            'id': 3204290,
            'name': u'My test configuration',
            'public_url': u'',
            'updated': "2015-08-18T10:08:48+00:00",
            'url': u'http://example.com/'
        }),
        status=201,
        content_type='application/json',
    )
