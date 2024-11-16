#! /bin/bash

#----------------------------------------
# MIDI Device Monitor and Automatic Connector
#
# [USAGE]
# - `midi_mon.sh &`
#
# [NOTE]
# - Edit `S_AUTO_CONNECT_SRC` and `S_AUTO_CONNECT_DST` below to enable automatic connector.
#----------------------------------------

D_TMP=/var/tmp/local/
F_MON="${D_TMP}midi-mon.txt"
F_CON="${D_TMP}midi-con.txt"

S_AUTO_CONNECT_SRC="MPK mini 3 MIDI 1"
S_AUTO_CONNECT_DST="U2MIDI Pro MIDI 1"

mkdir -p $D_TMP

while true ; do
	./aconnect_x.pl | tee "$F_MON" | awk '/^Conn / { sub("^Conn ", ""); print }' - > "$F_CON"
	if [ ! -s $F_CON ] ; then
		P_SRC=`awk '/Out  [0-9]+:[0-9]+ '"$S_AUTO_CONNECT_SRC"'/ { print $2 }' $F_MON`
		P_DST=`awk '/In   [0-9]+:[0-9]+ '"$S_AUTO_CONNECT_DST"'/ { print $2 }' $F_MON`
		if [ -n "$P_SRC" ] && [ -n "$P_DST" ] ; then
			#echo aconnect "$P_SRC" "$P_DST"
			aconnect "$P_SRC" "$P_DST"
			./aconnect_x.pl | tee "$F_MON" | awk '/^Conn / { sub("^Conn ", ""); print }' - > "$F_CON"
		fi
	fi
	sleep 10s
done
