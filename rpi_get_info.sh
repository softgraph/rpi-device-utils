#! /bin/bash

#---------------------------------------
# Get information from hosts.
#
# [USAGE]
#   - `./rpi_get_info.sh [OPTIONS]`
#
# [OPTIONS]
#   - `-t HOSTNAME`
#     or
#     `-t USER@HOSTNAME`
#   - If `-t` option is not specified, `targets` file is used instead.
#---------------------------------------

set -u

function begin_proc {
    mkdir -p info.out
}

function end_proc {
    :
}

function do_proc {
    if [ $# -eq 1 ] ; then
        target=$1
        host=${target#*@}
        echo "--- ${target} ---"
        for f in info.txt.bash/* ; do
            if [ ! -f $f ] ; then continue ; fi
            script=${f##*/}
            out=info.out/${script}.${host}.txt
            cat $f | ssh ${target} bash > $out 2> /dev/null
            echo "${script}"
        done
        for f in info.csv.bash/* ; do
            if [ ! -f $f ] ; then continue ; fi
            script=${f##*/}
            out=info.out/${script}.${host}.csv
            cat $f | ssh ${target} bash > $out 2> /dev/null
            echo "${script}"
        done
    fi
}

source rpi__main.sh
