-- Create users table

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(60) NOT NULL, -- Adjusted for bcrypt
    name VARCHAR(255) NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT false   
);