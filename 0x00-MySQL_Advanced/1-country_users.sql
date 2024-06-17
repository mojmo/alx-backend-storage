-- This script creates a table named 'users' with relevant attributes for user data storage.

-- Create the 'users' table if it does not already exist
CREATE TABLE IF NOT EXISTS users (
    -- Unique identifier (primary key)
    id INT NOT NULL AUTO_INCREMENT,
    -- User's email address (unique)
    email VARCHAR(255) NOT NULL UNIQUE,
    -- User's name
    name VARCHAR(255),
    -- User's country (enumeration)
    country ENUM('US', 'CO', 'TN') NOT NULL DEFAULT 'US'
    -- Set 'id' as the primary key
    , PRIMARY KEY (id)
);
