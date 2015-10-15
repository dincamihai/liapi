import pytest
from jmxextractor.extractor import Extractor


@pytest.fixture
def root():
    with open('tests/sample.jmx', 'rb') as jmx:
        tree = etree.parse(jmx)
        return tree.getroot()


@pytest.fixture
def extractor():
    return Extractor('tests/sample.jmx')


def test_extract_test_plan_name(extractor):
    assert extractor.data['test_plan_name'] == 'My test plan'


def test_extract_num_threads(extractor):
    assert extractor.data['num_threads'] == 50


def test_extract_ramp_time(extractor):
    assert extractor.data['ramp_time'] == 60


def test_extract_domain(extractor):
    assert extractor.data['domain'] == 'test.loadimpact.com'


def test_extract_concurrent_pool(extractor):
    assert extractor.data['concurrent_pool'] == 4


def test_extract_urls_paths(extractor):
    expected = ['/', '/news.php', '/', '/flip_coin.php', '/flip_coin.php']
    assert [url['path'] for url in extractor.data['targets']] == expected


def test_extract_urls_methods(extractor):
    expected = 5 * ['GET']
    assert [url['method'] for url in extractor.data['targets']] == expected


def test_extract_targets_arguments(extractor):
    expected = [None, None, None, None, {'bet': 'heads'}]
    assert [url.get('arguments', None) for url in extractor.data['targets']] == expected
