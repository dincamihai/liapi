import urllib
from liapi.extractor import Extractor


class LoadScriptGenerator(object):

    def __init__(self, jmx_file_path):
        self.data = Extractor(jmx_file_path).data
        self.script = self.get_script()

    def _get_batch_item(self, item_data):
        query_string = ''
        scheme = 'http'
        if item_data.get('arguments', None):
            query_string = "?%s" % urllib.urlencode(item_data['arguments'])
        return (
            '{{'
                '"{method}", "{scheme}://{domain}{path}{query_string}"'
            '}}'
        ).format(
            scheme=scheme,
            domain=self.data['domain'],
            method=item_data['method'],
            path=item_data['path'],
            query_string=query_string
        )

    def get_script(self):
        script_pattern = (
            'http.request_batch({'
                '{{content}}'
            '})'
        )
        content_items = []
        for idx, it in enumerate(self.data['targets']):
            content_items.append(self._get_batch_item(it))
        content = ','.join(content_items)
        return script_pattern.format(content=content)
