import os
import subprocess

"""
>>> unlocker.py
Unlock all the permission for all the PDF files in the current directory.
This requires `pdftk` to work! It can be installed via
`$ sudo snap install pdftk`
"""

# List the PDF files in the CWD
current_directory = os.getcwd()
files = [file_name for file_name in os.listdir(
    current_directory) if os.path.isfile(os.path.join(current_directory, file_name))
    and file_name.endswith('.pdf')]

# Unlock the files
for file in files:
    print(file)
    output_file = file.split('.pdf')[0]
    process = subprocess.run(
        f'pdftk {file}.pdf output {output_file}-unlocked.pdf allow AllFeatures', shell=True, cwd=current_directory)
