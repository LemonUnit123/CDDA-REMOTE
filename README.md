# About why this project exists

I'm a lazy person, and when I first got into Cataclysm: Dark Days Ahead, I quickly realized just how many key combinations there are to remember. While the depth of the game is amazing, I kept getting pulled out of the experience because I had to constantly recall or look up shortcuts.

That inspired me to build a simple remote control with visual buttons similar to a Stream Deck with icons and short descriptions instead of relying solely on keyboard shortcuts. The goal wasn't to replace the keyboard, but to make learning and using the game's controls much more approachable.

I mostly vibe-coded this project together with Claude, and since it's been genuinely useful for me, I thought I'd share it with anyone else who finds CDDA's keybindings a bit overwhelming.

Hopefully it helps you spend less time memorizing shortcuts and more time surviving the apocalypse. :)

# CDDA Remote

Turn an Android tablet (or any touch device) into a remote control for
**Cataclysm: Dark Days Ahead** running on your PC — big touch buttons with
icons instead of memorizing 80 keybindings.

A tiny Python server on your PC serves a web UI over your home network and
injects the corresponding keystrokes into the CDDA window. No mods, no game
API — works with any CDDA version.

## Visuals


<img width="640" height="400" alt="main view" src="https://github.com/user-attachments/assets/4c9e7f68-b2fa-4184-8289-38903b091b52" /> <img width="640" height="400" alt="settings" src="https://github.com/user-attachments/assets/83f86ca8-c3c5-4ae4-820f-07c385406a90" />
<img width="640" height="400" alt="editing" src="https://github.com/user-attachments/assets/457e8bc9-5e25-4ff3-8f12-dfd16a53ae41" /> <img width="640" height="400" alt="addbutton" src="https://github.com/user-attachments/assets/fe3306a7-cdce-4b57-9838-5431bfa4d27b" />




## Features

- 8-direction movement pad with the classic `@` as "wait one turn",
  plus optional hold-to-walk
- **Editable hotbar** above the pad for your most-used actions, with a
  **repeat button** that re-fires the last action you triggered
- 40+ default actions in 4 tabs (World / Body / Menus / System)
- **In-app settings**: language (DE/EN), pad position (left/right/off),
  hotbar position (top/left/right), button size (S/M/L), hold-to-walk speed,
  vibration feedback — saved on the device
- Fully data-driven: buttons, hotbar and tabs are all editable from the web
  UI and stored in `buttons.json`
- Key **sequences** per button (e.g. `["esc", "s"]` to save)
- Automatically focuses the CDDA window before each keystroke

## Quick start

Requires Python 3.9+ on the PC running CDDA (Windows).
Just open Cmd or Powershell in the tools directory and type:

```
pip install -r requirements.txt
python server.py
```

The server prints your LAN address, e.g. `http://192.168.178.42:5000`.
Open it in your tablet's browser. For a fullscreen app feel, use
"Add to Home Screen".

If the Windows Firewall asks, allow access for **private networks**.

## Customizing buttons

The fastest way is the **built-in editor**: tap the ✎ icon in the header to
enter edit mode, then tap any button to change it or the **+** tile to add a
new one. You can set the icon (pick from the palette or type any emoji), the
label, the key sequence, which tab or the hotbar it belongs to, and reorder
buttons. Changes are saved to `buttons.json` on the PC, so they apply to
every device that connects.

Buttons you create carry one plain label that stays the same in every
language. The bundled buttons ship with translations, and editing anything
but their text leaves those translations intact.

**Tabs are editable too.** In edit mode the tab bar gains two extra buttons:
**+** creates a new tab, **✎** renames, reorders or deletes the current one.
Deleting a tab removes its buttons as well, so it asks for a second tap to
confirm — and the last remaining tab can't be deleted.

Icons are plain Unicode characters — no image files involved. Anything your
device can display works, including emoji from your keyboard.

You can also edit `buttons.json` directly — no server restart needed, just
reload the page.

```json
{ "icon": "🔧", "label": "Use item", "keys": ["a"] }
{ "icon": "🔧", "label": { "de": "Benutzen", "en": "Use item" }, "keys": ["a"] }
```

- `label` is either a plain string, or a map of language codes to text.
  Adding a language (e.g. `"fr"`) makes it appear in the settings panel.
- `keys` is a **sequence** of keystrokes in
  [`keyboard`](https://github.com/boppreh/keyboard) library format:
  `"g"`, `"shift+e"`, `"esc"`, `"enter"`, `"tab"`, `"space"`, …

The first time you save from the editor, the original file is backed up as
`buttons.backup.json`.

## Hotbar and repeat button

The row above the movement pad is a hotbar: the shortcuts you reach for
constantly, always visible no matter which tab is open. It lives under the
`hotbar` key in `buttons.json` and is edited exactly like any other button —
in edit mode, tap a hotbar entry to change it or the **+** to add one. The
tab selector in the editor includes "Hotbar", so you can move buttons
between the hotbar and any tab.

Settings let you place it above the tabs, or as a vertical column on the
left or right — so you can run the movement pad on one side, tabs in the
middle and the hotbar on the other. In a side column its buttons take the
same square shape as the grid tiles. On narrow portrait screens it always
falls back to the horizontal row.

The **⟳** button at the end repeats the last action you triggered, showing
its icon as a reminder.

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
