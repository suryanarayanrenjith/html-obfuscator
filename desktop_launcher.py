from threading import Thread
import time
import webbrowser
import webview
from app import app  

PORT = 5000
URL  = f"http://127.0.0.1:{PORT}/"

def _run_flask():
    app.run(host="127.0.0.1", port=PORT, debug=False, use_reloader=False)

flask_thread = Thread(target=_run_flask, daemon=True)
flask_thread.start()

time.sleep(0.3)

import platform, os
if platform.system() == "Windows":
    os.environ["PYWEBVIEW_USE_EDGE_CHROMIUM"] = "1"

window = webview.create_window("HTML Obfuscator", URL, width=960, height=720)
webview.start()  