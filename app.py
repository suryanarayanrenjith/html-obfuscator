from __future__ import annotations

import io
import os
import datetime

from flask import Flask, render_template, request, send_file, abort
from werkzeug.utils import secure_filename

from obfuscate import obfuscate        

app = Flask(__name__, static_url_path="/static")


@app.get("/")
def home():
    """Render the one-page upload interface."""
    return render_template("index.html")

@app.post("/api/obfuscate")
def obfuscate_endpoint():
    """Accept one HTML file and return the obfuscated version."""
    if "file" not in request.files:
        abort(400, "Multipart form must include a field named 'file'")

    infile = request.files["file"]
    raw_html = infile.read().decode("utf-8", "ignore")

    result_html = obfuscate(raw_html)

    name_root = os.path.splitext(secure_filename(infile.filename) or "page")[0]
    ts = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
    download_name = f"{name_root}.obf.{ts}.html"

    return send_file(
        io.BytesIO(result_html.encode()),
        mimetype="text/html",
        as_attachment=True,
        download_name=download_name,
    )


if __name__ == "__main__":
    app.run(debug=True)