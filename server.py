"""
CDDA Remote - small LAN server that injects keystrokes into the game.
	   
		
	  
	  
	  

Start:   python server.py
Tablet:  http://<PC-IP>:5000  (the IP is printed on startup)

Dependencies:  pip install flask keyboard
Note: the 'keyboard' library does not need admin rights on Windows,
as long as CDDA itself is not running as administrator.
"""

import ctypes
import socket
import time

from flask import Flask, jsonify, request, send_from_directory

import keyboard

# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------
PORT = 5000
FOCUS_WINDOW = True              # focus the CDDA window before each keystroke
WINDOW_TITLE_PART = "Cataclysm"  # substring of the game window title
KEY_DELAY = 0.05                 # pause between keys of a sequence (seconds)

app = Flask(__name__, static_folder="static", static_url_path="")

# ----------------------------------------------------------------------------
# Window focus (pure ctypes, no pywin32 required)
# ----------------------------------------------------------------------------
user32 = ctypes.windll.user32


def _find_window(title_part: str):
    """Return the handle of the first top-level window whose title
    contains the given substring (case-insensitive), or None."""
    result = []

    @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    def enum_proc(hwnd, _lparam):
        length = user32.GetWindowTextLengthW(hwnd)
        if length > 0:
            buf = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buf, length + 1)
            if title_part.lower() in buf.value.lower():
                result.append(hwnd)
                return False  # stop enumeration
        return True

    user32.EnumWindows(enum_proc, 0)
    return result[0] if result else None


def focus_game_window() -> bool:
    """Bring the game window to the foreground. Returns False if not found."""
    hwnd = _find_window(WINDOW_TITLE_PART)
    if hwnd is None:
        return False
    if user32.IsIconic(hwnd):
        user32.ShowWindow(hwnd, 9)  # SW_RESTORE
    user32.SetForegroundWindow(hwnd)
    time.sleep(0.05)
    return True


# ----------------------------------------------------------------------------
# Routes
# ----------------------------------------------------------------------------
@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/buttons.json")
def buttons():
    return send_from_directory(".", "buttons.json")


@app.post("/key")
def send_key():
    """Inject a sequence of keystrokes into the game window.

    Expects JSON: {"keys": ["g"]} or {"keys": ["esc", "s"]}.
    Key names follow the 'keyboard' library format.
    """
    data = request.get_json(silent=True) or {}
    keys = data.get("keys", [])
    if not isinstance(keys, list) or not keys:
        return jsonify(ok=False, error="missing or empty 'keys'"), 400

    focused = focus_game_window() if FOCUS_WINDOW else None
    if FOCUS_WINDOW and not focused:
        return jsonify(ok=False, error="CDDA window not found"), 404

    for i, key in enumerate(keys):
        if i > 0:
            time.sleep(KEY_DELAY)
        keyboard.send(key)

    return jsonify(ok=True)


@app.get("/ping")
def ping():
    """Health check: reports whether the game window is currently visible."""
    return jsonify(ok=True, window=_find_window(WINDOW_TITLE_PART) is not None)


# ----------------------------------------------------------------------------
def local_ip() -> str:
    """Best-effort detection of the LAN IP of this machine."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


if __name__ == "__main__":
    print(f"\n  CDDA Remote is running:  http://{local_ip()}:{PORT}\n")
    print("  Open this address in your tablet's browser.")
    print("  Stop with Ctrl+C.\n")
    app.run(host="0.0.0.0", port=PORT)