import os
import subprocess

# Define the path to the SQLite database file
db_file_path = r"C:\Users\admin\allone\data\all_one_inc.db"

# Function to run a git command
def run_git_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing command: {command}")
        print(e)
        return False
    return True

# Ensure the database file is tracked by Git
status_command = "git status"
status_output = subprocess.run(status_command, shell=True, capture_output=True, text=True)
print(status_output.stdout)

# Stage all modified files
if "Changes not staged for commit" in status_output.stdout:
    print("Adding modified files...")
    run_git_command("git add -u")

# Stage all untracked files
if "Untracked files" in status_output.stdout:
    print("Adding untracked files...")
    run_git_command("git add -A")

# Commit the changes
run_git_command('git commit -m "Update SQLite database and add untracked files"')

# Pull the latest changes and rebase
run_git_command("git pull origin main --rebase")

# Push the changes
run_git_command("git push origin main")

# Final status check
final_status = subprocess.run(status_command, shell=True, capture_output=True, text=True)
print(final_status.stdout)
