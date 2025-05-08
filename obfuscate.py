from __future__ import annotations

import base64
import re
from urllib.parse import quote, unquote

_BEGIN = (
    "<!DOCTYPE html>\n"
    "<script type=\"text/javascript\">\n"
    "document.write(decodeURIComponent(atob('"
)
_END = (
    "')));\n"
    "</script>\n"
    "<noscript>You must enable javascript in your browser to view this webpage."
    "</noscript>\n"
)

_PAYLOAD_RE = re.compile(r"atob\('([^']+)'\)", re.S)


def _encode_payload(html: str) -> str:
    """URL-encode **then** Base-64 encode the HTML document."""
    return base64.b64encode(quote(html).encode()).decode()


def _decode_payload(payload: str) -> str:
    """Reverse _encode_payload()."""
    return unquote(base64.b64decode(payload).decode())


def obfuscate(html_text: str, **_ignored) -> str:
    """
    Return a fully obfuscated HTML document.

    Extra kwargs are ignored so the signature stays compatible with the
    earlier, more complex version that Flask called.
    """
    return _BEGIN + _encode_payload(html_text) + _END


def deobfuscate(obfuscated_html: str) -> str:
    """
    Extract and return the original HTML.

    Raises ValueError if the input doesn’t look like something produced by
    `obfuscate()`.
    """
    match = _PAYLOAD_RE.search(obfuscated_html)
    if not match:
        raise ValueError("Input does not appear to be produced by this obfuscator")
    return _decode_payload(match.group(1))

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python obfuscate.py <infile.html> <outfile.html>")
        sys.exit(0)

    infile, outfile = sys.argv[1:3]
    with open(infile, encoding="utf-8") as f_in:
        raw = f_in.read()

    result = obfuscate(raw)
    with open(outfile, "w", encoding="utf-8") as f_out:
        f_out.write(result)

    print(f"Wrote obfuscated file to {outfile}")