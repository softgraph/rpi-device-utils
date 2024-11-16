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
        if [ -f local/midi-mon/midi_mon.${host}.pl ] ; then
            echo "--- ${target} ---"
            ssh ${target} "mkdir -p local/midi-mon && pkill -f 'perl ./midi_mon.pl'"
            scp local/midi-mon/aconnect_x.pl       ${target}:local/midi-mon/
            scp local/midi-mon/midi_mon.${host}.pl ${target}:local/midi-mon/midi_mon.pl
            ssh ${target} "sh -c 'cd local/midi-mon && chmod +x *.pl && nohup ./midi_mon.pl > /dev/null 2>&1 < /dev/null &'"
            ssh ${target} "ps -x -o pid,ppid,user,cmd | grep -v grep | egrep '${user} +perl \./midi_mon\.pl'"
        fi
    fi
}

source rpi__main.sh
