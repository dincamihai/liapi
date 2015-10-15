import os
import pytest
import json
import requests
import responses


TOKEN = os.environ.get('LOAD_IMPACT_TOKEN', '')


@pytest.fixture
def load_scenario_response():
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


def test_load_scenario(load_scenario_response):
    with responses.RequestsMock() as rsps:
        rsps.add(**load_scenario_response)
        resp = requests.post(
            url='https://api.loadimpact.com/v2/user-scenarios',
            auth=(TOKEN, ''),
            data=dict(
                load_script="I am a string",
                name="test_scenario",
                data_stores=[1]
            ),
            headers={'Content-Type': 'application/json'}
        )
