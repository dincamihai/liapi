import os
import loadimpact
from apiwrapper.scriptcreator import LoadScriptGenerator
from apiwrapper.extractor import Extractor


class APIWrapper(object):

    def __init__(self, jmx_file_path):
        TOKEN = os.environ.get('LOAD_IMPACT_TOKEN', '')
        self.data = Extractor(jmx_file_path).data
        self.client = loadimpact.ApiTokenClient(api_token=TOKEN)

    def create_scenario(self):
        return self.client.create_user_scenario(
            dict(
                load_script=LoadScriptGenerator(
                    self.data['domain'], self.data['targets']
                ).script,
                name="test_scenario"
            )
        )

    def create_test_config(self):
        scenario = self.create_scenario()
        return self.client.create_test_config(
            {
                'name': self.data['test_plan_name'],
                'url': 'http://%s/' % self.data['domain'],
                'config': {
                    "user_type": "sbu",
                    "load_schedule": [{"users": 10, "duration": 10}],
                    "tracks": [{
                        "clips": [{
                            "user_scenario_id": scenario.id,
                            "percent": 100
                        }],
                        "loadzone": loadimpact.LoadZone.AMAZON_US_ASHBURN
                    }]
                }
            }
        )
