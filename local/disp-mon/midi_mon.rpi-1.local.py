#----------------------------------------
# MIDI Monitor
#
# [USAGE]
# - `import midi_mon`
# - `midi_mon.init(_context_name)`
# - `midi_mon.toggle()`
# - `midi_mon.update()`
#----------------------------------------

import collections
import logging
import os
import re
import subprocess

#----------------------------------------
# Non-public Parameters
#----------------------------------------

_D_DISP_MON = "/var/tmp/local/disp-mon/";
_F_DISP_MON = F"{_D_DISP_MON}midi_mon.txt";

_AUTO_CONNECT_SRC_PORT = "MPK mini 3:0"
_AUTO_CONNECT_DST_PORT = "U2MIDI Pro:0"

#----------------------------------------
# Non-public Variables
#----------------------------------------

logging.basicConfig(format = "%(message)s", level = logging.INFO) # configure handler
_logger = logging.getLogger()

_contextName = None

_is_active = True
_is_active_latest = False

_midi_src_ports = collections.deque([])
_midi_dst_ports = collections.deque([])
_midi_con_pairs = collections.deque([])
_midi_con_pairs_latest = collections.deque([])

#----------------------------------------
# Public Functions
#----------------------------------------

def init(context_name):
    global _context_name
    _context_name = context_name

def is_active():
    return _is_active

def toggle():
    if _is_active:
        return deactivate()
    else:
        return activate()

def deactivate():
    global _is_active
    if _is_active:
        _logger.info(f"{_contextName}: MIDI Monitor is deactivated")
        _is_active = False
        _update(force = True)
        return True # To be refreshed
    else:
        return False # No need to be refreshed

def activate():
    global _is_active
    if not _is_active:
        _logger.info(f"{_contextName}: MIDI Monitor is activated")
        _is_active = True
        _update(force = True)
        return True # To be refreshed
    else:
        return False # No need to be refreshed

def update(force = False):
    return _update(force)

#----------------------------------------
# Non-public Functions
#----------------------------------------

def _update(force = False):
    global _is_active_latest
    if not _is_active:
        _update_midi()
        done = _disconnect_midi_all()
        if (force == True or
            done == True or
            _is_active_latest != _is_active):
            _is_active_latest = _is_active
            try:
                os.makedirs(_D_DISP_MON, exist_ok = True)
                with open(_F_DISP_MON, "w") as file:
                    file.write('MIDI: Disabled')
            except (FileNotFoundError, PermissionError):
                pass
            return True # To be refreshed
        else:
            return False # No need to be refreshed
    else:
        _update_midi()
        done = _auto_connect_midi()
        if (force == True or
            done == True or
            _is_active_latest != _is_active or
            not _equals(_midi_con_pairs_latest, _midi_con_pairs)):
            _is_active_latest = _is_active
            _shallow_copy(_midi_con_pairs_latest, _midi_con_pairs)
            try:
                os.makedirs(_D_DISP_MON, exist_ok = True)
                with open(_F_DISP_MON, 'w') as file:
                    for pair in _midi_con_pairs:
                        file.write(f"{pair[0]}  >>>\n")
                        file.write(f"\t\t>>>  {pair[1]}\n")
            except (FileNotFoundError, PermissionError):
                pass
            return True # To be refreshed
        else:
            return False # No need to be refreshed

def _equals(x, y):
    m = len(x)
    if m != len(y):
        return False
    for i in range(m):
        n = len(x[i])
        if n != len(y[i]):
            return False
        for j in range(n):
            if x[i][j] != y[i][j]:
                return False
    return True

def _shallow_copy(dst, src):
    dst.clear()
    for element in src:
        dst.append(element)

def _disconnect_midi_all():
    if len(_midi_con_pairs) > 0:
        _logger.info(f"{_contextName}: Run `aconnect -x`")
        subprocess.run(["aconnect", "-x"])
        _update_midi()
        return True # Done
    else:
        return False # Nop

def _auto_connect_midi():
    auto_connect_required = True
    for pair in _midi_con_pairs:
        if pair[0] == _AUTO_CONNECT_SRC_PORT and pair[1] == _AUTO_CONNECT_DST_PORT:
            auto_connect_required = False
            break
    if auto_connect_required:
        return _connect_midi(_AUTO_CONNECT_SRC_PORT, _AUTO_CONNECT_DST_PORT)
    else:
        return False # Nop

def _connect_midi(src_port, dst_port):
    src_valid = False
    dst_valid = False
    for port in _midi_src_ports:
        if port == src_port:
            src_valid = True
            break
    for port in _midi_dst_ports:
        if port == dst_port:
            dst_valid = True
            break
    if src_valid and dst_valid:
        _logger.info(f"{_contextName}: Run `aconnect '{src_port}' '{dst_port}'`")
        subprocess.run(["aconnect", f"{src_port}", f"{dst_port}"])
        _update_midi()
        return True # Done
    else:
        return False # Nop

def _update_midi():
    _midi_src_ports.clear()
    _midi_dst_ports.clear()
    _midi_con_pairs.clear()
    try:
        process = subprocess.run(["./aconnect_ex"], check = True, text = True, stdout = subprocess.PIPE)
        for line in process.stdout.splitlines():
            # Update MIDI Source (Output) Ports
            match = re.match(r"""
                             ^ Out          # keyword
                             \s+ (.+:.+)    # #1: device number + port number
                             \s+ '(.+)'     # #2: device name + port number
                             \s+ '(.+)'     # #3: port name
                             $
                             """, line, re.X)
            if match:
                _midi_src_ports.append(match.group(2))

            # Update MIDI Destination (Input) Ports
            match = re.match(r"""
                             ^ In           # keyword
                             \s+ (.+:.+)    # #1: device number + port number
                             \s+ '(.+)'     # #2: device name + port number
                             \s+ '(.+)'     # #3: port name
                             $
                             """, line, re.X)
            if match:
                _midi_dst_ports.append(match.group(2))

            # Update MIDI Connected Pairs
            match = re.match(r"""
                             ^ Con          # keyword
                             \s+ '(.+)'     # #1: source device and port
                             \s+ ->         # keyword
                             \s+ '(.+)'     # #2: destination device and port
                             $
                             """, line, re.X)
            if match:
                _midi_con_pairs.append([ match.group(1), match.group(2) ])
    except (subprocess.CalledProcessError):
        pass

#----------------------------------------
