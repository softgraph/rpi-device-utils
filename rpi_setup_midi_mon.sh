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
        if [ -f local/midi-mon/midi_mon.${host}.pl ] ; then
            echo "--- ${target} ---"
            ssh ${target} " \
                mkdir -p ~/.config/systemd/user ; \
                mkdir -p ~/local/midi-mon && \
                systemctl --user stop midi_mon ; \
                systemctl --user disable midi_mon ; \
                pkill -f 'perl .*/midi_mon\.pl' \
            "
            scp local/midi-mon/aconnect_x               ${target}:local/midi-mon/
            scp local/midi-mon/midi_mon.${host}.pl      ${target}:local/midi-mon/midi_mon.pl
            scp local/midi-mon/midi_mon.${host}.service ${target}:local/midi-mon/midi_mon.service
            ssh ${target} " \
                chmod +x ~/local/midi-mon/aconnect_x ; \
                chmod +x ~/local/midi-mon/*.pl ; \
                cd ~/.config/systemd/user && \
                ln -fs ~/local/midi-mon/midi_mon.service . ; \
                loginctl enable-linger ${user} ; \
                systemctl --user enable midi_mon ; \
                systemctl --user start midi_mon \
            "
            ssh ${target} " \
                ps -x -o pid,ppid,user,cmd | \
                grep -v grep | \
                egrep 'perl .*/midi_mon\.pl' \
            "
        fi
    fi
}

source rpi__main.sh
