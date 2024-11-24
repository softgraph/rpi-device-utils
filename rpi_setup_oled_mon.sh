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
    if [ $# -eq 1 ] ; then
        target=$1
        user=${target%@*}
        host=${target#*@}
        if [ -f local/oled-mon/oled_mon.${host}.py ] ; then
            echo "--- ${target} ---"
            ssh ${target} " \
                mkdir -p ~/local/oled-mon ; \
                systemctl --user stop oled_mon ; \
                pkill -f 'python oled_mon\.py' \
            "
            scp local/oled-mon/demo_opts.py             ${target}:local/oled-mon/
            scp local/oled-mon/oled_mon.${host}.py      ${target}:local/oled-mon/oled_mon.py
            scp local/oled-mon/oled_mon.${host}.service ${target}:local/oled-mon/oled_mon.service
            ssh ${target} " \
                mkdir -p ~/.config/systemd/user ; \
                cd ~/.config/systemd/user && \
                ln -fs ~/local/oled-mon/oled_mon.service . ; \
                systemctl --user enable oled_mon && \
                systemctl --user start oled_mon \
            "
            ssh ${target} " \
                ps -x -o pid,ppid,user,cmd | \
                grep -v grep | \
                egrep 'python oled_mon\.py' \
            "
        fi
    fi
}

source rpi__main.sh
