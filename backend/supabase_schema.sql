-- Run this in your Supabase SQL Editor (supabase.com → your project → SQL Editor)

-- Table: cached fact-check results
CREATE TABLE IF NOT EXISTS checks (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    text_hash   TEXT NOT NULL UNIQUE,
    original_text TEXT NOT NULL,
    response_json TEXT NOT NULL,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_checks_text_hash ON checks(text_hash);

-- Table: daily usage per user
CREATE TABLE IF NOT EXISTS user_usage (
    id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id  TEXT NOT NULL,
    date     DATE NOT NULL,
    count    INTEGER NOT NULL DEFAULT 0,
    UNIQUE(user_id, date)
);

CREATE INDEX IF NOT EXISTS idx_user_usage_user_date ON user_usage(user_id, date);

-- Enable Row Level Security (important for production)
ALTER TABLE checks ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_usage ENABLE ROW LEVEL SECURITY;

-- Allow the service role (backend) to do everything
CREATE POLICY "Service role full access on checks"
    ON checks FOR ALL USING (true);

CREATE POLICY "Service role full access on user_usage"
    ON user_usage FOR ALL USING (true);
