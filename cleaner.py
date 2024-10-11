import re
import os

"""
>>> cleaner.py
Patch all the PDF files in the current directory removing all the PDF objects matching with the `watermark_features`
"""

# Put here the entries that identify the watermark object
watermark_features = [b'/Width 720', b'/Height 540']

def watermark_rule(match):
    # Get the full matched block (including << and >>)
    block = match.group(0)
    if all(feature in block for feature in watermark_features):
        print(str(block))
        return b'<<>>'  # block.replace(b'Width 0',b'Width 0')
    else:
        return block


# List the PDF files in the CWD
current_directory = os.getcwd()
files = [file_name for file_name in os.listdir(
    current_directory) if os.path.isfile(os.path.join(current_directory, file_name))
    and file_name.endswith('.pdf')
    and '-cleaned' not in file_name]

# The Regex for PDF dictionaries
object_pattern = br'<<[^>]+>>'

for file in files:
    pdf = open(file, 'rb').read()
    pdf = re.sub(object_pattern, watermark_rule, pdf)
    open(f'{file.replace('.pdf','')}-cleaned.pdf', 'wb').write(pdf)