chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.type === 'save') {
    fetch('http://localhost:7799/save', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(msg.data)
    })
      .then(r => r.json())
      .then(data => sendResponse({ok: true, data}))
      .catch(() => sendResponse({ok: false}));
    return true; // keep channel open for async response
  }

  if (msg.type === 'transcript') {
    const {videoId, captionUrl} = msg.data;
    fetch(captionUrl)
      .then(r => r.json())
      .then(data => {
        const segments = [];
        for (const ev of (data.events || [])) {
          if (!ev.segs) continue;
          const start = (ev.tStartMs || 0) / 1000;
          const text = ev.segs.map(s => s.utf8 || '').join('').trim();
          if (text && text !== '\n') segments.push({start, text});
        }
        if (!segments.length) return;
        return fetch('http://localhost:7799/transcript', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({videoId, segments})
        });
      })
      .catch(() => {});
  }
});
