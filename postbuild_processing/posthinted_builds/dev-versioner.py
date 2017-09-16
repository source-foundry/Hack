#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  ------------------------------------------------------------------------------
#  dev-versioner.py
#  Copyright 2016 Christopher Simpkins
#  MIT license
#  ------------------------------------------------------------------------------

import sys
from fontTools import ttLib

VERSION_STRING="Version 2.020;DEV-03192016;"

def main(argv):
    success_indicator = 0
    for font_variant_path in argv:
        tt = ttLib.TTFont(font_variant_path)
        namerecord_list = tt['name'].__dict__['names']

        path_list = font_variant_path.split(".")
        outfile_path = path_list[0] + "-DEV." + path_list[1]

        for record in namerecord_list:
            if record.__dict__['langID'] == 0 and record.__dict__['nameID'] == 5:
                record.__dict__['string'] = VERSION_STRING

                tt.save(outfile_path)
                success_indicator += 1

            elif record.__dict__['langID'] == 1033 and record.__dict__['nameID'] == 5:
                record.__dict__['string'] = VERSION_STRING.encode('utf_16_be')  # UTF-16 big endian encoding for the Microsoft tables

                tt.save(outfile_path)
                success_indicator += 1

        if success_indicator == 0:
            print("[ERROR] Unable to complete the name table update for " + font_variant_path)
        elif success_indicator == 1:  # should equal 2 if both name tables were successfully updated
            print("[ERROR] Incomplete name table update for " + font_variant_path)

        success_indicator = 0   # reset success indicator


if __name__ == '__main__':
    main(sys.argv[1:])

