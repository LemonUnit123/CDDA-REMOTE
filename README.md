# CDDA Remote

Turn an Android tablet (or any touch device) into a remote control for
**Cataclysm: Dark Days Ahead** running on your PC — big touch buttons with
icons instead of memorizing 80 keybindings.

A tiny Python server on your PC serves a web UI over your home network and
injects the corresponding keystrokes into the CDDA window. No mods, no game
API — works with any CDDA version.

## Features

- 8-direction movement pad with the classic `@` as "wait one turn"
- 40 default actions in 4 tabs (World / Body / Menus / System)
- **In-app settings**: language (DE/EN), pad position (left/right/off),
  button size (S/M/L), vibration feedback — saved on the device
- Fully data-driven: all buttons live in `buttons.json`, edit and reload
- Key **sequences** per button (e.g. `["esc", "s"]` to save)
- Automatically focuses the CDDA window before each keystroke
- No build step, no framework, no external assets — three files

## Quick start

Requires Python 3.9+ on the PC running CDDA (Windows).

```
pip install -r requirements.txt
python server.py
```

The server prints your LAN address, e.g. `http://192.168.178.42:5000`.
Open it in your tablet's browser. For a fullscreen app feel, use
"Add to Home Screen".

If the Windows Firewall asks, allow access for **private networks**.

### Schnellstart (Deutsch)

Auf dem PC: `pip install -r requirements.txt`, dann `python server.py`.
Die angezeigte Adresse im Tablet-Browser öffnen. Sprache lässt sich in den
Einstellungen (⚙) auf Deutsch stellen.

## Customizing buttons

Edit `buttons.json` — no server restart needed, just reload the page.

```json
{ "icon": "🔧", "label": { "de": "Benutzen", "en": "Use item" }, "keys": ["a"] }
```

- `keys` is a **sequence** of keystrokes in
  [`keyboard`](https://github.com/boppreh/keyboard) library format:
  `"g"`, `"shift+e"`, `"esc"`, `"enter"`, `"tab"`, `"space"`, …
- `label` maps language codes to text. Add any language (e.g. `"fr"`)
  and it automatically appears in the settings panel.

## Server configuration

Top of `server.py`:

| Option              | Meaning                                              |
|---------------------|------------------------------------------------------|
| `PORT`              | Default 5000                                         |
| `FOCUS_WINDOW`      | Focus the CDDA window before each keystroke          |
| `WINDOW_TITLE_PART` | Substring of the window title (default "Cataclysm")  |
| `KEY_DELAY`         | Delay between keys in a sequence (seconds)           |

## Good to know

- **Verify keybindings.** The defaults in `buttons.json` match CDDA's
  stock bindings, but defaults change between versions. Press `?` in game
  to see your current bindings and adjust the JSON where needed.
- Keys like `shift+7` depend on your **physical keyboard layout** (`&` is
  Shift+6 on a German layout). You can also use the character directly,
  e.g. `["&"]`.
- If CDDA runs **as administrator**, the server must too, or keystrokes
  won't arrive.
- **LAN only, by design.** The server injects arbitrary keystrokes into
  your PC and has no authentication. Never expose it to the internet.

## Project structure

```
cdda-remote/
├── server.py          Flask server, keystroke injection, window focus
├── buttons.json       All tabs & buttons — data-driven, edit freely
├── requirements.txt
└── static/
    └── index.html     Touch UI, settings panel, i18n
```

## License

MIT — see [LICENSE](LICENSE).
