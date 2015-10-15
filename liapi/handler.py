import os
import loadimpact
from liapi.scriptcreator import LoadScriptGenerator


class Handler(object):

    def __init__(self, jmx_file_path):
        self.client = self.get_client()
        self.jmx_file_path = jmx_file_path
        self.script = LoadScriptGenerator(self.jmx_file_path).script
        self.scenario = self.load_scenario()

    def get_client(self):
        TOKEN = os.environ.get('LOAD_IMPACT_TOKEN', '')
        return loadimpact.ApiTokenClient(api_token=TOKEN)

    def load_scenario(self):
        return self.client.create_user_scenario(
            dict(
                load_script=self.script,
                name="test_scenario",
            )
        )

    def create_test_config(self):
        return self.client.create_test_config(
            {
                'name': 'My test configuration',
                'url': 'http://example.com/',
                'config': {
                    "user_type": "sbu",
                    "load_schedule": [{"users": 10, "duration": 10}],
                    "tracks": [{
                        "clips": [{
                            "user_scenario_id": self.scenario.id,
                            "percent": 100
                        }],
                        "loadzone": loadimpact.LoadZone.AMAZON_US_ASHBURN
                    }]
                }
            }
        )
