import os
import json
import loadimpact
import requests
from apiwrapper.scriptcreator import LoadScriptGenerator
from apiwrapper.extractor import Extractor


class JMXHandler(object):

    def __init__(self, jmx_file_path):
        self.token = os.environ.get('LOAD_IMPACT_TOKEN', '')
        with open('apiwrapper/config.json', 'rb') as config_file:
            self.data = Extractor(jmx_file_path, json.load(config_file)).data
        self.client = loadimpact.ApiTokenClient(api_token=self.token)

    def create_scenario(self):
        resp = requests.post(
            'https://api.loadimpact.com/v2/user-scenarios',
            data=dict(
                load_script=LoadScriptGenerator(
                    self.data['domain'], self.data['targets']
                ).script,
                name="test_scenario"
            ),
            headers={
                "Content-Type": "application/json"
            },
            auth=(self.token, '')
        )
        return resp.json()['id']

    def create_test_config(self, scenario_id):
        return self.client.create_test_config(
            {
                'name': self.data['test_plan_name'],
                'url': 'http://%s/' % self.data['domain'],
                'config': {
                    "user_type": "sbu",
                    "load_schedule": [{"users": 10, "duration": 10}],
                    "tracks": [{
                        "clips": [{
                            "user_scenario_id": scenario_id,
                            "percent": 100
                        }],
                        "loadzone": loadimpact.LoadZone.AMAZON_US_ASHBURN
                    }]
                }
            }
        )
