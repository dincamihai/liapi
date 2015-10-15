from liapi.scriptcreator import LoadScriptGenerator


def test_creator_generates_request_batch(data):
    generator = LoadScriptGenerator(**data)
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
