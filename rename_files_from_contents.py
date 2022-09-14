#! /usr/bin/python3

import os
import re
from shutil import move

file_name_match_pattern = r''
in_file_match_pattern = r''
base_directory = ''

for file in os.scandir(base_directory):
    if re.search(file_name_match_pattern, file.name):
        file_contents = open(file, 'r')
        matches = re.search(in_file_match_pattern,
                            file_contents.read())
        if matches:
            # Need to add something to preserve extensions
            new_file_name = os.path.join(base_directory, matches.group(1))
            move(file, new_file_name)
