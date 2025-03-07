import datetime

import pandas as pd
import pytest

from pywarp10.gts import GTS
from pywarp10.sanitize import SanitizeError, desanitize, sanitize


def test_sanitize():
    object = {
        "string": "foo",
        "numeric": 1,
        "boolean": True,
        "list": [1, 2, 3],
        "dict": {},
        "date_string": "2020-01-01",
        "invalid_token_date_string": "test{}",
        "date_datetime": pd.Timestamp("2020-01-01 12:00:00"),
        "date_timedelta": pd.Timedelta("1d"),
        "date_date": datetime.date(2020, 1, 1),
        "duration": "1h",
        "string_number": "1871",
        "warpscript": "ws:foo",
    }
    result = """{
 'string' 'foo'
 'numeric' 1
 'boolean' TRUE
 'list' [ 1 2 3 ]
 'dict' {}
 'date_string' 1577854800000000
 'invalid_token_date_string' 'test{}'
 'date_datetime' 1577880000000000
 'date_timedelta' 86400000000
 'date_date' 1577836800000000
 'duration' 3600000000
 'string_number' '1871'
 'warpscript' foo
}"""
    assert sanitize(object) == result

    # Test error
    with pytest.raises(SanitizeError):
        sanitize(("foo", "bar"))


def test_desanitize():
    gts = {
        "c": "metric",
        "l": {"foo": "bar"},
        "a": {"foo": "bar"},
        "la": {"foo": "bar"},
        "v": [[1, 2]],
    }
    pd.testing.assert_frame_equal(desanitize(gts), GTS(gts))
    pd.testing.assert_frame_equal(desanitize([gts]), GTS([gts]))
    result = desanitize([1, 2, gts])
    assert result[0:-1] == (1, 2)
    pd.testing.assert_frame_equal(result[-1], GTS(gts))


def test_list_desanitize():
    lgts = [
        {
            "c": "metric_1",
            "l": {"foo": "bar", "toto": "lol"},
            "a": {"foo": "bar"},
            "la": {"foo": "bar"},
            "v": [[1, 2]],
        },
        {
            "c": "metric_1",
            "l": {"foo": "bar", "toto": "lolp"},
            "a": {"foo": "bar"},
            "la": {"foo": "bar"},
            "v": [[0, 6]],
        },
    ]
    results = desanitize(lgts, bind_lgts=True)
    assert results is not None
