"""
CDDA Remote - kleiner LAN-Server, der Tastendruecke ins Spiel schickt.

Start:   python server.py
Tablet:  http://<PC-IP>:5000  (IP wird beim Start angezeigt)

Abhaengigkeiten:  pip install flask keyboard
Hinweis: 'keyboard' braucht unter Windows keine Adminrechte,
solange CDDA nicht als Administrator laeuft.
"""

import ctypes
import socket
import time

from flask import Flask, jsonify, request, send_from_directory

import keyboard

# ----------------------------------------------------------------------------
# Konfiguration
# ----------------------------------------------------------------------------
PORT = 5000
FOCUS_WINDOW = True          # vor jedem Tastendruck CDDA-Fenster fokussieren
WINDOW_TITLE_PART = "Cataclysm"  # Teilstring des Fenstertitels
KEY_DELAY = 0.05             # Pause zwischen Tasten einer Sequenz (Sekunden)

app = Flask(__name__, static_folder="static", static_url_path="")

# ----------------------------------------------------------------------------
# Fenster-Fokus (reines ctypes, kein pywin32 noetig)
# ----------------------------------------------------------------------------
user32 = ctypes.windll.user32


def _find_window(title_part: str):
    result = []

    @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    def enum_proc(hwnd, _lparam):
        length = user32.GetWindowTextLengthW(hwnd)
        if length > 0:
            buf = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buf, length + 1)
            if title_part.lower() in buf.value.lower():
                result.append(hwnd)
                return False  # Suche beenden
        return True

    user32.EnumWindows(enum_proc, 0)
    return result[0] if result else None


def focus_game_window() -> bool:
    hwnd = _find_window(WINDOW_TITLE_PART)
    if hwnd is None:
        return False
    if user32.IsIconic(hwnd):
        user32.ShowWindow(hwnd, 9)  # SW_RESTORE
    user32.SetForegroundWindow(hwnd)
    time.sleep(0.05)
    return True


# ----------------------------------------------------------------------------
# Routen
# ----------------------------------------------------------------------------
@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/buttons.json")
def buttons():
    return send_from_directory(".", "buttons.json")


@app.post("/key")
def send_key():
    data = request.get_json(silent=True) or {}
    keys = data.get("keys", [])
    if not isinstance(keys, list) or not keys:
        return jsonify(ok=False, error="keys fehlt oder leer"), 400

    focused = focus_game_window() if FOCUS_WINDOW else None
    if FOCUS_WINDOW and not focused:
        return jsonify(ok=False, error="CDDA-Fenster nicht gefunden"), 404

    for i, key in enumerate(keys):
        if i > 0:
            time.sleep(KEY_DELAY)
        keyboard.send(key)

    return jsonify(ok=True)


@app.get("/ping")
def ping():
    return jsonify(ok=True, window=_find_window(WINDOW_TITLE_PART) is not None)


# ----------------------------------------------------------------------------
def local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


if __name__ == "__main__":
    print(f"\n  CDDA Remote laeuft:  http://{local_ip()}:{PORT}\n")
    print("  Diese Adresse im Tablet-Browser oeffnen.")
    print("  Beenden mit Strg+C.\n")
    app.run(host="0.0.0.0", port=PORT)
