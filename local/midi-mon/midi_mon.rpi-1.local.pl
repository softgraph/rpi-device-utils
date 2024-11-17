#! /usr/bin/env perl

#----------------------------------------
# MIDI Device Monitor and Automatic Connector
#
# [USAGE]
# - `midi_mon.pl &`
#
# [REQUIREMENT]
# - `aconnect_x.pl`
#
# [NOTE]
# - Edit the following lines to enable automatic connector.
#   - `$S_AUTO_CONNECT_SRC`: The name of the source port.
#   - `$S_AUTO_CONNECT_DST`: The name of the destination port.
#   - `$S_AUTO_CONNECT_OPT`: Option for the `aconnect` command.
# - Run `aconnect` and `aconnect -l` for the details.
#----------------------------------------

use strict;
use warnings;
use File::Path qw(make_path);

#----------------------------------------
# Configurations
#----------------------------------------

my $S_AUTO_CONNECT_SRC = 'MPK mini 3 MIDI 1';
my $S_AUTO_CONNECT_DST = 'U2MIDI Pro MIDI 1';
my $S_AUTO_CONNECT_OPT = '';

#----------------------------------------
# Constants
#----------------------------------------

my $d_tmp = "/var/tmp/local/";
my $f_mon = "${d_tmp}midi-mon.txt";
my $f_con = "${d_tmp}midi-con.txt";

#----------------------------------------
# Globl Variables
#----------------------------------------

my $opt_verbose = 0;
my @list_midi;

#----------------------------------------
# Main
#----------------------------------------

check_options();
run_loop();

#----------------------------------------
# Functions
#----------------------------------------

# Check options.
sub check_options {
	foreach (@ARGV) {
		if (m|^-v$|) {
			$opt_verbose += 1;
		}
		elsif (m|^-vv$|) {
			$opt_verbose = 2;
		}
		elsif (m|^-vvv$|) {
			$opt_verbose = 3;
		}
	}
}

# Run loop.
sub run_loop {
	while (1) {
		update_midi_device_list();
		if (export_midi_connection_list() == 0) {
			my $p_src;
			my $p_dst;
			foreach (@list_midi) {
				if (m|^Out ([0-9]+:[0-9]+) '$S_AUTO_CONNECT_SRC'$|) {
					$p_src = $1;
				}
				elsif (m|^In  ([0-9]+:[0-9]+) '$S_AUTO_CONNECT_DST'$|) {
					$p_dst = $1;
				}
			}
			if (defined $p_src and defined $p_dst) {
				system("aconnect $S_AUTO_CONNECT_OPT $p_src $p_dst");
				update_midi_device_list();
				export_midi_connection_list();
			}
		}
		sleep(10); # seconds
	}
}

# Update midi device list.
sub update_midi_device_list {
	@list_midi = `./aconnect_x.pl`;
}

# Export midi connection list.
sub export_midi_connection_list {
	my $count = 0;
	make_path($d_tmp);
	open(my $file, ">", $f_con) or do {
		if ($opt_verbose > 0) {
			warn "+ WARNING: open() failed for '$f_con'";
		}
		return $count;
	};
	foreach (@list_midi) {
		if (s|^Con ||) {
			print $file $_;
			$count++;
		}
	}
	close($file);
	return $count;
}

#----------------------------------------
