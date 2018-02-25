#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------------------------------------------------------
# checksum.py
#  A SHA1 hash checksum list generator for fonts and fontTools
#  XML dumps of font OpenType table data
#
# Copyright 2018 Christopher Simpkins
# MIT License
#
# Usage: checksum.py (options) [file path 1]...[file path n]
#
# Dependencies: Python fontTools library
#----------------------------------------------------------------

import argparse
import hashlib
import os
import sys

from os.path import basename

from fontTools.ttLib import TTFont


def main(filepaths, stdout_write=False, use_ttx=False, include_tables=None, exclude_tables=None, do_not_cleanup=False):
    checksum_dict = {}
    for path in filepaths:
        if not os.path.exists(path):
            sys.stderr.write("[checksum.py] ERROR: " + path + " is not a valid file path" + os.linesep)
            sys.exit(1)

        if use_ttx:
            # append a .ttx extension to existing extension to maintain data about the binary that
            # was used to generate the .ttx XML dump.  This creates unique checksum path values for
            # paths that would otherwise not be unique with a file extension replacement with .ttx
            # An example is woff and woff2 web font files that share the same base file name:
            #
            #  coolfont-regular.woff  ==> coolfont-regular.ttx
            #  coolfont-regular.woff2 ==> coolfont-regular.ttx  (KAPOW! checksum data lost as this would overwrite dict value)
            temp_ttx_path = path + ".ttx"

            tt = TTFont(path)
            tt.saveXML(temp_ttx_path, newlinestr="\n", skipTables=exclude_tables, tables=include_tables)
            checksum_path = temp_ttx_path
        else:
            if include_tables is not None:
                sys.stderr.write("[checksum.py] -i and --include are not supported for font binary filepaths. \
                    Use these flags for checksums with the --ttx flag.")
                sys.exit(1)
            if exclude_tables is not None:
                sys.stderr.write("[checksum.py] -e and --exclude are not supported for font binary filepaths. \
                    Use these flags for checksums with the --ttx flag.")
                sys.exit(1)
            checksum_path = path

        file_contents = read_binary(checksum_path)

        # store SHA1 hash data and associated file path basename in the checksum_dict dictionary
        checksum_dict[basename(checksum_path)] = hashlib.sha1(file_contents).hexdigest()

        # remove temp ttx files when present
        if use_ttx and do_not_cleanup is False:
            os.remove(temp_ttx_path)

    # generate the checksum list string for writes
    checksum_out_data = ""
    for key in checksum_dict.keys():
        checksum_out_data += checksum_dict[key] + "  " + key + "\n"

    # write to stdout stream or file based upon user request (default = file write)
    if stdout_write:
        sys.stdout.write(checksum_out_data)
    else:
        checksum_report_filepath = "checksum.txt"
        with open(checksum_report_filepath, "w") as file:
            file.write(checksum_out_data)


def read_binary(filepath):
    with open(filepath, mode='rb') as file:
        return file.read()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="checksum.py")
    parser.add_argument("-t", "--ttx", help="Calculate from ttx file", action="store_true")
    parser.add_argument("-s", "--stdout", help="Write output to stdout stream", action="store_true")
    parser.add_argument("-n", "--noclean", help="Do not discard *.ttx files used to calculate SHA1 hashes", action="store_true")
    parser.add_argument("filepaths", nargs="+", help="One or more file paths to font binary files")

    parser.add_argument("-i", "--include", action="append", help="Included OpenType tables for ttx data dump")
    parser.add_argument("-e", "--exclude", action="append", help="Excluded OpenType tables for ttx data dump")

    args = parser.parse_args(sys.argv[1:])

    main(args.filepaths, stdout_write=args.stdout, use_ttx=args.ttx, do_not_cleanup=args.noclean, include_tables=args.include, exclude_tables=args.exclude)
