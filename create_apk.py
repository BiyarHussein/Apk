import os

def create_buildozer_spec(py_file_path):
    # Define the location of your source directory (assuming it’s the root folder)
    source_dir = os.path.dirname(py_file_path)

    # Prepare the buildozer.spec content with a valid source directory
    buildozer_spec_content = f"""
[app]
# (list of other settings...)

# Define the source directory, which should point to the folder containing your Python file
source.dir = {source_dir}
# Specify the Python file to use as the main entry point
source.include_exts = py,png,jpg,kv,atlas
# Additional necessary configurations like requirements
# For example, if you need Kivy and requests:
# requirements = python3,kivy,requests

# (list of other configurations...)
"""

    # Write the content to a new buildozer.spec file
    with open("buildozer.spec", "w") as spec_file:
        spec_file.write(buildozer_spec_content)

# Assuming eth_private_key_viewer.py is in the current directory
create_buildozer_spec('eth_private_key_viewer.py')
