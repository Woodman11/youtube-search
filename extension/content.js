document.addEventListener('keydown', async (e) => {
  // Shift+Y — use capture phase (third arg true) so YouTube's stopPropagation() can't swallow it
  if (e.code !== 'KeyY' || !e.shiftKey || e.altKey || e.ctrlKey || e.metaKey) return;
  const t = e.target;
  if (t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName))) return;
  e.preventDefault();

  const video = document.querySelector('video');
  if (!video) {
    showToast('No video found on page', 'error');
    return;
  }

  const params = new URLSearchParams(window.location.search);
  const videoId = params.get('v');
  if (!videoId) return; // not on a watch page, ignore silently

  const currentTime = Math.floor(video.currentTime);
  const title = document.title.replace(/ - YouTube$/, '').trim();

  // Fetch transcript from the page itself — avoids any server-side YouTube requests
  const segments = await fetchTranscriptFromPage();

  fetch('http://localhost:7799/save', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ videoId, currentTime, title, segments })
  })
    .then(r => r.json())
    .then(data => showToast(data.message))
    .catch(() => showToast('Server not running — start server.py', 'error'));
}, true);

async function fetchTranscriptFromPage() {
  const baseUrl = getCaptionBaseUrl();
  if (!baseUrl) return null;
  try {
    const r = await fetch(baseUrl + '&fmt=json3');
    const data = await r.json();
    const segs = [];
    for (const ev of (data.events || [])) {
      if (!ev.segs) continue;
      const start = (ev.tStartMs || 0) / 1000;
      const text = ev.segs.map(s => s.utf8 || '').join('').trim();
      if (text && text !== '\n') segs.push({ start, text });
    }
    return segs.length ? segs : null;
  } catch {
    return null;
  }
}

function getCaptionBaseUrl() {
  // ytInitialPlayerResponse is embedded as JSON in a <script> tag — no injection needed
  for (const script of document.querySelectorAll('script')) {
    const text = script.textContent;
    if (!text.includes('captionTracks')) continue;
    const urls = [];
    const re = /"baseUrl":"(https:[^"]+timedtext[^"]+)"/g;
    let m;
    while ((m = re.exec(text)) !== null) {
      urls.push(m[1].replace(/\\u0026/g, '&'));
    }
    if (!urls.length) continue;
    return urls.find(u => /[?&]lang=en/.test(u)) || urls[0];
  }
  return null;
}

function showToast(msg, type = 'ok') {
  // Remove any existing toast
  document.getElementById('yt-search-toast')?.remove();

  const el = document.createElement('div');
  el.id = 'yt-search-toast';
  el.textContent = msg;
  Object.assign(el.style, {
    position: 'fixed',
    top: '72px',
    right: '20px',
    zIndex: '99999',
    background: type === 'error' ? '#c0392b' : '#1a1a2e',
    color: '#fff',
    padding: '10px 18px',
    borderRadius: '6px',
    font: 'bold 13px/1.4 "YouTube Noto",Roboto,sans-serif',
    boxShadow: '0 4px 14px rgba(0,0,0,.45)',
    transition: 'opacity .3s ease',
    opacity: '1',
  });

  document.body.appendChild(el);

  setTimeout(() => {
    el.style.opacity = '0';
    setTimeout(() => el.remove(), 300);
  }, 2700);
}
