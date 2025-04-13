# Parameters
$pythonExecutable = "python" # Change to "python3" if needed or specify the full path to your Python executable
$djangoSettingsModule = "core.settings" # Replace 'myproject' with your actual Django project name

# Helper function to run a shell command
function Run-Command {
    param (
        [string]$Command
    )
    try {
        Invoke-Expression $Command
    } catch {
        Write-Host "Error: $($_.Exception.Message)"
        exit 1
    }
}

Write-Host "Running Django setup..."

# Step 1: Set DJANGO_SETTINGS_MODULE environment variable
[System.Environment]::SetEnvironmentVariable("DJANGO_SETTINGS_MODULE", $djangoSettingsModule, [System.EnvironmentVariableTarget]::Process)

# Step 2: Run migrations
Write-Host "Making migrations..."
Run-Command "$pythonExecutable manage.py makemigrations"

Write-Host "Applying migrations..."
Run-Command "$pythonExecutable manage.py migrate"

# Step 3: Create a superuser
Write-Host "Creating Django superuser..."
$superuserEmail = Read-Host -Prompt "Enter superuser email"
$superuserPassword = Read-Host -Prompt "Enter superuser password (input will be hidden)" -AsSecureString

# Convert the secure string to plain text
$plainPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($superuserPassword))

# Save the Python script to a temporary file
$tempPythonScript = [System.IO.Path]::GetTempFileName() + ".py"
Set-Content -Path $tempPythonScript -Value @"
import os
from django.contrib.auth.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '$djangoSettingsModule')

email = "$superuserEmail"
password = "$plainPassword"
username = email.split('@')[0]

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser created successfully with username: {username}")
else:
    print("Superuser already exists.")
"@

Write-Host "Running superuser creation script..."
Run-Command "$pythonExecutable $tempPythonScript"

# Clean up temporary Python script
Remove-Item $tempPythonScript

Write-Host "Django setup completed successfully!"

