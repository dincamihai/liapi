from lxml import etree
from apiwrapper import exceptions


class Extractor(object):

    XPATHS = dict(
        URLS="hashTree/hashTree/hashTree/hashTree/HTTPSamplerProxy",
        URLS_PATH="./stringProp[@name='HTTPSampler.path']",
        URLS_METHOD="./stringProp[@name='HTTPSampler.method']",
        URLS_ARGUMENTS="./elementProp[@name='HTTPsampler.Arguments']/collectionProp/elementProp",
        URLS_ARGUMENTS_NAME="./stringProp[@name='Argument.name']",
        URLS_ARGUMENTS_VALUE="./stringProp[@name='Argument.value']"
    )

    CONFIG = [
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
        )
    ]

    def __init__(self, jmx_path):
        with open(jmx_path, 'rb') as jmx:
            self.tree = etree.parse(jmx)
            self.root = self.tree.getroot()
            self.data = self.get_data()

    def _extract(self, data):
        source = data['source']
        value = None
        node = self.root.find(data['path'])
        if node is None:
            raise exceptions.ExtractionException('Unable to extract %s' % data['key'])
        else:
            if source['type'] == 'attribute':
                value = node.get(source['attribute_name'])
            elif source['type'] == 'text':
                value = node.text
                if source.get('cast') == 'int':
                    try:
                        value = int(node.text)
                    except:
                        raise exceptions.CastException('Unable to cast %s to %s' % (data['key'], source['cast']))
        return {data['key']: value}

    def get_data(self):
        data = dict()
        for item in self.CONFIG:
            extracted = self._extract(item)
            data.update(extracted)
        data['targets'] = self.get_targets()
        return data

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
