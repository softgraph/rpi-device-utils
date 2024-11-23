#! /bin/bash

#---------------------------------------
# Run a command on hosts.
#
# [USAGE]
#   - `./rpi_run.sh [OPTIONS] COMMAND ...`
#
# [OPTIONS]
#   - `-s TAGETS_FILE`
#     or
#     `-t USER@HOSTNAME`
#   - If neither `-s` or `-t` is given, `targets` file is used instead.
#
# [EXAMPLE]
#   - `./rpi_run.sh ls -l`
#   - `./rpi_run.sh -t pi@rpi-1.local ls -l`
#---------------------------------------

set -u

function begin_proc {
    :
}

function end_proc {
    :
}

function do_proc {
    if [ $# -ge 2 ] ; then
        target=$1
        shift
        echo "--- ${target} ---"
        ssh ${target} $*
    fi
}

source rpi__main.sh
