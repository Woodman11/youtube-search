# Reelm

Save YouTube videos with **Shift+Y** while watching, then search across the
auto-generated transcripts of every video you've saved. Local SQLite + FTS5,
no cloud.

```
[Chrome extension] --Shift+Y--> [localhost:7799 server] --> videos.db (FTS5)
                                        |
                                        +-- yt-dlp (transcript fallback)
```

## Install (macOS)

### 1. System dependencies

```bash
brew install python yt-dlp
```

`yt-dlp` is required — the server shells out to it for transcripts.

### 2. Get the code

```bash
git clone <repo-url> ~/reelm
cd ~/reelm
./setup.sh
```

`setup.sh` checks for `python3` and `yt-dlp`, creates `venv/`, installs
Python deps. The only Python dep is `rumps` (used by the optional menu-bar
app `app.py`); the plain server uses only stdlib.

### 3. Load the Chrome extension

1. Open `chrome://extensions`
2. Enable **Developer mode** (top right)
3. Click **Load unpacked** → select the `extension/` folder
4. Pin the icon if you want the popup search

### 4. Start the server

```bash
venv/bin/python server.py
```

Should print `listening on http://localhost:7799`. Open any YouTube video
and press **Shift+Y** — a toast confirms the save and the transcript is
indexed in the background.

### 5. (Optional) Auto-start at login

Two LaunchAgent plists are included:

- `com.james.reelm.plist` — runs `server.py` continuously
- `com.james.reelm-maintain.plist` — runs `maintain.py` every 15 min
  to retry failed transcripts and optimize the FTS index

**Both plists are user-specific.** Before installing, edit them:

- Change the `Label` (`com.james.…`) to your own prefix
- Replace `/Users/james/Systems-Admin/youtube-search/` with the actual
  install path

Then:

```bash
cp com.*.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.<you>.reelm.plist
launchctl load ~/Library/LaunchAgents/com.<you>.reelm-maintain.plist
```

## Usage

- **Save a video:** Shift+Y on any `youtube.com/watch?v=…` page
- **Search:** click the extension icon → type a query
- **CLI search:** `venv/bin/python search.py "your query"`
- **Maintenance run:** `venv/bin/python maintain.py`

## Files

| File | Purpose |
|------|---------|
| `server.py` | HTTP server on `localhost:7799`, accepts saves, indexes transcripts |
| `maintain.py` | Retries failed transcripts, optimizes FTS5, vacuums |
| `app.py` | Optional menu-bar wrapper around `server.py` (uses `rumps`) |
| `search.py` | CLI search |
| `extension/` | Chrome MV3 extension (manifest, content/background/popup scripts) |
| `videos.db` | SQLite DB (created on first run, gitignored) |
| `setup.sh` | Creates venv, installs deps |
| `build.sh` | Builds standalone `.app` via PyInstaller (optional) |

## Migrating existing data

`videos.db` is gitignored. To copy your indexed library to a new Mac:

```bash
scp old-mac:~/reelm/videos.db ~/reelm/videos.db
```

## Troubleshooting

- **Toast says "Server not running"** → start `server.py`, or check
  `~/Library/LaunchAgents/` is loaded (`launchctl list | grep reelm`)
- **Saves work but transcripts never index** → verify `yt-dlp` is on PATH
  (`which yt-dlp`) and is recent (`yt-dlp --version` ≥ 2026.03.17)
- **Shift+Y does nothing** → reload the YouTube tab after installing the
  extension
