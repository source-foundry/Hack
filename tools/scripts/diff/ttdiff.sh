#!/bin/bash

# Copyright 2018 Source Foundry Authors
# MIT License

# compare fonts with ttx
ttdiff () {
    if [ "$#" -lt 2 ]
    then
        echo "Usage: ttdiff FONT1.ttf FONT2.ttf [tables ...]"
        return 1
    fi
    first="$1"
    if [ ! -f "$first" ]; then
        echo "File $first not found"
        return 1
    fi
    second="$2"
    if [ ! -f "$second" ]; then
        echo "File $second not found"
        return 1
    fi
    tables=""
    for i in ${@:3}
    do
        if [ ! -z "$i" ]
        then
            table="-t "
            if [ ${#i} -eq 3 ]; then
                # add trailing space to pad tag to four chars
                table+="'"$i" '"
            else
                table+=$i
            fi
            tables+="$table "
        fi
    done
    cmd1="ttx -q -o - $tables \"$first\" 2>/dev/null"
    cmd2="ttx -q -o - $tables \"$second\" 2>/dev/null"
    echo $cmd1
    echo $cmd2
    # colorize output if colordiff is installed
    if `command -v colordiff >/dev/null 2>&1`; then
        diff -u <(eval $cmd1) <(eval $cmd2) | colordiff | less -R
    else
        diff -u <(eval $cmd1) <(eval $cmd2) | less -R
    fi
}

ttdiff "$@"
