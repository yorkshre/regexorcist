import re

import pytest

import regexorcist
from regexorcist import RegexorcistError, holy_water

TEXT = "Call 555-1234 or 555-9876 for a free demon inspection."
PHONE = r"\d{3}-\d{4}"


def test_find_counts_and_texts():
    demons = regexorcist.find(PHONE, TEXT)
    assert demons.count() == 2 == len(demons)
    assert demons.texts() == ["555-1234", "555-9876"]
    assert demons.first().group(0) == "555-1234"
    assert demons.spans() == [(5, 13), (17, 25)]
    assert demons


def test_exorcise_and_baptize():
    demons = regexorcist.find(PHONE, TEXT)
    assert demons.exorcise() == "Call  or  for a free demon inspection."
    assert demons.baptize("[PHONE]") == "Call [PHONE] or [PHONE] for a free demon inspection."
    assert demons.baptize(lambda m: m.group(0)[:3] + "-XXXX").count("XXXX") == 2


def test_text_is_never_mutated():
    demons = regexorcist.find(PHONE, TEXT)
    demons.exorcise()
    assert demons.text == TEXT


def test_clean_text():
    demons = regexorcist.find(PHONE, "Nothing to see here")
    assert not demons
    assert demons.first() is None
    assert "clean" in demons.confess()


def test_confess_report():
    report = regexorcist.find(PHONE, TEXT).confess()
    assert report.startswith("Found 2 demons:")
    assert "'555-1234' at 5-13" in report
    assert regexorcist.find(PHONE, "x 555-1234").confess().startswith("Found 1 demon:")


def test_shortcuts_and_flags():
    assert regexorcist.is_possessed("DEMON", TEXT, re.I)
    assert not regexorcist.is_possessed("angel", TEXT)
    assert regexorcist.exorcise(PHONE, "a 555-1234 b") == "a  b"
    assert regexorcist.baptize(PHONE, "a 555-1234 b", "#") == "a # b"


def test_accepts_compiled_pattern():
    assert regexorcist.find(re.compile(PHONE), TEXT).count() == 2


@pytest.mark.parametrize(
    "bad, fragment",
    [
        (r"(abc", "Unclosed parenthesis"),
        (r"abc)", "Unbalanced parenthesis"),
        (r"[abc", "Unclosed [ ]"),
        (r"\q", "Bad escape"),
        (r"*abc", "Nothing to repeat"),
        (r"a**", "Multiple repeat"),
    ],
)
def test_dramatic_errors(bad, fragment):
    with pytest.raises(RegexorcistError, match=re.escape(fragment)):
        regexorcist.find(bad, TEXT)


def test_error_is_a_valueerror():
    assert issubclass(RegexorcistError, ValueError)


def test_holy_water():
    assert regexorcist.find(holy_water.EMAIL, "mail me: a.b+c@example.co.uk!").texts() == ["a.b+c@example.co.uk"]
    assert regexorcist.find(holy_water.IPV4, "ip 192.168.0.1 and 999.1.1.1").texts() == ["192.168.0.1"]
    assert regexorcist.find(holy_water.URL, "see https://pypi.org/project/x now").texts() == ["https://pypi.org/project/x"]
    assert regexorcist.find(holy_water.HEX_COLOR, "color #ff00aa and #abc").texts() == ["#ff00aa", "#abc"]
