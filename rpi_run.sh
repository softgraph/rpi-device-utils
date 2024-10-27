#! /bin/bash

#---------------------------------------
# Run a command on hosts.
#
# [EXAMPLE]
#   - `rpi_run.sh ls -l`
#   - `rpi_run.sh -u pi -h rpi-1.local ls -l`
#
# [USAGE]
#   - `rpi_run.sh [OPTIONS] COMMAND ...`
#
# [OPTIONS]
#   - `-h HOSTNAME`
#     - Hostnames given by `cat hosts` are used if no option is given.
#   - `-u USER`
#     - User `pi` is used if no option is given.
#---------------------------------------

set -u

function begin_proc {
    :
}

function end_proc {
    :
}

function do_proc {
    if [ $# -ge 3 ]
    then
        host=$1
        user=$2
        shift 2
        echo "--- ${user}@${host} ---"
        ssh ${user}@${host} $*
    fi
}

source rpi__main.sh
