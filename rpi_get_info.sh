#! /bin/bash

# [USAGE]
# - `rpi_get_info.sh`
#   - Get information of `hosts`.
# - `rpi_get_info.sh HOST_1 HOST_2`
#   - Get information of HOST_1 and HOST_2.

set -u

function begin_proc {
    mkdir -p info.out
}

function end_proc {
    :
}

function do_proc {
    if [ $# -eq 1 ] ; then
        host=$1
        echo "--- ${host} ---"
        for f in info.txt.bash/* ; do
            if [ ! -f $f ] ; then continue ; fi
            script=${f##*/}
            out=info.out/${script}.${host}.txt
            cat $f | ssh pi@${host} bash > $out
            echo "${script}"
        done
        for f in info.csv.bash/* ; do
            if [ ! -f $f ] ; then continue ; fi
            script=${f##*/}
            out=info.out/${script}.${host}.csv
            cat $f | ssh pi@${host} bash > $out
            echo "${script}"
        done
    fi
}

begin_proc

if [ $# -eq 0 ] ; then
    for i in `cat hosts` ; do
        do_proc $i
    done
else
    for i in $* ; do
        do_proc $i
    done
fi

end_proc
