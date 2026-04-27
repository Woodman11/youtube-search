"""Shared filesystem paths for Reelm components."""
import os
import shutil

DATA_DIR = os.path.expanduser('~/Library/Application Support/Reelm')
DB_PATH = os.path.join(DATA_DIR, 'videos.db')

# Older Application Support directory names we migrate from on first run.
_LEGACY_DATA_DIRS = [
    os.path.expanduser('~/Library/Application Support/MyYouTubeSearch'),
]


def _migrate_legacy_db():
    if os.path.exists(DB_PATH):
        return
    os.makedirs(DATA_DIR, exist_ok=True)
    for legacy_dir in _LEGACY_DATA_DIRS:
        legacy = os.path.join(legacy_dir, 'videos.db')
        if os.path.exists(legacy):
            shutil.copy2(legacy, DB_PATH)
            return
    legacy = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'videos.db')
    if os.path.exists(legacy):
        shutil.copy2(legacy, DB_PATH)


_migrate_legacy_db()
