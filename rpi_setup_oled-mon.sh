#! /bin/bash

#---------------------------------------
# Setup `oled-mon` on hosts.
#
# [USAGE]
#   - `./rpi_setup_oled-mon.sh [OPTIONS]`
#
# [OPTIONS]
#   - `-t HOSTNAME`
#     or
#     `-t USER@HOSTNAME`
#   - If `-t` option is not specified, `targets` file is used instead.
#---------------------------------------

set -u

function begin_proc {
    :
}

function end_proc {
    :
}

function do_proc {
    if [ $# -eq 1 ]
    then
        target=$1
        host=${target#*@}
        if [ -f local/oled-mon/oled-mon.${host}.py ] ; then
            echo "--- ${target} ---"
            ssh ${target} "mkdir -p local/oled-mon && pkill -f '/home/pi/venv/luma/bin/python local/oled-mon/oled-mon.py'"
            scp local/oled-mon/demo_opts.py        ${target}:local/oled-mon/
            scp local/oled-mon/oled-mon.${host}.py ${target}:local/oled-mon/oled-mon.py
            ssh ${target} "~/venv/luma/bin/python local/oled-mon/oled-mon.py &"
        fi
    fi
}

source rpi__main.sh
