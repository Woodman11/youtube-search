# reeLm — Web Store Screenshot Shot List

_Five shots, ordered for the Web Store carousel (first one is the
hero). All at **1280×800 PNG**. Chrome Web Store requires a
consistent aspect ratio across all screenshots in a listing — don't
mix 1280×800 and 640×400._

## Pre-shoot setup

- Use Chrome with no other extensions visible in the toolbar (or pin
  only reeLm) — clutter looks unprofessional.
- Sign into a clean / generic YouTube account, or use an Incognito
  window with the extension allowed in incognito. Avoid showing
  personal subscriptions, watch history, or recommendations that
  identify you.
- Have ~10–20 videos saved with real transcripts indexed before
  shooting, so the search results look populated.
- Pick query terms that produce 3–5 result groups with at least one
  showing the "▶ N more timestamps in this video" fold-out — that
  feature is unique and worth highlighting.
- Window size: resize Chrome to **exactly 1280×800** before
  capture so you don't have to scale (CMD+Shift+4 on a sized window,
  or use a window-resize tool). Slight chrome/devtools cropping is
  fine; the Web Store will accept it.
- Theme: YouTube in dark mode matches the popup's dark UI — looks
  cohesive.

## Shot 1 — Hero: popup with search results (the headline feature)

**Goal:** in one frame, communicate "type a phrase, get back the
moment in a video where someone said it."

- Background: a YouTube watch page (any non-controversial tutorial,
  e.g. a programming or cooking video) playing in the main window.
- Foreground: reeLm popup open from the toolbar, anchored top-right.
- In the popup: search query already typed (something concrete like
  `kubernetes pods` or `proof by induction`), 3–5 results visible,
  at least one showing the "▶ 2 more timestamps in this video"
  expander. Health dot green. Stats reading e.g. `18 / 20 indexed`.
- Optional caption overlay (added in image editor, not in browser):
  **"Search every word you've ever heard on YouTube."**

## Shot 2 — Save flow: Shift+Y toast on a YouTube page

**Goal:** show the save action — fast, one keystroke, non-intrusive.

- Full YouTube watch page, video playing.
- reeLm toast visible top-right: "Saved" (the actual server response
  message — capture it live).
- Optional overlay: a `Shift` + `Y` keycap graphic in the lower-left
  with an arrow to the toast, plus caption: **"Press Shift+Y to save
  any video to your searchable library."**

## Shot 3 — Result jumps to the spoken-word timestamp

**Goal:** prove the payoff — clicking a result lands you exactly
where the phrase was spoken.

- Split-screen composite (or just a YouTube page mid-playback):
  - Top half / left: the popup with one result highlighted
    (mouse cursor over it), the timestamp visible (e.g. `@ 4:23`).
  - Bottom half / right: the YouTube page that result links to,
    paused/playing at exactly that timestamp, captions visible
    showing the matching phrase.
- Overlay: **"Click a result → jump to the exact moment."**

## Shot 4 — Options page: privacy-first, local-only

**Goal:** reinforce the "100% local, no cloud" pitch — gives privacy-
conscious users a reason to install.

- reeLm options page in its own tab (`chrome-extension://…/
  options.html`), full window.
- The Library stats section visible at top, with a real-looking count
  (e.g. `42 / 45 videos indexed`).
- The red-bordered "Wipe library" section visible below.
- Overlay: **"Your library lives on your machine. No account, no
  cloud, no telemetry."**

## Shot 5 — Empty popup, ready to install

**Goal:** the "first run" view — what a new user sees right after
install, so they know what to expect.

- reeLm popup open, search box empty with placeholder
  `Search saved videos…`, focused.
- Health dot green, stats reading `0 / 0 indexed`.
- Background: the Chrome new-tab page or the reeLm GitHub README,
  not a YouTube page, so it's visually distinct from shots 1–3.
- Overlay: **"Install → press Shift+Y on any YouTube video → start
  searching."**

## Optional: 440×280 small promo tile

Single image, used in Web Store category browsing. Minimal:

- reeLm icon (red magnifier on white) on the left at ~180px.
- Wordmark "reeLm" + tagline "Search every word on YouTube" stacked
  to the right.
- Solid dark background (`#0f0f0f` matches the popup).
- No screenshots — too small to read.

## Capture / edit workflow

1. macOS native: `Cmd+Shift+4` then Space to grab a window, or
   Cmd+Shift+5 for full-screen with the window selected.
2. Open in Preview or any image editor; verify dimensions are
   exactly **1280×800** (resize / crop as needed — don't upscale).
3. Add overlay captions in Preview (Tools → Annotate → Text) or
   Figma / Pixelmator if you want nicer typography.
4. Export as PNG, name `reelm-shot-1.png` … `reelm-shot-5.png`,
   drop into `assets/store/` (gitignored or committed — your call;
   they're useful to keep around for re-uploads).
5. Upload all five in order via the Web Store Developer Dashboard.

## Things to avoid

- Real personal data in the saved-video list (channel names that
  identify you, work-specific search queries).
- Browser bookmarks bar, other extension icons, or notification
  badges in frame.
- Copyrighted thumbnails featuring recognizable faces if you can
  avoid it — pick tutorial/talk videos with neutral thumbnails.
- Any window chrome or OS chrome that reveals beta builds, internal
  hostnames, or your username in a path.
