PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS study_sessions (session_id INTEGER PRIMARY KEY AUTOINCREMENT,date TEXT,start_time TEXT,end_time TEXT,duration_min INTEGER,subject TEXT,technique TEXT,distractions INTEGER,mood INTEGER,caffeine_mg INTEGER,productivity INTEGER);
CREATE TABLE IF NOT EXISTS metadata (key TEXT PRIMARY KEY,value TEXT);
