#!/usr/bin/env python3
import os
import sqlite3
import sys
import threading
from http.server import HTTPServer

import rumps

import server
from server import init_db, Handler, DB_PATH, PORT


def _icon_path():
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, 'icons', 'icon32.png')
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'extension', 'icons', 'icon32.png')


class ReelmApp(rumps.App):
    def __init__(self):
        super().__init__('', icon=_icon_path(), template=False, quit_button=None)
        self.stats_item = rumps.MenuItem('Loading…')
        self.menu = [self.stats_item, None, rumps.MenuItem('Quit', callback=self._quit)]

        init_db()
        threading.Thread(
            target=lambda: HTTPServer(('127.0.0.1', PORT), Handler).serve_forever(),
            daemon=True
        ).start()
        self._refresh_stats(None)

    @rumps.timer(30)
    def _refresh_stats(self, _):
        try:
            conn = sqlite3.connect(DB_PATH)
            row = conn.execute('SELECT COUNT(*), SUM(has_transcript) FROM videos').fetchone()
            conn.close()
            total, indexed = row[0], row[1] or 0
            self.stats_item.title = f'{indexed} / {total} videos indexed'
        except Exception:
            self.stats_item.title = 'DB unavailable'

    def _quit(self, _):
        rumps.quit_application()


if __name__ == '__main__':
    ReelmApp().run()
