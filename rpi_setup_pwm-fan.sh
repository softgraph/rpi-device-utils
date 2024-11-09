#! /bin/bash

#---------------------------------------
# Setup `pwm-fan` on hosts.
#
# [USAGE]
#   - `./rpi_setup_pwm-fan.sh [OPTIONS]`
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
        if [ -f local/pwm-fan/pwm-fan.${host}.dts ] ; then
            echo "--- ${target} ---"
            ssh ${target} "mkdir -p local/pwm-fan"
            scp local/pwm-fan/pwm-fan.${host}.dts ${target}:local/pwm-fan/pwm-fan.dts
            ssh ${target} "cd local/pwm-fan && cpp -nostdinc -undef -x assembler-with-cpp -I /usr/src/linux-headers-6.6.51+rpt-common-rpi/include/ -I /usr/src/linux-headers-6.6.47+rpt-common-rpi/include/ -o pwm-fan.tmp.dts pwm-fan.dts && dtc -O dtb -o pwm-fan.dtbo pwm-fan.tmp.dts && sudo cp pwm-fan.dtbo /boot/firmware/overlays/ && ls -l /boot/firmware/overlays/pwm-fan.dtbo && sudo reboot"
        fi
    fi
}

source rpi__main.sh
