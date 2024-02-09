DROP TABLE IF EXISTS expenses;

CREATE TABLE expenses (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  amount INTEGER NOT NULL,
  name TEXT,
  category TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  length INTEGER NOT NULL,
  description TEXT
);