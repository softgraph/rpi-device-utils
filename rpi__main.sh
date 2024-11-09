#! /bin/bash

#---------------------------------------
# The main component for `rpi_xxx.sh` scripts.
#
# [USAGE]
# - `function begin_proc { ... }` # called as `begin_proc`
# - `function end_proc { ... }`   # called as `end_proc`
# - `function do_proc { ... }`    # called as `do_proc ${target} $*`
# - `source rpi__main.sh`
#---------------------------------------

set -u

targets=''

if [ $# -ge 2 ] && [ $1 = '-t' ] ; then
    targets=$2
    shift 2
fi

if [ $# -ge 2 ] && [ $1 = '-s' ] ; then
    targets=`cat $2`
    shift 2
fi

if [ "${targets}" = '' ] ; then
    targets=`cat targets`
fi

begin_proc

for target in ${targets} ; do
    do_proc ${target} $*
done

end_proc
