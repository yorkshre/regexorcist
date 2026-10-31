"""regexorcist: regular expressions, but with an exorcist.

The power of Python compels you!
"""
from . import holy_water
from .core import Demons, baptize, exorcise, find, is_possessed
from .errors import RegexorcistError

__all__ = [
    "Demons",
    "RegexorcistError",
    "baptize",
    "exorcise",
    "find",
    "holy_water",
    "is_possessed",
]
__version__ = "0.1.0"
