#! /bin/bash

#---------------------------------------
# Setup `~/local/midi-mon/midi_mon.sh` on hosts.
#
# [USAGE]
#   - `./rpi_setup_midi_mon.sh [OPTIONS]`
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
        user=${target%@*}
        host=${target#*@}
        if [ -f local/midi-mon/midi_mon.${host}.sh ] ; then
            echo "--- ${target} ---"
            ssh ${target} "mkdir -p local/midi-mon && pkill -f '/bin/bash ./midi_mon.sh'"
            scp local/midi-mon/aconnect_x.pl       ${target}:local/midi-mon/
            scp local/midi-mon/midi_mon.${host}.sh ${target}:local/midi-mon/midi_mon.sh
            ssh ${target} "sh -c 'cd local/midi-mon && chmod +x *.sh *.pl && nohup ./midi_mon.sh > /dev/null 2>&1 < /dev/null &'"
            ssh ${target} "ps -x -o pid,ppid,user,cmd | grep -v grep | egrep '${user} +/bin/bash \./midi_mon\.sh'"
        fi
    fi
}

source rpi__main.sh
