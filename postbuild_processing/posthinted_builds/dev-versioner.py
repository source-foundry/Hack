#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  ------------------------------------------------------------------------------
#  dev-versioner.py
#  Copyright 2016 Christopher Simpkins
#  MIT license
#  ------------------------------------------------------------------------------

import sys
from fontTools import ttLib

VERSION_STRING="Version 2.020;DEV-03172016;"
SUCCESS_INDICATOR = 0

def main(argv):
    for font_variant_path in argv:
        tt = ttLib.TTFont(font_variant_path)
        namerecord_list = tt['name'].__dict__['names']
        for record in namerecord_list:
            if record.__dict__['langID'] == 0:
                if record.__dict__['nameID'] == 5:
                    record.__dict__['string'] = VERSION_STRING

                    path_list = font_variant_path.split(".")
                    outfile_path = path_list[0] + "-DEV." + path_list[1]
                    tt.save(outfile_path)
                    SUCCESS_INDICATOR = 1

                    print("Updated '" + font_variant_path + "' version string to " + VERSION_STRING)

        if SUCCESS_INDICATOR == 0:
            print("Unable to complete the name table update for " + font_variant_path)


if __name__ == '__main__':
    main(sys.argv[1:])

