# regexorcist

> Regular expressions, but with an exorcist.
> *The power of Python compels you!*

Find, banish and cleanse text patterns with a friendlier API on top of Python's `re`.
Your patterns are still regular expressions. They just have a priest now.

## Install

```bash
pip install regexorcist
```

## Usage

```python
import regexorcist

text = "Call 555-1234 or 555-9876 for a free demon inspection."

demons = regexorcist.find(r"\d{3}-\d{4}", text)

demons.count()            # 2
demons.texts()            # ['555-1234', '555-9876']
demons.exorcise()         # 'Call  or  for a free demon inspection.'
demons.baptize("[PHONE]") # 'Call [PHONE] or [PHONE] for a free demon inspection.'
print(demons.confess())
# Found 2 demons:
#   1. '555-1234' at 5-13
#   2. '555-9876' at 17-25
```

One-liners:

```python
regexorcist.is_possessed(r"demon", text)        # True
regexorcist.exorcise(r"\d{3}-\d{4}", text)
regexorcist.baptize(r"\d{3}-\d{4}", text, "#")
```

### Holy water (ready-made patterns)

```python
from regexorcist import holy_water

regexorcist.find(holy_water.EMAIL, "write to a@b.com").texts()
```

Available: `EMAIL`, `URL`, `IPV4`, `HEX_COLOR`, `HASHTAG`, `PHONE`.

### Errors with personality

```python
regexorcist.find(r"(abc", "text")
# RegexorcistError: Unclosed parenthesis. Your pattern is possessed. (position 0)
```

`RegexorcistError` is a `ValueError`, so existing error handling keeps working.

## API

| regexorcist | standard `re` equivalent |
|---|---|
| `find()` | `re.finditer()` |
| `Demons.exorcise()` | `re.sub(pattern, "", text)` |
| `Demons.baptize(x)` | `re.sub(pattern, x, text)` |
| `is_possessed()` | `re.search() is not None` |

## Development

```bash
pip install -e . pytest
pytest
```

## License

MIT
