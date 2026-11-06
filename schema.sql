-- Smart Nutrition Analyzer Database Schema

CREATE TABLE IF NOT EXISTS users (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT    NOT NULL,
    email           TEXT    NOT NULL UNIQUE,
    password_hash   TEXT    NOT NULL,
    age             INTEGER DEFAULT 25,
    weight_kg       REAL    DEFAULT 70,
    height_cm       REAL    DEFAULT 170,
    gender          TEXT    DEFAULT 'male',
    activity_level  TEXT    DEFAULT 'moderate',
    daily_calorie_goal INTEGER DEFAULT 2000,
    created_at      TEXT    DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS foods (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    name         TEXT    NOT NULL UNIQUE,
    category     TEXT    NOT NULL DEFAULT 'Other',
    calories     REAL    NOT NULL DEFAULT 0,   -- per 100g
    protein      REAL    DEFAULT 0,
    carbs        REAL    DEFAULT 0,
    fat          REAL    DEFAULT 0,
    fiber        REAL    DEFAULT 0,
    sugar        REAL    DEFAULT 0,
    sodium       REAL    DEFAULT 0,
    serving_size REAL    DEFAULT 100,
    serving_unit TEXT    DEFAULT 'g',
    created_by   INTEGER REFERENCES users(id),
    created_at   TEXT    DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS food_logs (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id           INTEGER NOT NULL REFERENCES users(id),
    food_id           INTEGER NOT NULL REFERENCES foods(id),
    quantity_g        REAL    NOT NULL DEFAULT 100,
    meal_type         TEXT    DEFAULT 'lunch',
    log_date          TEXT    NOT NULL,
    calories_per_100g REAL    DEFAULT 0,
    protein_per_100g  REAL    DEFAULT 0,
    carbs_per_100g    REAL    DEFAULT 0,
    fat_per_100g      REAL    DEFAULT 0,
    fiber_per_100g    REAL    DEFAULT 0,
    created_at        TEXT    DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_food_logs_user_date ON food_logs(user_id, log_date);
CREATE INDEX IF NOT EXISTS idx_foods_category ON foods(category);
