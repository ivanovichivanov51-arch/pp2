-- 1. Топтар кестесі (Groups table)
-- Байланыстарды 'Work', 'Family', 'Friends' деп бөлу үшін
CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- 2. Байланыстар кестесі (Contacts table)
-- Негізгі ақпарат: аты-жөні, email және туған күні
CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    birthday DATE,
    group_id INTEGER REFERENCES groups(id) ON DELETE SET NULL
);

-- 3. Телефондар кестесі (Phones table)
-- Бір адамда бірнеше телефон болуы мүмкін (One-to-Many байланысы)
CREATE TABLE IF NOT EXISTS phones (
    id SERIAL PRIMARY KEY,
    contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
    phone VARCHAR(20) NOT NULL,
    type VARCHAR(10) CHECK (type IN ('home', 'work', 'mobile'))
);