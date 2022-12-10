#! /usr/bin/python3
"""
"""

import os
import re
from shutil import move


def rename_files_from_contents(
        file_name_match_pattern,
        in_file_match_pattern,
        base_directory):
    """


    :param file_name_match_pattern:
    :param in_file_match_pattern:
    :param base_directory:

    :return:
    """

    for file in os.scandir(base_directory):
        if re.search(file_name_match_pattern, file.name):
            file_contents = open(file, 'r')
            matches = re.search(in_file_match_pattern,
                                file_contents.read())
            if matches:
                # Need to add something to preserve extensions
                new_file_name = os.path.join(base_directory, matches.group(1))
            move(file, new_file_name)


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('file_name_match_pattern')
    parser.add_argument('in_file_match_pattern')
    parser.add_argument('base_directory')
    args = parser.parse_args()

    rename_files_from_contents(
        args.file_name_match_pattern,
        args.in_file_match_pattern,
        args.base_directory
    )
