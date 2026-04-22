#!/usr/bin/env python3
"""
YouTube Search Server — listens on localhost:7799
Receives save requests from the Chrome extension,
fetches transcripts, and indexes them in SQLite FTS5.
"""

import json
import os
import sqlite3
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    HAS_TRANSCRIPT_API = True
except ImportError:
    HAS_TRANSCRIPT_API = False
    print("WARNING: youtube-transcript-api not installed.")
    print("Run: pip3 install youtube-transcript-api")

DB_PATH = os.path.join(os.path.dirname(__file__), 'videos.db')
PORT = 7799


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS videos (
            id            TEXT PRIMARY KEY,
            title         TEXT,
            save_ts_secs  INTEGER,
            indexed_at    INTEGER DEFAULT (strftime('%s','now')),
            has_transcript INTEGER DEFAULT 0
        );

        CREATE VIRTUAL TABLE IF NOT EXISTS segments USING fts5(
            video_id      UNINDEXED,
            start_secs    UNINDEXED,
            text,
            tokenize      = "porter unicode61"
        );
    ''')
    conn.commit()
    conn.close()


def _write_segments(video_id, segments):
    """Insert (start_secs, text) pairs and mark has_transcript=1."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute('UPDATE videos SET has_transcript=1 WHERE id=?', (video_id,))
    for start, text in segments:
        conn.execute(
            'INSERT INTO segments(video_id, start_secs, text) VALUES (?,?,?)',
            (video_id, int(start), text)
        )
    conn.commit()
    conn.close()


def fetch_and_index(video_id, title, save_ts_secs):
    if not HAS_TRANSCRIPT_API:
        return
    try:
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id)
        segments = [(seg.start, seg.text) for seg in transcript]
        _write_segments(video_id, segments)
        print(f"Indexed {len(segments)} segments: {title}")
    except Exception as e:
        print(f"Transcript unavailable for {video_id}: {e}")


class Handler(BaseHTTPRequestHandler):

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        from urllib.parse import urlparse, parse_qs
        parsed = urlparse(self.path)

        if parsed.path == '/stats':
            conn = sqlite3.connect(DB_PATH)
            row = conn.execute(
                'SELECT COUNT(*), SUM(has_transcript) FROM videos'
            ).fetchone()
            conn.close()
            self._reply(200, {'total': row[0], 'indexed': row[1] or 0})
            return

        if parsed.path != '/search':
            self.send_response(404)
            self.end_headers()
            return
        q = parse_qs(parsed.query).get('q', [''])[0].strip()
        if not q:
            self._reply(400, {'results': [], 'error': 'Missing query'})
            return
        try:
            conn = sqlite3.connect(DB_PATH)
            rows = conn.execute('''
                SELECT v.title, s.video_id, s.start_secs, v.indexed_at
                FROM segments s
                JOIN videos v ON v.id = s.video_id
                WHERE segments MATCH ?
                ORDER BY rank
                LIMIT 25
            ''', (q,)).fetchall()
            conn.close()
            results = [
                {
                    'title': title,
                    'videoId': vid_id,
                    'startSecs': start,
                    'savedAt': indexed_at,
                    'url': f'https://youtube.com/watch?v={vid_id}&t={start}'
                }
                for title, vid_id, start, indexed_at in rows
            ]
            self._reply(200, {'results': results})
        except Exception as e:
            self._reply(500, {'results': [], 'error': str(e)})

    def do_POST(self):
        if self.path != '/save':
            self.send_response(404)
            self.end_headers()
            return

        length = int(self.headers.get('Content-Length', 0))
        data = json.loads(self.rfile.read(length))
        video_id = data.get('videoId', '').strip()
        title = data.get('title', 'Unknown').strip()
        save_ts_secs = int(data.get('currentTime', 0))

        if not video_id:
            self._reply(400, {'message': 'Missing videoId'})
            return

        conn = sqlite3.connect(DB_PATH)
        exists = conn.execute(
            'SELECT id FROM videos WHERE id=?', (video_id,)
        ).fetchone()
        conn.close()

        if exists:
            mins, secs = divmod(save_ts_secs, 60)
            msg = f'Already saved — {title}'
        else:
            conn = sqlite3.connect(DB_PATH)
            conn.execute(
                'INSERT INTO videos(id, title, save_ts_secs) VALUES (?,?,?)',
                (video_id, title, save_ts_secs)
            )
            conn.commit()
            conn.close()
            threading.Thread(
                target=fetch_and_index,
                args=(video_id, title, save_ts_secs),
                daemon=True
            ).start()
            mins, secs = divmod(save_ts_secs, 60)
            msg = f'Saved @ {mins}:{secs:02d} — {title}'

        self._reply(200, {'message': msg})

    def _reply(self, code, body):
        payload = json.dumps(body).encode()
        self.send_response(code)
        self._cors()
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(payload))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, fmt, *args):
        pass  # silence default access log


if __name__ == '__main__':
    init_db()
    print(f'YouTube search server listening on http://localhost:{PORT}')
    print('Press Ctrl+C to stop.\n')
    HTTPServer(('127.0.0.1', PORT), Handler).serve_forever()
