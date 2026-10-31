# regexorcist tutorial

A step-by-step guide to hunting down and banishing text patterns with
`regexorcist`. No exorcism experience required. If you know a little Python
and a little regex, you are overqualified.

> Under the hood everything is plain Python `re`. Your regular expressions work
> exactly as before. `regexorcist` only gives them a nicer, friendlier API.

## Contents

1. [Installation](#1-installation)
2. [Your first exorcism](#2-your-first-exorcism)
3. [Meet the Demons](#3-meet-the-demons)
4. [Banishing and baptizing](#4-banishing-and-baptizing)
5. [One-liners](#5-one-liners)
6. [Flags and compiled patterns](#6-flags-and-compiled-patterns)
7. [Holy water: ready-made patterns](#7-holy-water-ready-made-patterns)
8. [Errors with personality](#8-errors-with-personality)
9. [Recipes](#9-recipes)
10. [Cheat sheet](#10-cheat-sheet)

---

## 1. Installation

```bash
pip install regexorcist
```

Requires Python 3.9 or newer. There are no dependencies.

## 2. Your first exorcism

```python
import regexorcist

text = "Call 555-1234 or 555-9876 for a free demon inspection."

demons = regexorcist.find(r"\d{3}-\d{4}", text)

print(demons.count())     # 2
print(demons.texts())     # ['555-1234', '555-9876']
print(demons.exorcise())  # Call  or  for a free demon inspection.
```

Three ideas to remember:

- **demon** = one match of your pattern in the text
- **`find()`** hunts for demons and returns a `Demons` object
- **rituals** (`exorcise`, `baptize`) never change the original text, they
  return a new string

## 3. Meet the Demons

`find()` always returns a `Demons` object, even when nothing is found.

```python
demons = regexorcist.find(r"\d{3}-\d{4}", text)

len(demons)       # 2, same as demons.count()
bool(demons)      # True if at least one demon was found
demons.texts()    # ['555-1234', '555-9876']
demons.spans()    # [(5, 13), (17, 25)]  start and end of each match
demons.first()    # the first match object, or None if the text is clean
```

Each demon is a standard `re.Match`, so everything you know still works:

```python
for demon in demons:
    print(demon.start(), demon.group())
# 5 555-1234
# 17 555-9876
```

Named groups work too:

```python
m = regexorcist.find(r"(?P<area>\d{3})-(?P<num>\d{4})", text).first()
m.group("area")   # '555'
m.groupdict()     # {'area': '555', 'num': '1234'}
```

### Confession

`confess()` returns a readable report of what was found:

```python
print(demons.confess())
# Found 2 demons:
#   1. '555-1234' at 5-13
#   2. '555-9876' at 17-25
```

On a clean text you get: `No demons found. This text is clean. Go in peace.`

## 4. Banishing and baptizing

**`exorcise()`** removes every demon:

```python
demons.exorcise()
# 'Call  or  for a free demon inspection.'
```

**`baptize(replacement)`** replaces every demon with something else:

```python
demons.baptize("[PHONE]")
# 'Call [PHONE] or [PHONE] for a free demon inspection.'
```

`baptize` also accepts a function that receives the match and returns the
replacement:

```python
regexorcist.find(r"\d+", "I have 3 cats and 12 fish").baptize(
    lambda m: str(int(m.group()) * 2)
)
# 'I have 6 cats and 24 fish'
```

## 5. One-liners

When you only need a quick answer, skip the `Demons` object:

```python
regexorcist.is_possessed(r"demon", text)           # True or False
regexorcist.exorcise(r"\s+", "too    many   spaces")
# 'toomanyspaces'
regexorcist.baptize(r"\s+", "too    many   spaces", " ")
# 'too many spaces'
```

## 6. Flags and compiled patterns

Pass flags as the last argument, exactly like in `re`:

```python
import re

regexorcist.is_possessed("DEMON", text)           # False
regexorcist.is_possessed("DEMON", text, re.I)     # True

regexorcist.find("demon", "Demon DEMON demon", re.I).texts()
# ['Demon', 'DEMON', 'demon']
```

Patterns you already compiled with `re.compile()` work as well:

```python
pattern = re.compile(r"\d+")
regexorcist.find(pattern, "a1b22").texts()   # ['1', '22']
```

## 7. Holy water: ready-made patterns

For common jobs there are blessed patterns in `regexorcist.holy_water`:

| Name | Finds |
|---|---|
| `EMAIL` | e-mail addresses |
| `URL` | `http://` and `https://` links |
| `IPV4` | IPv4 addresses (rejects `999.9.9.9`) |
| `HEX_COLOR` | CSS colors like `#fff` or `#1a2b3c` |
| `HASHTAG` | `#hashtags` |
| `PHONE` | phone numbers (international and with parentheses) |

```python
from regexorcist import holy_water

regexorcist.find(holy_water.IPV4, "from 10.0.0.1 to 192.168.1.20 via 999.9.9.9").texts()
# ['10.0.0.1', '192.168.1.20']

regexorcist.find(holy_water.HEX_COLOR, "body{color:#fff;background:#1a2b3c}").texts()
# ['#fff', '#1a2b3c']
```

These patterns are fine for everyday cleaning and searching. They are **not**
strict validators: e-mail and phone formats are full of exceptions, so do not
use them to decide whether an address is "officially valid".

## 8. Errors with personality

A broken pattern raises `RegexorcistError`, with a message that tells you
what went wrong and where:

```python
from regexorcist import RegexorcistError

try:
    regexorcist.find(r"(abc", "some text")
except RegexorcistError as e:
    print(e)
# Unclosed parenthesis. Your pattern is possessed. (position 0)
```

`RegexorcistError` is a subclass of `ValueError`, so existing
`except ValueError:` handlers keep working.

Some messages you may meet:

| Mistake | Message |
|---|---|
| `(abc` | Unclosed parenthesis. Your pattern is possessed. |
| `abc)` | Unbalanced parenthesis: a closing one showed up with no partner. |
| `[abc` | Unclosed [ ]. The character set is trapped between dimensions. |
| `\q` | Bad escape. Too many backslashes? Even the devil would escape. |
| `*abc` | Nothing to repeat. You can't multiply the void. |
| `a**` | Multiple repeat. One quantifier per demon, please. |

## 9. Recipes

### Mask e-mail addresses in logs

```python
log = "user a@b.com logged in, then c.d@example.org logged out"
regexorcist.baptize(holy_water.EMAIL, log, "[email]")
# 'user [email] logged in, then [email] logged out'
```

### Collect hashtags

```python
regexorcist.find(holy_water.HASHTAG, "Loving #python and #regex today! #exorcism").texts()
# ['#python', '#regex', '#exorcism']
```

### Extract links from a text

```python
regexorcist.find(
    holy_water.URL,
    "docs: https://pypi.org/project/regexorcist/ and http://example.com",
).texts()
# ['https://pypi.org/project/regexorcist/', 'http://example.com']
```

### Normalize whitespace

```python
regexorcist.baptize(r"\s+", "too    many   spaces", " ")
# 'too many spaces'
```

### Strip simple HTML tags

```python
regexorcist.exorcise(r"<[^>]+>", "<p>Hello <b>world</b></p>")
# 'Hello world'
```

(For real-world HTML use a proper parser. This is fine for quick cleanups.)

### Check a file for sensitive data

```python
from pathlib import Path

for number, line in enumerate(Path("app.log").read_text().splitlines(), 1):
    demons = regexorcist.find(holy_water.EMAIL, line)
    if demons:
        print(f"line {number}: {demons.texts()}")
```

## 10. Cheat sheet

| I want to... | regexorcist | plain `re` |
|---|---|---|
| find all matches | `find(p, text)` | `re.finditer(p, text)` |
| count matches | `find(p, text).count()` | `len(re.findall(p, text))` |
| list matched strings | `find(p, text).texts()` | `re.findall(p, text)` |
| check if anything matches | `is_possessed(p, text)` | `re.search(p, text) is not None` |
| delete matches | `exorcise(p, text)` | `re.sub(p, "", text)` |
| replace matches | `baptize(p, text, new)` | `re.sub(p, new, text)` |
| print a report | `find(p, text).confess()` | write a loop |

Found a bug or have an idea for a new ritual? Open an issue in the repository.

*The power of Python compels you!*
