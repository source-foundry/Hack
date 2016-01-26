#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  ------------------------------------------------------------------------------
#  font-tables.py
#  Copyright 2015 Christopher Simpkins
#  MIT license
#  ------------------------------------------------------------------------------

import sys
import os
import os.path
import hashlib
from fontTools import ttLib

# TODO: expand Python objects within the table values
# TODO: modify TTFA table read to create YAML format from the strings


def main(fontpaths):
    """The main function creates a YAML formatted report on the OpenType tables in one
    or more fonts included in the fontpaths function parameter.
    :param fontpaths: """

    # create a report directory, gracefully fail if it already exists
    if not os.path.isdir("otreports"):
        os.mkdir("otreports")

    # iterate through fonts requested in the command
    for fontpath in fontpaths:

        if os.path.isfile(fontpath):
            # create a fonttools TTFont object using the fontpath
            tt = ttLib.TTFont(fontpath)
            print("Processing " + fontpath + "...")

            # define the outfile path
            basename = os.path.basename(fontpath)
            basefilename = basename + "-TABLES.yaml"
            outfilepath = os.path.join("otreports", basefilename)

            # read the font data and create a SHA1 hash digest for the report
            fontdata = read_bin(fontpath)
            hash_digest = hashlib.sha1(fontdata).hexdigest()

            # report strings for file name and SHA1 digest
            report_header_string = "FILE: " + fontpath + "\n"
            report_header_string += "SHA1: " + hash_digest + "\n\n"

            # open outfile write stream, create file, write name + SHA1 header
            with open(outfilepath, "w") as writer:
                writer.write(report_header_string)

            # iterate through the OpenType tables, write table fields in a newline delimited format with YAML syntax
            for table in tt.keys():
                table_dict = tt[table].__dict__
                if len(table_dict) > 0:
                    table_string = yaml_formatter(table, table_dict)
                    with open(outfilepath, 'a') as appender:
                                appender.write(table_string)
                    print("[✓] " + table)
                else:
                    print("[E] " + table)  # indicate missing table data in standard output, do not write to YAML file
            print(fontpath + " table report is available in " + outfilepath + "\n")
        else:  # not a valid filepath
            sys.stderr.write("Error: '" + fontpath + "' was not found. Please check the filepath.\n\n")


def yaml_formatter(table_name, table_dict):
    """Creates a YAML formatted string for OpenType table font reports"""
    # define the list of tables that require table-specific processing
    special_table_list = ['name', 'OS/2', 'TTFA']
    if table_name in special_table_list:
        if table_name == "name":
            return name_yaml_formatter(table_dict)
        elif table_name == "OS/2":
            return os2_yaml_formatter(table_dict)
        elif table_name == "TTFA":
            return ttfa_yaml_formatter(table_dict)
    else:
        table_string = table_name.strip() + ": {\n"
        for field in table_dict.keys():
            table_string = table_string + (" " * 4) + field + ": " + str(table_dict[field]) + ',\n'
        table_string += "}\n\n"
        return table_string


def name_yaml_formatter(table_dict):
    """Formats the YAML table string for OpenType name tables"""
    table_string = "name: {\n"
    namerecord_list = table_dict['names']
    for record in namerecord_list:
        if record.__dict__['langID'] == 0:
            record_name = str(record.__dict__['nameID'])
        else:
            record_name = str(record.__dict__['nameID']) + "u"
        record_field = (" " * 4) + "nameID" + record_name
        table_string = table_string + record_field + ": " + str(record.__dict__) + ",\n"
    table_string = table_string + "}\n\n"
    return table_string


def os2_yaml_formatter(table_dict):
    """Formats the YAML table string for OpenType OS/2 tables"""
    table_string = "OS/2: {\n"
    for field in table_dict.keys():
        if field == "panose":
            table_string = table_string + (" "*4) + field + ": {\n"
            panose_string = ""
            panose_dict = table_dict['panose'].__dict__
            for panose_field in panose_dict.keys():
                panose_string = panose_string + (" " * 8) + panose_field[1:] + ": " + str(panose_dict[panose_field]) + ",\n"
            table_string = table_string + panose_string + (" " * 4) + "}\n"
        else:
            table_string = table_string + (" "*4) + field + ": " + str(table_dict[field]) + ',\n'
    table_string = table_string + "}\n\n"
    return table_string


def ttfa_yaml_formatter(table_dict):
    """Formats the YAML table string for the ttfautohint TTFA table"""
    data_string = table_dict['data'].strip()
    data_list = data_string.split('\n')  # split on newlines in the string
    table_string = "TTFA: {\n"
    for definition_string in data_list:
        definition_list = definition_string.split("=")
        field = definition_list[0].strip()
        if len(definition_list) > 1:
            value = definition_list[1].strip()
        else:
            value = "''"
        table_string = table_string + (" " * 4) + field + ": " + value + ",\n"
    table_string = table_string + "}\n\n"
    return table_string


def read_bin(filepath):
    """read_bin function reads filepath parameter as binary data and returns raw binary to calling code"""
    try:
        with open(filepath, 'rb') as bin_reader:
            data = bin_reader.read()
            return data
    except Exception as e:
        sys.stderr.write("Error: Unable to read file " + filepath + ". " + str(e))


if __name__ == '__main__':
    main(sys.argv[1:])
