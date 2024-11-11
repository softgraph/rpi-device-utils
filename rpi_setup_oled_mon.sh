#! /bin/bash

#---------------------------------------
# Setup `~/local/oled-mon/oled_mon.py` on hosts.
#
# [USAGE]
#   - `./rpi_setup_oled_mon.sh [OPTIONS]`
#
# [OPTIONS]
#   - `-s TAGETS_FILE`
#     or
#     `-t USER@HOSTNAME`
#   - If neither `-s` or `-t` is given, `targets` file is used instead.
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
        if [ -f local/oled-mon/oled_mon.${host}.py ] ; then
            echo "--- ${target} ---"
            ssh ${target} "mkdir -p local/oled-mon && pkill -f '/home/pi/venv/luma/bin/python local/oled-mon/oled_mon.py'"
            scp local/oled-mon/demo_opts.py        ${target}:local/oled-mon/
            scp local/oled-mon/oled_mon.${host}.py ${target}:local/oled-mon/oled_mon.py
            ssh ${target} "~/venv/luma/bin/python local/oled-mon/oled_mon.py > /dev/null 2>&1 & ps -e -o pid,cmd | grep -v 'grep' | grep 'oled_mon.py'"
        fi
    fi
}

source rpi__main.sh