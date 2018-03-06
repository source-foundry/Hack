#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------------------------------------
# checksum.py
#  A SHA1 hash checksum list generator for fonts and fontTools
#  XML dumps of font OpenType table data + checksum testing
#  script
#
# Copyright 2018 Christopher Simpkins
# MIT License
#
# Dependencies:
#   - Python fontTools library
#   - Python 3 interpreter
#
# Usage: checksum.py (options) [file path 1]...[file path n]
#
#   `file path` should be defined as a path to a font file for all use cases except with use of -c/--check.
#   With the -c/--check option, use one or more file paths to checksum files
#
# Options:
#   -h, --help          Help
#   -t, --ttx           Calculate SHA1 hash values from ttx dump of XML (default = font binary)
#   -s, --stdout        Stream to standard output stream (default = write to working dir as 'checksum.txt')
#   -c, --check         Test SHA1 checksum values against a valid checksum file
#
# Options, --ttx only:
#   -e, --exclude       Excluded OpenType table (may be used more than once, mutually exclusive with -i)
#   -i, --include       Included OpenType table (may be used more than once, mutually exclusive with -e)
#   -n, --noclean       Do not discard .ttx files that are used to calculate SHA1 hashes
#-----------------------------------------------------------------------------------------------------------

import argparse
import hashlib
import os
import sys

from os.path import basename

from fontTools.ttLib import TTFont


def write_checksum(filepaths, stdout_write=False, use_ttx=False, include_tables=None, exclude_tables=None, do_not_cleanup=False):
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
            # important to keep the newlinestr value defined here as hash values will change across platforms
            # if platform specific newline values are assumed
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

        file_contents = _read_binary(checksum_path)

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


def check_checksum(filepaths):
    check_failed = False
    for path in filepaths:
        if not os.path.exists(path):
            sys.stderr.write("[checksum.py] ERROR: " + path + " is not a valid filepath" + os.linesep)
            sys.exit(1)

        with open(path, mode='r') as file:
            for line in file.readlines():
                cleaned_line = line.rstrip()
                line_list = cleaned_line.split(" ")
                # eliminate empty strings parsed from > 1 space characters
                line_list = list(filter(None, line_list))
                if len(line_list) == 2:
                    expected_sha1 = line_list[0]
                    test_path = line_list[1]
                else:
                    sys.stderr.write("[checksum.py] ERROR: failed to parse checksum file values" + os.linesep)
                    sys.exit(1)

                if not os.path.exists(test_path):
                    print(test_path + ": Filepath is not valid, ignored")
                else:
                    file_contents = _read_binary(test_path)
                    observed_sha1 = hashlib.sha1(file_contents).hexdigest()
                    if observed_sha1 == expected_sha1:
                        print(test_path + ": OK")
                    else:
                        print("-" * 80)
                        print(test_path + ": === FAIL ===")
                        print("Expected vs. Observed:")
                        print(expected_sha1)
                        print(observed_sha1)
                        print("-" * 80)
                        check_failed = True

    # exit with status code 1 if any fails detected across all tests in the check
    if check_failed is True:
        sys.exit(1)


def _read_binary(filepath):
    with open(filepath, mode='rb') as file:
        return file.read()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="checksum.py")
    parser.add_argument("-t", "--ttx", help="Calculate from ttx file", action="store_true")
    parser.add_argument("-s", "--stdout", help="Write output to stdout stream", action="store_true")
    parser.add_argument("-n", "--noclean", help="Do not discard *.ttx files used to calculate SHA1 hashes", action="store_true")
    parser.add_argument("-c", "--check", help="Verify checksum values vs. files", action="store_true")
    parser.add_argument("filepaths", nargs="+", help="One or more file paths to font binary files")

    parser.add_argument("-i", "--include", action="append", help="Included OpenType tables for ttx data dump")
    parser.add_argument("-e", "--exclude", action="append", help="Excluded OpenType tables for ttx data dump")

    args = parser.parse_args(sys.argv[1:])

    if args.check is True:
        check_checksum(args.filepaths)
    else:
        write_checksum(args.filepaths, stdout_write=args.stdout, use_ttx=args.ttx, do_not_cleanup=args.noclean, include_tables=args.include, exclude_tables=args.exclude)
