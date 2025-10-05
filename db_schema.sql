-- SQLite 建表
CREATE TABLE IF NOT EXISTS annotations (
id INTEGER PRIMARY KEY AUTOINCREMENT,
image_id TEXT NOT NULL,
type TEXT NOT NULL,
x REAL,
y REAL,
width REAL,
height REAL,
label TEXT,
zoom_level INTEGER,
metadata TEXT,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);