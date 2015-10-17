import pytest
from lxml import etree
from apiwrapper.extractor import Extractor
from apiwrapper import exceptions


@pytest.fixture
def root():
    with open('tests/sample.jmx', 'rb') as jmx:
        tree = etree.parse(jmx)
        return tree.getroot()


def test_extract_test_plan_name(config_mapping):
    extractor = Extractor(
        'tests/sample.jmx', config_mapping['test_plan_name_config'])
    assert extractor.data['test_plan_name'] == 'My test plan'


def test_extract_num_threads(config_mapping):
    extractor = Extractor(
        'tests/sample.jmx', config_mapping['num_threads_config'])
    assert extractor.data['num_threads'] == 50


def test_extract_ramp_time(config_mapping):
    extractor = Extractor(
        'tests/sample.jmx', config_mapping['ramp_time_config'])
    assert extractor.data['ramp_time'] == 60


def test_extract_domain(config_mapping):
    extractor = Extractor(
        'tests/sample.jmx', config_mapping['domain_config'])
    assert extractor.data['domain'] == 'test.loadimpact.com'


def test_extract_concurrent_pool(config_mapping):
    extractor = Extractor(
        'tests/sample.jmx', config_mapping['concurrent_pool_config'])
    assert extractor.data['concurrent_pool'] == 4


def test_extract_urls_paths(config_mapping):
    extractor = Extractor(
        'tests/sample.jmx', config_mapping['targets_config'])
    expected = ['/', '/news.php', '/', '/flip_coin.php', '/flip_coin.php']
    assert [url['path'] for url in extractor.data['targets']] == expected


def test_extract_urls_methods(config_mapping):
    extractor = Extractor('tests/sample.jmx', config_mapping['targets_config'])
    expected = 5 * ['GET']
    assert [url['method'] for url in extractor.data['targets']] == expected


def test_extract_targets_arguments(config_mapping):
    extractor = Extractor('tests/sample.jmx', config_mapping['targets_config'])
    expected = [[], [], [], [], [{'name': 'bet', 'value': 'heads'}]]
    value = [url.get('arguments', None) for url in extractor.data['targets']]
    assert value == expected


def test_extract_missing_test_plan_name(config_mapping):
    extractor = Extractor(
        'tests/sample_no_test_plan_name.jmx',
        config_mapping['test_plan_name_config'])
    assert extractor.data['test_plan_name'] is None


def test_cast_int_exception(config_mapping):
    with pytest.raises(exceptions.CastException) as exc:
        Extractor(
            'tests/sample_bad_int.jmx', config_mapping['num_threads_config'])
    assert exc.value.message == 'Unable to cast num_threads to int'


def test_extract_missing_TestPlan(config_mapping):
    with pytest.raises(exceptions.ExtractionException) as exc:
        Extractor(
            'tests/sample_no_test_plan_node.jmx',
            config_mapping['test_plan_name_config']
        )
    assert exc.value.message == 'Unable to extract test_plan_name'


def test_extract_invalid_file_path():
    with pytest.raises(IOError):
        Extractor('tests/missing_file.jmx', {})


def test_extract_single_argument(single_argument_config):
    config = single_argument_config
    data = Extractor('tests/argument.jmx', config).data
    assert data == {'name': 'bet', 'value': 'heads'}


def test_extract_arguments_list(arguments_config):
    config = arguments_config
    data = Extractor('tests/arguments.jmx', config).data
    assert data == {
        'arguments': [
            {'name': 'arg1', 'value': 'value1'},
            {'name': 'arg2', 'value': 'value2'}
        ]
    }


def test_extract_targets(targets_config):
    config = targets_config
    data = Extractor('tests/targets.jmx', config).data
    assert data == {
        'targets': [
            {
                'arguments': [
                    {'name': 'arg1', 'value': 'value1'},
                    {'name': 'arg2', 'value': 'value2'}
                ],
                'method': 'GET',
                'path': '/path1'
            },
            {
                'arguments': [],
                'method': 'GET',
                'path': '/path2'
            }
        ]
    }
