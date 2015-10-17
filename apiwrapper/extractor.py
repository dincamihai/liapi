from lxml import etree
from apiwrapper import exceptions


class Extractor(object):

    def __init__(self, jmx_path, config):
        with open(jmx_path, 'rb') as jmx:
            self.config = config
            root = etree.parse(jmx).getroot()
            self.data = self.get_data(config, root)

    @classmethod
    def _extract(cls, config_item, parent):
        value = None
        if not config_item.get('many'):
            node = parent.find(config_item['path'])
            value = cls._extract_single(
                config_item['key'], config_item['source'], node
            )
        else:
            value = cls._extract_many(config_item, parent)
        return {config_item['key']: value}

    @classmethod
    def _extract_single(cls, key, source, node):
        value = None
        if node is None:
            raise exceptions.ExtractionException(
                'Unable to extract %s' % key
            )
        else:
            if source.get('type') == 'attribute':
                value = node.get(source['attribute_name'])
            elif source.get('type') == 'text':
                value = node.text
                if source.get('cast') == 'int':
                    try:
                        value = int(node.text)
                    except:
                        raise exceptions.CastException(
                            'Unable to cast %s to %s' % (key, source['cast'])
                        )
        return value

    @classmethod
    def _extract_many(cls, config_item, parent):
        value = []
        for node in parent.findall(config_item['path']):
            value.append(cls.get_data(config_item['config'], node))
        return value

    @classmethod
    def get_data(cls, config, node=None):
        data = dict()
        for config_item in config:
            extracted = cls._extract(config_item, node)
            data.update(extracted)
        return data
