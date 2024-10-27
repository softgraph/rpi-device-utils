#! /bin/bash

# [USAGE]
# - `rpi_get_info.sh`
#   - Get information of `hosts`.
# - `rpi_get_info.sh -h HOSTNAME`
#   - Get information of HOSTNAME.

set -u

function begin_proc {
    mkdir -p info.out
}

function end_proc {
    :
}

function do_proc {
    if [ $# -eq 2 ] ; then
        host=$1
        user=$2
        echo "--- ${user}@${host} ---"
        for f in info.txt.bash/* ; do
            if [ ! -f $f ] ; then continue ; fi
            script=${f##*/}
            out=info.out/${script}.${host}.txt
            cat $f | ssh ${user}@${host} bash > $out 2> /dev/null
            echo "${script}"
        done
        for f in info.csv.bash/* ; do
            if [ ! -f $f ] ; then continue ; fi
            script=${f##*/}
            out=info.out/${script}.${host}.csv
            cat $f | ssh ${user}@${host} bash > $out 2> /dev/null
            echo "${script}"
        done
    fi
}

source rpi__main.sh
