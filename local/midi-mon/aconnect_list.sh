#! /bin/bash

#----------------------------------------
# List `aconnect -l` outputs.
#
# [USAGE]
# - `aconnect_list.sh`
#
# [NOTE for `aconnect`]
# - `aconnect` is an ALSA utility to connect / disconnect two MIDI devices.
# - `aconnect -l` prints:
#   - 1) Client Information
#     - "client %d: '%s' [type=user" or
#       "client %d: '%s' [type=kernel" (%d: client_id, %s: client_name)
#     - [ ",card=%d" ] (if available, %d: card_number)
#     - [ ",pid=%d" ] (if available, %d: pid)
#     - "]\n" 
#   - 2) Port Information
#     - "  %3d '%-16s'\n" (%d: port_id, %s: port_name)
#   - 3) Connection Information
#     - "\tConnecting To: " or
#       "\tConnected From: "
#     - {
#       - "%d:%d" ( %d: client_id, %d: port_id )
#       - [ "[ex]" ] (if connected with '--exclusive')
#       - [ "[real:%d]" ] (if connected with '--real', %d: real_queue)
#       - [ "[tick:%d]" ] (if connected with '--tick', %d: tick_queue)
#       - [ ", " ] ()
#     - } x 1..n
#     - "\n"
# - For the details, see:
#   - An `aconnect.c` version that may be included in Raspberry Pi OS
#     - <https://github.com/alsa-project/alsa-utils/blob/ccc108fb83bf31d6995c80ba9716ef3760f49637/seq/aconnect/aconnect.c>
#   - or the latest one
#     - <https://github.com/alsa-project/alsa-utils/blob/master/seq/aconnect/aconnect.c>
#----------------------------------------

D_TMP=/var/tmp/local/
F_TMP_0="${D_TMP}aconnect_list.$$.0"
F_TMP_1="${D_TMP}aconnect_list.$$.1"
F_TMP_2="${D_TMP}aconnect_list.$$.2"

mkdir -p "${D_TMP}"

aconnect -l > "${F_TMP_0}"

# List clients (`C`) and ports (`P`).
awk ' \
	$1 == "client" { \
		client = $2; \
		$1 = "C"; $2 = $2 " "; print \
	} \
	/   +[0-9]/ { \
		$1 = "P " client $1; print \
	} \
' "${F_TMP_0}" > "${F_TMP_1}"

# List connections (`T` or `F`).
awk ' \
	$1 == "client" { \
		client = $2 \
	} \
	/   +[0-9]/ { \
		port = $1 \
	} \
	/	Connecting To:/ { \
		$1 = "T " client port; $2 = "->"; print \
	} \
	/	Connected From:/ { \
		$1 = "F " client port; $2 = "<-"; print \
	} \
' "${F_TMP_0}" >> "${F_TMP_1}"

# List connections with port names (`t` or `f`).
awk ' \
	$1 == "P" { \
		port = $2; \
		$1 = ""; $2 = ""; port_name = $0; \
		sub("  ", "", port_name); \
		port_map[port] = port_name; \
	} \
	$1 == "T" { \
		gsub("\[.*\]", "", $2); \
		gsub("\[.*\]", "", $4); \
		print "t", port_map[$2], $3, port_map[$4]; \
	} \
	$1 == "F" { \
		gsub("\[.*\]", "", $2); \
		gsub("\[.*\]", "", $4); \
		print "f", port_map[$2], $3, port_map[$4]; \
	} \
' "${F_TMP_1}" > "${F_TMP_2}"

# Print all.
echo "--- C: Client, P: Port, T/t: Port Connected To, F/f: Port Connected From ---"
cat "${F_TMP_1}"
cat "${F_TMP_2}"

# Remove temporary files.
rm -f "${F_TMP_0}" "${F_TMP_1}" "${F_TMP_2}"
