import pytest
from liapi.scriptcreator import LoadScriptGenerator


TARGETS = [
    {
        'path': '/',
        'method': 'GET'
    },
    {
        'path': '/news.php',
        'method': 'GET'
    },
    {
        'path': '/',
        'method': 'GET'
    },
    {
        'path': '/flip_coin.php',
        'method': 'GET'
    },
    {
        'path': '/flip_coin.php',
        'method': 'GET',
        'arguments': {'bet': 'heads'}
    }
]


DATA = {
    "domain": "test.loadimpact.com",
    "targets": TARGETS
}


def test_creator_generates_request_batch():
    generator = LoadScriptGenerator(DATA)
    expected = (
        'http.request_batch({'
            '{"GET", "http://test.loadimpact.com/"},'
            '{"GET", "http://test.loadimpact.com/news.php"},'
            '{"GET", "http://test.loadimpact.com/"},'
            '{"GET", "http://test.loadimpact.com/flip_coin.php"},'
            '{"GET", "http://test.loadimpact.com/flip_coin.php?bet=heads"}'
        '})'
    )
    assert generator.script == expected
