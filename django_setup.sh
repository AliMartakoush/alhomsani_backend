#!/bin/bash

# Parameters
python_executable="python3"
django_settings_module="core.settings"
project_root="$(pwd)"  # Add project root path

# Helper function to run commands with error handling
run_command() {
    echo "Running: $1"
    if ! eval "$1"; then
        echo "Error: Command failed" >&2
        exit 1
    fi
}

echo "Running Django setup..."

# Add Python path configuration
export PYTHONPATH="${PYTHONPATH}:$project_root"
export DJANGO_SETTINGS_MODULE="$django_settings_module"

# Verify manage.py exists
if [ ! -f "manage.py" ]; then
    echo "Error: manage.py not found in current directory!" >&2
    exit 1
fi

# Step 2: Run migrations
echo "Making migrations..."
run_command "$python_executable manage.py makemigrations"

echo "Applying migrations..."
run_command "$python_executable manage.py migrate"

echo "creating superuser ..."
run_command "$python_executable manage.py createsuperuser"

echo "Django setup completed successfully!"
