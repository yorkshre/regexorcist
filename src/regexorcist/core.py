"""The actual rituals."""
from __future__ import annotations

import re
from typing import Callable, Iterator, List, Union

from .errors import translate

Replacement = Union[str, Callable[[re.Match], str]]


def _compile(pattern: Union[str, re.Pattern], flags: int = 0) -> re.Pattern:
    if isinstance(pattern, re.Pattern):
        return pattern
    try:
        return re.compile(pattern, flags)
    except re.error as exc:
        raise translate(exc) from exc


class Demons:
    """The matches found in a text. Immutable: rituals return new strings."""

    def __init__(self, pattern: re.Pattern, text: str) -> None:
        self.pattern = pattern
        self.text = text
        self.matches: List[re.Match] = list(pattern.finditer(text))

    def __iter__(self) -> Iterator[re.Match]:
        return iter(self.matches)

    def __len__(self) -> int:
        return len(self.matches)

    def __bool__(self) -> bool:
        return bool(self.matches)

    def __repr__(self) -> str:
        return f"<Demons x{len(self)} for {self.pattern.pattern!r}>"

    def count(self) -> int:
        return len(self.matches)

    def first(self):
        """The first demon, or None if the text is clean."""
        return self.matches[0] if self.matches else None

    def texts(self) -> List[str]:
        return [m.group(0) for m in self.matches]

    def spans(self):
        return [m.span() for m in self.matches]

    def exorcise(self) -> str:
        """Return the text with every demon removed."""
        return self.pattern.sub("", self.text)

    def baptize(self, replacement: Replacement) -> str:
        """Return the text with every demon replaced (string or function)."""
        return self.pattern.sub(replacement, self.text)

    def confess(self) -> str:
        """A human-readable report of what was found."""
        if not self.matches:
            return "No demons found. This text is clean. Go in peace."
        noun = "demon" if len(self) == 1 else "demons"
        lines = [f"Found {len(self)} {noun}:"]
        for i, m in enumerate(self.matches, 1):
            start, end = m.span()
            lines.append(f"  {i}. {m.group(0)!r} at {start}-{end}")
        return "\n".join(lines)


def find(pattern: Union[str, re.Pattern], text: str, flags: int = 0) -> Demons:
    """Hunt for demons (matches) in the text."""
    return Demons(_compile(pattern, flags), text)


def is_possessed(pattern: Union[str, re.Pattern], text: str, flags: int = 0) -> bool:
    """True if the text contains at least one match."""
    return _compile(pattern, flags).search(text) is not None


def exorcise(pattern: Union[str, re.Pattern], text: str, flags: int = 0) -> str:
    """Shortcut: remove all matches."""
    return find(pattern, text, flags).exorcise()


def baptize(pattern: Union[str, re.Pattern], text: str, replacement: Replacement, flags: int = 0) -> str:
    """Shortcut: replace all matches."""
    return find(pattern, text, flags).baptize(replacement)
