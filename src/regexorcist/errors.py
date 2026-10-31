"""Friendly (and slightly dramatic) error handling."""
from __future__ import annotations

import re


class RegexorcistError(ValueError):
    """Raised when a pattern is too cursed to compile."""


_HINTS = (
    ("missing )", "Unclosed parenthesis. Your pattern is possessed."),
    ("unbalanced parenthesis", "Unbalanced parenthesis: a closing one showed up with no partner."),
    ("unterminated character set", "Unclosed [ ]. The character set is trapped between dimensions."),
    ("bad escape", "Bad escape. Too many backslashes? Even the devil would escape."),
    ("nothing to repeat", "Nothing to repeat. You can't multiply the void."),
    ("multiple repeat", "Multiple repeat. One quantifier per demon, please."),
    ("bad character range", "Bad character range. The alphabet does not work that way."),
)


def translate(exc: re.error) -> RegexorcistError:
    """Turn a boring re.error into a RegexorcistError with a flair."""
    msg = str(exc.msg).lower()
    for needle, hint in _HINTS:
        if needle in msg:
            return RegexorcistError(f"{hint} (position {exc.pos})")
    return RegexorcistError(f"Your pattern is cursed: {exc.msg} (position {exc.pos})")
