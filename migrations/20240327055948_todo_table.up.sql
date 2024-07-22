-- Add up migration script here
BEGIN;

CREATE TABLE todo (
  uuid          UUID PRIMARY KEY NOT NULL,
  status        TEXT NOT NULL DEFAULT 'todo',
  title         TEXT NOT NULL,
  description   TEXT,
  created_at    TIMESTAMP DEFAULT now(),
  updated_at    TIMESTAMP DEFAULT now()
);

COMMIT;
