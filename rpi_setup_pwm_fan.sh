#! /bin/bash

#---------------------------------------
# Setup `/boot/firmware/overlays/pwm-fan.dtbo` on hosts.
#
# [USAGE]
#   - `./rpi_setup_pwm_fan.sh [OPTIONS]`
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
        host=${target#*@}
        if [ -f local/pwm-fan/pwm-fan.${host}.dts ] ; then
            echo "--- ${target} ---"
            ssh ${target} " \
                mkdir -p local/pwm-fan \
            "
            scp local/pwm-fan/pwm-fan.${host}.dts ${target}:local/pwm-fan/pwm-fan.dts
            ssh ${target} " \
                grep dtoverlay=pwm-fan /boot/firmware/config.txt > /dev/null ; \
                if [ \$? -eq 1 ] ; then \
                    echo [ERROR] Add the following line to \'${host}:/boot/firmware/config.txt\'. ; \
                    echo dtoverlay=pwm-fan ; \
                else \
                    cd local/pwm-fan && \
                    cpp -nostdinc -undef -x assembler-with-cpp -I /usr/src/linux-headers-6.6.51+rpt-common-rpi/include/ -I /usr/src/linux-headers-6.6.47+rpt-common-rpi/include/ -o pwm-fan.tmp.dts pwm-fan.dts && \
                    dtc -O dtb -o pwm-fan.dtbo pwm-fan.tmp.dts && \
                    sudo cp pwm-fan.dtbo /boot/firmware/overlays/ && \
                    ls -l /boot/firmware/overlays/pwm-fan.dtbo && \
                    sudo reboot ; \
                fi \
            "
        fi
    fi
}

source rpi__main.sh
