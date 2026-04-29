yes# reeLm — Chrome Web Store Listing Draft

_Companion to `dist/reelm-extension-v1.5.zip`. Paste these into the
Web Store Developer Dashboard fields when submitting._

---

## Store listing

### Item name (max 75)
reeLm

### Summary (max 132)
Save YouTube videos with Shift+Y, then full-text search every spoken word across your library. 100% local, no cloud, no account.

### Category
Productivity

### Language
English (United States)

### Description (long)

reeLm turns YouTube into a searchable personal library.

Press **Shift+Y** while watching any YouTube video and reeLm saves it.
In the background, it grabs the auto-generated transcript and indexes
every spoken word with SQLite FTS5. Open the popup later, type a
phrase, and jump straight to the moment in the video where someone
said it.

**Why it exists**
YouTube's own search only matches titles and descriptions. If you
remember a phrase from a tutorial you watched two months ago but not
the channel or title, you're stuck scrubbing. reeLm fixes that.

**How it works**
- Shift+Y on any youtube.com/watch page → toast confirms the save
- A tiny local server on 127.0.0.1:7799 (installed separately) fetches
  the transcript and writes it to a SQLite DB on your own machine
- Click the reeLm icon → search box → results link straight to the
  spoken-word timestamp on YouTube

**Local-first, no cloud**
reeLm has no account system, no telemetry, no analytics, no servers
we control. Your saved videos and transcripts live in
`~/Library/Application Support/Reelm/videos.db` on your own computer.
The only network traffic is (1) the local 127.0.0.1 server and
(2) youtube.com itself for transcript fetches.

**Requires the reeLm helper**
The extension is the front-end; the indexing happens in a small
companion service you install via Homebrew on macOS:

```
brew tap Woodman11/reelm
brew install reelm
brew services start reelm
```

Full source, install instructions, and privacy policy:
https://github.com/Woodman11/reelm

---

## Single-purpose description

reeLm has one purpose: let the user save YouTube videos with a
keyboard shortcut and search across the transcripts of those saved
videos from a popup.

---

## Permission justifications

### `host_permissions: *://*.youtube.com/*`
The extension's content script runs on YouTube watch pages so that the
Shift+Y shortcut can capture the video URL, title, and current
playback position when the user presses it. No data is read from
YouTube pages until the user explicitly invokes the shortcut.

### `host_permissions: http://localhost:7799/*`
reeLm's indexing and search backend is a local-only HTTP server
bundled with the user-installed reeLm helper, listening on
127.0.0.1:7799. The extension POSTs save requests to it and GETs
search results from it. No remote server is ever contacted.

### `action` (toolbar popup)
Provides the search UI. Clicking the toolbar icon opens a popup with
a search box that queries the local server's FTS5 index.

### `options_ui`
A small options page exposes a "Wipe Library" button that asks the
local server to clear the SQLite DB. No options are synced.

### Content script (`content.js` on `*://*.youtube.com/*`)
Listens for the Shift+Y keypress on YouTube watch pages, reads the
current video's URL/title/timestamp, and forwards them to the
extension's background service worker, which relays the save to the
local server.

### Background service worker (`background.js`)
Acts as the bridge between the content script and the local server.
It also handles the privileged transcript-fetch requests
(`timedtext` calls to `youtube.com`) so that the content script
doesn't need broader permissions.

### Why no `storage`, `tabs`, `cookies`, etc.
reeLm deliberately requests no broad permissions. All persistent
state lives in the local SQLite DB on the user's machine, not in
extension storage.

---

## Privacy practices (data-disclosure form)

**Does this item collect or use any of the following user data?**

| Category | Collected? | Notes |
|---|---|---|
| Personally identifiable information | No | |
| Health information | No | |
| Financial and payment information | No | |
| Authentication information | No | |
| Personal communications | No | |
| Location | No | |
| Web history | **Yes — used locally only** | URLs of YouTube videos the user explicitly saves with Shift+Y are written to a SQLite DB on the user's own computer. Not transmitted off-device. |
| User activity | No | (No clicks/keystrokes/mouse-movement collected beyond the single Shift+Y trigger.) |
| Website content | **Yes — used locally only** | Titles and auto-generated transcripts of saved videos are indexed in the local DB on the user's own computer. Not transmitted off-device. |

**Certifications (all three required to check):**
- [x] I do not sell or transfer user data to third parties, outside of the approved use cases
- [x] I do not use or transfer user data for purposes that are unrelated to my item's single purpose
- [x] I do not use or transfer user data to determine creditworthiness or for lending purposes

**Privacy policy URL:**
https://github.com/Woodman11/reelm/blob/main/docs/privacy.md

---

## Distribution

- **Visibility:** Public
- **Regions:** All regions
- **Pricing:** Free

---

## Assets still needed before submitting

- [ ] Promo screenshots — at least 1, up to 5, **1280×800 or 640×400 PNG/JPG**
  - Suggested: (1) popup with search results, (2) Shift+Y toast on a YouTube page,
    (3) options page with Wipe Library, (4) ~~zoom on a transcript-jump result~~
- [ ] Small promo tile — **440×280 PNG/JPG** (optional but recommended)
- [ ] Demo GIF for `assets/demo.gif` (referenced in README, not required by the Store)

The 128×128 icon is already in the package (`icons/icon128.png`).
