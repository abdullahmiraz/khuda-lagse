import os
import re
from datetime import datetime

# Define the path to the parent repository (current directory)
parent_repo_path = os.getcwd()

# Keep track of encountered submodule paths and URLs
encountered_submodules = set()

# Read the existing .gitmodules content
with open(os.path.join(parent_repo_path, '.gitmodules'), 'r') as gitmodules_file:
    existing_gitmodules = gitmodules_file.read()

# Initialize an empty string to store .gitmodules contents
gitmodules_contents = ''

# Function to get the URL of a submodule from its .git/config
def get_submodule_url(submodule_path):
    git_config_path = os.path.join(parent_repo_path, submodule_path, '.git', 'config')
    
    # Read the .git/config file of the submodule
    with open(git_config_path, 'r') as git_config_file:
        config_contents = git_config_file.read()
    
    # Use regular expressions to extract the URL
    match = re.search(r'url\s*=\s*(.*)', config_contents)
    if match:
        return match.group(1)
    else:
        return None

# Iterate through all directories in the parent repository
for root, dirs, files in os.walk(parent_repo_path):
    if '.git' in dirs:
        # A .git folder is found, indicating a child repository
        child_path = os.path.relpath(root, parent_repo_path)

        # Get the URL for the submodule
        submodule_url = get_submodule_url(child_path)
        # Replace backslashes with forward slashes in child_path
        child_path = child_path.replace("\\", "/")
        
        # Check if submodule files exist
        submodule_exists = os.path.exists(os.path.join(parent_repo_path, child_path))
        
        # Record the encountered submodule
        if (child_path, submodule_url) not in encountered_submodules:
            encountered_submodules.add((child_path, submodule_url))
            
            # Add timestamp comment only for new submodules
            timestamp_comment = f"# Updated on ----- Date: {datetime.now().strftime('%d %B %Y')} ; Time: {datetime.now().strftime('%I.%M %p')}\n"
            gitmodules_contents += timestamp_comment
        
        gitmodules_contents += f"[submodule \"{child_path}\"]\n"
        gitmodules_contents += f'    path = "{child_path}"\n'
        
        if submodule_url:
            gitmodules_contents += f"    url = {submodule_url}\n"
        else:
            gitmodules_contents += f"    # url = {submodule_url}  # Submodule files not found\n"
        
        gitmodules_contents += "\n"

# Write the combined contents to the .gitmodules file
with open(os.path.join(parent_repo_path, '.gitmodules'), 'w') as gitmodules_file:
    gitmodules_file.write(existing_gitmodules.replace("[submodule", "# [submodule"))
    gitmodules_file.write(gitmodules_contents)

print("Submodules added to .gitmodules file.")
