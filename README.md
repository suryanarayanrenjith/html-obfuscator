# HTML Obfuscator

A **zero‑config utility** that turns any HTML document into a self‑decoding, Base‑64/URL‑encoded wrapper.  Run it as a

* Web app (Flask)
* Desktop app (single‑click EXE via **pywebview**)

The original HTML never changes – it’s wrapped so casual viewers see only encoded text while browsers render it normally.

---

## Features

| Mode         | How it works                       | Use‑case                   |
| ------------ | ---------------------------------- | -------------------------- |
| **Web UI**   | Flask + Tailwind upload interface  | Share online, team utility |
| **API only** | `POST /api/obfuscate` multipart    | Scriptable CI/CD step      |
| **Desktop**  | Packaged EXE with embedded WebView | Non‑tech users, offline    |

---

## Project layout

```text
html-obfuscator/
├── app.py                # Flask entry‑point (web + API)
├── obfuscate.py          # 15‑line encode/decode core
├── desktop_launcher.py   # Embed Flask in pywebview
├── requirements.txt      # Flask + pywebview
├── templates/
│   └── index.html        # Tailwind upload form
└── static/
    └── ...               # JS / CSS assets
```

---

## Quick start

### Run locally (web interface)

```bash
python -m venv .venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py           
```

Open the URL, upload an HTML file, download `<name>.obf.<timestamp>.html`.

### Use the packaged desktop app

Double‑click **`html‑obfuscator.exe`** and follow the on‑screen prompt to choose an HTML file.

---

## API reference

```
POST /api/obfuscate
Content‑Type: multipart/form‑data

file=<your HTML file>
```

**Response**: raw `text/html` attachment (obfuscated).

---

## Releases

Pre‑built binaries are available on the [**Releases**](https://github.com/suryanarayanrenjith/html-obfuscator/releases) page for Windows:

| File                        | Notes                                                                                                                                                                                                                                                           |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `html‑obfuscator.exe` | Portable single‑file build. **Heads‑up:** Unsigned executables sometimes trigger SmartScreen or antivirus false positives. If this happens you can safely allow / whitelist the file or build your own binary with `pyinstaller --onefile desktop_launcher.py`. |
|                             |                                                                                                                                                                                                                                                                 |

---

## License

MIT – see [LICENSE](https://github.com/suryanarayanrenjith/html-obfuscator/blob/main/LICENSE).

> **Security note**: Obfuscation ≠ encryption. This tool only deters casual copy‑pasting; determined users can always decode the payload.
