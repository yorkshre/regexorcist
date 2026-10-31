"""Blessed, ready-to-use patterns. Good enough for everyday exorcisms,
not for validating things that RFCs have opinions about."""

EMAIL = r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+"
URL = r"https?://[^\s<>\"']+"
IPV4 = r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b"
HEX_COLOR = r"#(?:[0-9a-fA-F]{3}){1,2}\b"
HASHTAG = r"#\w+"
PHONE = r"\+?\d[\d\s().-]{6,}\d"
