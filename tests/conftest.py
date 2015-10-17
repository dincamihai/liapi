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


@pytest.fixture
def single_argument_config():
    return [
        {
            "path": "stringProp[@name='Argument.name']",
            "key": 'name',
            "source": {'type': 'text'}
        },
        {
            "path": "stringProp[@name='Argument.value']",
            "key": 'value',
            "source": {'type': 'text'}
        }
    ]

@pytest.fixture
def arguments_config(single_argument_config):
    return [
        {
            "path": "elementProp[@name='HTTPsampler.Arguments']/collectionProp/elementProp",
            "key": "arguments",
            "many": True,
            "config": single_argument_config
        }
    ]


@pytest.fixture
def single_target_config(single_argument_config):
    return [
        {
            "path": "stringProp[@name='HTTPSampler.path']",
            "key": "path",
            "source": {'type': 'text'}
        },
        {
            "path": "stringProp[@name='HTTPSampler.method']",
            "key": 'method',
            "source": {'type': 'text'}
        },
        {
            "path": "elementProp[@name='HTTPsampler.Arguments']/collectionProp/elementProp",
            "key": "arguments",
            "many": True,
            "config": single_argument_config
        }
    ]


@pytest.fixture
def targets_config(single_target_config):
    return [
        {
            "path": "hashTree/hashTree/hashTree/hashTree/HTTPSamplerProxy",
            "key": "targets",
            "many": True,
            "config": single_target_config
        }
    ]


@pytest.fixture
def config(single_target_config):
    return [
        dict(
            path="hashTree/TestPlan",
            key='test_plan_name',
            source={'type': 'attribute', 'attribute_name': 'testname'}
        ),
        dict(
            path="hashTree/hashTree/ThreadGroup/stringProp[@name='ThreadGroup.num_threads']",
            key='num_threads',
            source={'type': 'text', 'cast': 'int'}
        ),
        dict(
            path="hashTree/hashTree/ThreadGroup/stringProp[@name='ThreadGroup.ramp_time']",
            key='ramp_time',
            source={'type': 'text', 'cast': 'int'}
        ),
        dict(
            path="hashTree/hashTree/hashTree/ConfigTestElement/stringProp[@name='HTTPSampler.domain']",
            key='domain',
            source={'type': 'text'}
        ),
        dict(
            path="hashTree/hashTree/hashTree/ConfigTestElement/stringProp[@name='HTTPSampler.concurrentPool']",
            key='concurrent_pool',
            source={'type': 'text', 'cast': 'int'}
        ),
        {
            "path": "hashTree/hashTree/hashTree/hashTree/HTTPSamplerProxy",
            "key": "targets",
            "many": True,
            "config": single_target_config
        }
    ]


@pytest.fixture
def config_mapping(config):
    return dict(zip(
        [
            'test_plan_name_config',
            'num_threads_config',
            'ramp_time_config',
            'domain_config',
            'concurrent_pool_config',
            'targets_config'
        ],
        [[it] for it in config]
    ))
