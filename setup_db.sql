-- Create reddit database if it doesn't exist
SELECT 'CREATE DATABASE reddit'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'reddit')\gexec

-- Connect to reddit database
\c reddit

-- Verify connection
SELECT current_database(), current_user, version();
