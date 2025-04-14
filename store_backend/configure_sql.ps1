# Parameters
$dbName = "store_db"
$dbUser = "alhomsani"
$dbPassword = "essa_alghannam"

# Helper function to run a psql command
function Run-PSQLCommand {
    param (
        [string]$Command
    )
    try {
        psql -U postgres -c "$Command"
    } catch {
        Write-Host "Error: $($_.Exception.Message)"
        exit 1
    }
}

Write-Host "Configuring PostgreSQL Database..."

# Step 1: Create the database
Write-Host "Creating database '$dbName'..."
Run-PSQLCommand "CREATE DATABASE $dbName;"

# Step 2: Create the user
Write-Host "Creating user '$dbUser'..."
Run-PSQLCommand "CREATE USER $dbUser WITH PASSWORD '$dbPassword';"

# Step 3: Grant privileges
Write-Host "Granting privileges on database '$dbName' to user '$dbUser'..."
Run-PSQLCommand "GRANT ALL PRIVILEGES ON DATABASE $dbName TO $dbUser;"

Write-Host "PostgreSQL configuration completed successfully!"

