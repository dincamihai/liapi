from lxml import etree


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
        with open('tests/sample.jmx', 'rb') as jmx:
            self.tree = etree.parse(jmx)
            self.root = self.tree.getroot()
            self.data = self.get_data()

    def get_data(self):
        return dict(
            test_plan_name= self.root.find(
                self.XPATHS['TEST_PLAN_NAME']).get('testname'),
            num_threads = int(
                self.root.find(self.XPATHS['NUM_THREADS']).text),
            ramp_time = int(
                self.root.find(self.XPATHS['RAMP_TIME']).text),
            domain = self.root.find(self.XPATHS['DOMAIN']).text,
            concurrent_pool = int(
                self.root.find(self.XPATHS['CONCURENT_POOL']).text),
            targets = self.get_targets()
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
