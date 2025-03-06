import os
import sys
from shutil import copyfile

# Check if the file path is provided as an argument
if len(sys.argv) < 2:
    print("Please provide the path to the Python script.")
    sys.exit(1)

script_path = sys.argv[1]  # Get the Python file path from command line arguments

# Ensure the provided Python script exists
if not os.path.isfile(script_path):
    print(f"Error: The file '{script_path}' does not exist.")
    sys.exit(1)

# Function to create the buildozer.spec file
def create_buildozer_spec(script_path):
    spec_content = f"""
# buildozer.spec
[app]
title = Ethereum Private Key Viewer
package.name = eth_private_key_viewer
package.domain = org
source.include_exts = py,png,jpg,kv,atlas
source.include_patterns = {script_path}
version = 1.0
requirements = kivy, requests, eth-account  # Add additional dependencies here
# Additional settings as required
    """

    # Write content to the buildozer.spec file
    with open('buildozer.spec', 'w') as f:
        f.write(spec_content.strip())

    print("buildozer.spec file created successfully.")

# Function to build the APK using Buildozer
def build_apk():
    print("Starting the APK build process...")
    os.system('buildozer android debug')  # Command to build the APK

    # Check if the build was successful
    if os.path.exists('bin/eth_private_key_viewer-debug.apk'):
        print("APK successfully built!")
    else:
        print("Failed to build APK. Please check the Buildozer output for errors.")

# Main function
def main():
    # Create the buildozer.spec file based on the provided Python script
    create_buildozer_spec(script_path)

    # Build the APK using Buildozer
    build_apk()

if __name__ == "__main__":
    main()
