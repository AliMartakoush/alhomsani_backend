#!/bin/bash

# Parameters
DB_NAME="store_db"
DB_USER="alhomsani"
DB_PASSWORD="essa_alghannam"

# Helper function to run a psql command
run_psql_command() {
    local command="$1"
    sudo -u postgres psql -c "$command"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to execute command: $command"
        exit 1
    fi
}

echo "Configuring PostgreSQL Database..."

# Step 1: Create the database
echo "Creating database '$DB_NAME'..."
run_psql_command "CREATE DATABASE $DB_NAME;"

# Step 2: Create the user
echo "Creating user '$DB_USER'..."
run_psql_command "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"

# Step 3: Grant privileges
echo "Granting privileges on database '$DB_NAME' to user '$DB_USER'..."
run_psql_command "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"

echo "PostgreSQL configuration completed successfully!"
,st
