import urllib


class LoadScriptGenerator(object):

    def __init__(self, domain, targets):
        self.domain = domain
        self.targets = targets
        self.script = self._get_script()

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
            domain=self.domain,
            method=item_data['method'],
            path=item_data['path'],
            query_string=query_string
        )

    def _get_script(self):
        script_pattern = (
            'http.request_batch({'
                '{{content}}'
            '})'
        )
        content_items = []
        for idx, it in enumerate(self.targets):
            content_items.append(self._get_batch_item(it))
        content = ','.join(content_items)
        return script_pattern.format(content=content)
