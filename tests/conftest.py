import pytest
import responses
import json


@pytest.fixture()
def handler(load_scenario_response):
    from liapi.handler import APIWrapper
    with load_scenario_response:
        return APIWrapper('tests/sample.jmx')


@pytest.fixture(scope='function')
def load_scenario_response(request):
    rsps =  responses.RequestsMock()
    rsps.add(
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
    return rsps


@pytest.fixture(scope='function')
def create_config_response(request):
    rsps =  responses.RequestsMock()
    rsps.add(
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
    return rsps
