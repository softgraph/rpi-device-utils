#! /bin/bash

#---------------------------------------
# Setup `~/local/disp-mon/disp_mon.py` on hosts.
#
# [USAGE]
#   - `./rpi_setup_disp_mon.sh [OPTIONS]`
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
        if [ -f local/disp-mon/disp_mon.${host}.py ] ; then
            echo "--- ${target} ---"
            ssh ${target} " \
                mkdir -p ~/.config/systemd/user ; \
                mkdir -p ~/local/disp-mon ; \
                systemctl --user stop disp_mon ; \
                systemctl --user disable disp_mon ; \
                pkill -f 'python disp_mon\.py' \
            "
            scp local/disp-mon/demo_opts.py         ${target}:local/disp-mon/
            scp local/disp-mon/disp_contents.py     ${target}:local/disp-mon/
            scp local/disp-mon/disp_device.py       ${target}:local/disp-mon/
            scp local/disp-mon/disp_mon.${host}.py  ${target}:local/disp-mon/disp_mon.py
            scp local/disp-mon/disp_mon.service     ${target}:local/disp-mon/
            scp local/disp-mon/event_mon.py         ${target}:local/disp-mon/
            if [ -f local/disp-mon/midi_mon.${host}.py ] ; then
                scp local/midi-mon/aconnect_ex          ${target}:local/disp-mon/
                scp local/disp-mon/midi_mon.${host}.py  ${target}:local/disp-mon/midi_mon.py
                ssh ${target} " \
                    chmod +x ~/local/disp-mon/aconnect_ex ; \
                "
            fi
            ssh ${target} " \
                cd ~/.config/systemd/user && \
                ln -fs ~/local/disp-mon/disp_mon.service . ; \
                systemctl --user enable disp_mon ; \
                systemctl --user start disp_mon ; \
                loginctl enable-linger ${user} \
            "
            ssh ${target} " \
                ps -x -o pid,ppid,user,cmd | \
                grep -v grep | \
                egrep 'python disp_mon\.py' \
            "
        fi
    fi
}

source rpi__main.sh
