-- This script creates a table named 'users' with the following attributes:
-- id: integer, never null, auto increment, primary key
-- email: string (255 characters), never null, unique
-- name: string (255 characters)
-- The script ensures that if the table already exists, it will not fail

-- Create the 'users' table if it does not already exist
CREATE TABLE IF NOT EXISTS users (
    -- id: Primary key, auto increment
    id INT NOT NULL AUTO_INCREMENT,
    -- email: Unique and never null
    email VARCHAR(255) NOT NULL UNIQUE,
    -- name: Optional
    name VARCHAR(255),
    -- Define the primary key
    PRIMARY KEY (id)
);
