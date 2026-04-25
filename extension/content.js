document.addEventListener('keydown', (e) => {
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

  // Route through background service worker to avoid Private Network Access block
  chrome.runtime.sendMessage(
    {type: 'save', data: {videoId, currentTime, title}},
    response => {
      if (chrome.runtime.lastError) {
        showToast('Extension error — reload page', 'error');
        return;
      }
      if (response && response.ok) {
        showToast(response.data.message);
        if (response.data.new_save) uploadTranscript(videoId);
      } else {
        showToast('Server not running — start server.py', 'error');
      }
    }
  );
}, true);

// Fire-and-forget: pass caption URL to background, which fetches and uploads transcript
function uploadTranscript(videoId) {
  const baseUrl = getCaptionBaseUrl();
  if (!baseUrl) return;
  // Background worker fetches the timedtext (no CORS restriction there)
  chrome.runtime.sendMessage({type: 'transcript', data: {videoId, captionUrl: baseUrl + '&fmt=json3'}});
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
  document.getElementById('yt-search-host')?.remove();

  // Shadow DOM isolates the toast from YouTube's CSS and MutationObservers
  const host = document.createElement('div');
  host.id = 'yt-search-host';
  const shadow = host.attachShadow({mode: 'closed'});

  const style = document.createElement('style');
  style.textContent = `
    .toast {
      position: fixed;
      top: 72px;
      right: 20px;
      z-index: 2147483647;
      background: ${type === 'error' ? '#c0392b' : '#1a1a2e'};
      color: #fff;
      padding: 10px 18px;
      border-radius: 6px;
      font: bold 13px/1.4 sans-serif;
      box-shadow: 0 4px 14px rgba(0,0,0,.45);
      opacity: 1;
      transition: opacity .3s ease;
    }
  `;

  const el = document.createElement('div');
  el.className = 'toast';
  el.textContent = msg;

  shadow.appendChild(style);
  shadow.appendChild(el);
  document.documentElement.appendChild(host);

  setTimeout(() => {
    el.style.opacity = '0';
    setTimeout(() => host.remove(), 300);
  }, 2700);
}
