import pytest

from src import utils


def test_slugify_basic():
    assert utils.slugify("Hello World!") == "hello-world"


def test_slugify_strips_edges():
    assert utils.slugify("  --foo bar--  ") == "foo-bar"


def test_chunked_exact_split():
    assert list(utils.chunked([1, 2, 3, 4], 2)) == [[1, 2], [3, 4]]


def test_chunked_uneven():
    assert list(utils.chunked([1, 2, 3], 2)) == [[1, 2], [3]]


def test_human_size():
    assert utils.human_size(500) == "500.0 B"
    assert utils.human_size(2048) == "2.0 KB"


def test_retry_gives_up():
    def boom():
        raise ValueError("nope")

    with pytest.raises(ValueError):
        utils.retry(boom, attempts=2, delay=0)
