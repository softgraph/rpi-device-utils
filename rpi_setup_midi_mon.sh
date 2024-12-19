#! /bin/bash

#---------------------------------------
# Setup `~/local/midi-mon/midi_mon.sh` on hosts.
#
# [USAGE]
#   - `./rpi_setup_midi_mon.sh [OPTIONS]`
#
# [OPTIONS]
#   - `-s TARGETS_FILE`
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
    if [ $# -eq 1 ] ; then
        target=$1
        user=${target%@*}
        host=${target#*@}
        if [ -f local/midi-mon/midi_mon.${host}.py ] ; then
            echo "--- ${target} ---"
            ssh ${target} " \
                mkdir -p ~/.config/systemd/user ; \
                mkdir -p ~/local/midi-mon && \
                systemctl --user stop midi_mon ; \
                systemctl --user disable midi_mon ; \
                pkill -f 'python midi_mon\.py' \
            "
            scp local/midi-mon/aconnect_ex         ${target}:local/midi-mon/
            scp local/midi-mon/midi_mon.${host}.py ${target}:local/midi-mon/midi_mon.py
            scp local/midi-mon/midi_mon.service    ${target}:local/midi-mon/
            ssh ${target} " \
                chmod +x ~/local/midi-mon/aconnect_ex ; \
                cd ~/.config/systemd/user && \
                ln -fs ~/local/midi-mon/midi_mon.service . ; \
                loginctl enable-linger ${user} ; \
                systemctl --user enable midi_mon ; \
                systemctl --user start midi_mon \
            "
            ssh ${target} " \
                ps -x -o pid,ppid,user,cmd | \
                grep -v grep | \
                egrep 'python midi_mon\.py' \
            "
        fi
    fi
}

source rpi__main.sh
