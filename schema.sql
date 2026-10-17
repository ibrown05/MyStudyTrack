PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    color TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS study_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER NOT NULL,
    minutes INTEGER NOT NULL CHECK (minutes > 0),
    session_date TEXT NOT NULL,
    FOREIGN KEY (subject_id) REFERENCES subjects(id)
);
