#! /bin/bash

#---------------------------------------
# The main component for `rpi_xxx.sh` scripts.
#
# [USAGE]
# - `function begin_proc { ... }` # called as `begin_proc`
# - `function end_proc { ... }`   # called as `end_proc`
# - `function do_proc { ... }`    # called as `do_proc ${host} ${user} $*`
# - `source rpi__main.sh`
#---------------------------------------

set -u

hosts=''
user='pi'

for i in {1..2} ; do
	if [ $# -ge 2 ] && [ $1 = '-h' ] ; then
		hosts=$2
		shift 2
    elif [ $# -ge 2 ] && [ $1 = '-u' ] ; then
        user=$2
        shift 2
    fi
done

if [ -z ${hosts} ] ; then
    hosts=`cat hosts`
fi

begin_proc

for host in ${hosts} ; do
    do_proc ${host} ${user} $*
done

end_proc
