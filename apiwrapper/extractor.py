from lxml import etree
from apiwrapper import exceptions


class Extractor(object):

    XPATHS=dict(
        TEST_PLAN_NAME="hashTree/TestPlan",
        NUM_THREADS="hashTree/hashTree/ThreadGroup/stringProp[@name='ThreadGroup.num_threads']",
        RAMP_TIME="hashTree/hashTree/ThreadGroup/stringProp[@name='ThreadGroup.ramp_time']",
        DOMAIN="hashTree/hashTree/hashTree/ConfigTestElement/stringProp[@name='HTTPSampler.domain']",
        CONCURENT_POOL="hashTree/hashTree/hashTree/ConfigTestElement/stringProp[@name='HTTPSampler.concurrentPool']",
        URLS="hashTree/hashTree/hashTree/hashTree/HTTPSamplerProxy",
        URLS_PATH="./stringProp[@name='HTTPSampler.path']",
        URLS_METHOD="./stringProp[@name='HTTPSampler.method']",
        URLS_ARGUMENTS="./elementProp[@name='HTTPsampler.Arguments']/collectionProp/elementProp",
        URLS_ARGUMENTS_NAME="./stringProp[@name='Argument.name']",
        URLS_ARGUMENTS_VALUE="./stringProp[@name='Argument.value']"
    )

    def __init__(self, jmx_path):
        with open(jmx_path, 'rb') as jmx:
            self.tree = etree.parse(jmx)
            self.root = self.tree.getroot()
            self.data = self.get_data()

    def _extract(self, key, source):
        assert key in self.XPATHS, exceptions.InvalidKeyException('')
        node = self.root.find(self.XPATHS[key])
        if node is None:
            raise exceptions.ExtractionException('Unable to extract %s' % key)
        else:
            if source['type'] == 'attribute':
                return node.get(source['attribute_name'])
            elif source['type'] == 'text':
                out = node.text
                if source['cast'] == 'int':
                    try:
                        out = int(node.text)
                    except:
                        raise exceptions.CastException('Unable to cast %s to %s' % (key, source['cast']))
                return out

    def get_data(self):
        return dict(
            test_plan_name=self._extract(
                'TEST_PLAN_NAME',
                source={'type': 'attribute', 'attribute_name': 'testname'}
            ),
            num_threads=self._extract(
                'NUM_THREADS',
                source={'type': 'text', 'cast': 'int'}
            ),
            ramp_time=int(
                self.root.find(self.XPATHS['RAMP_TIME']).text),
            domain=self.root.find(self.XPATHS['DOMAIN']).text,
            concurrent_pool=int(
                self.root.find(self.XPATHS['CONCURENT_POOL']).text),
            targets=self.get_targets()
        )

    def get_targets(self):
        urls = []
        for node in self.root.findall(self.XPATHS['URLS']):
            arguments = dict()
            node_dict = dict(
                path=node.find(self.XPATHS['URLS_PATH']).text,
                method=node.find(self.XPATHS['URLS_METHOD']).text
            )
            for arg_node in node.findall(self.XPATHS['URLS_ARGUMENTS']):
                name = arg_node.find(self.XPATHS['URLS_ARGUMENTS_NAME']).text
                value = arg_node.find(self.XPATHS['URLS_ARGUMENTS_VALUE']).text
                arguments[name] = value
            if arguments:
                node_dict['arguments'] = arguments
            urls.append(node_dict)
        return urls
