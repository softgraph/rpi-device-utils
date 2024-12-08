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
#   - `$S_AUTO_CONNECT_SRC`: The name of the source device with port number.
#   - `$S_AUTO_CONNECT_DST`: The name of the destination device with port number.
#   - `$S_AUTO_CONNECT_OPT`: Option for the `aconnect` command.
# - Run `aconnect` and `aconnect -l` for the details.
#----------------------------------------

use strict;
use warnings;
use File::Path qw(make_path);

#----------------------------------------
# Configurations
#----------------------------------------

my $S_AUTO_CONNECT_SRC = 'MPK mini 3:0';
my $S_AUTO_CONNECT_DST = 'U2MIDI Pro:0';
my $S_AUTO_CONNECT_OPT = '';

#----------------------------------------
# Constants
#----------------------------------------

my $d_disp_mon = "/var/tmp/local/disp-mon/";
my $f_midi_mon = "${d_disp_mon}midi_mon.txt";

#----------------------------------------
# Globl Variables
#----------------------------------------

my $opt_verbose = 0;
my @midi_device_list;

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
		# Update midi device list
		update_midi_device_list();

		# Check connection
		my $connected = 0;
		foreach (@midi_device_list) {
			if (m|^Con '$S_AUTO_CONNECT_SRC' -> '$S_AUTO_CONNECT_DST'$|) {
				$connected = 1;
				last;
			}
		}

		# Create command if required
		my $command;
		if (not $connected) {
			my $p_src;
			my $p_dst;
			foreach (@midi_device_list) {
				if (m|^Out ([0-9]+:[0-9]+) ('$S_AUTO_CONNECT_SRC') ('.*')$|) {
					$p_src = $2;
				}
				elsif (m|^In  ([0-9]+:[0-9]+) ('$S_AUTO_CONNECT_DST') ('.*')$|) {
					$p_dst = $2;
				}
			}
			if (defined $p_src and defined $p_dst) {
				$command = "aconnect $S_AUTO_CONNECT_OPT $p_src $p_dst";
			}
		}

		# Run command if exists
		if (defined $command) {
			system($command);
			update_midi_device_list();
			export_midi_connection_list($command);
		}
		else {
			export_midi_connection_list();
		}

		# Sleep
		sleep(10); # seconds
	}
}

# Update midi device list.
sub update_midi_device_list {
	@midi_device_list = `~/local/midi-mon/aconnect_x`;
}

# Export midi connection list.
sub export_midi_connection_list {
	my ($line) = @_;
	my $count = 0;
	make_path($d_disp_mon);
	open(my $file, ">", $f_midi_mon) or do {
		if ($opt_verbose > 0) {
			warn "+ WARNING: open() failed for '$f_midi_mon'";
		}
		return $count;
	};
	if ($line) {
		print $file "$line\n";
	}
	else {
		foreach (@midi_device_list) {
			if (m|^Con '(.*)' -> '(.*)'$|) {
				print $file "$1 ->\n";
				print $file "-> $2\n";
			}
			$count++;
		}
	}
	close($file);
	return $count;
}

#----------------------------------------
