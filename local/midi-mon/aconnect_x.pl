#! /usr/bin/env perl

#----------------------------------------
# Extend `aconnect`.
#
# [USAGE]
# - `aconnect_x.pl [OPTIONS]`
#   - Print formatted output of `aconnect -l`.
#
# [OPTIONS]
# - `-v`: Enable verbose output.
#----------------------------------------

#----------------------------------------
# [NOTE for `aconnect`]
# - `aconnect` is an ALSA utility to connect or disconnect MIDI input and output ports.
# - `aconnect -l` prints:
#   - A) Client (device) Information
#     - "client %d: '%s' [type=user" or
#       "client %d: '%s' [type=kernel" (%d: client_id, %s: client_name)
#     - [ ",card=%d" ] (if available, %d: card_number)
#     - [ ",pid=%d" ] (if available, %d: pid)
#     - "]\n" 
#   - B) Port Information
#     - "  %3d '%-16s'\n" (%d: port_id, %s: port_name)
#   - C) Connection Information
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
#   - Note `aconnect -i` or `aconnect -o` also print A and B for input or output ports.
# - For the details, see:
#   - An `aconnect.c` version that may be included in Raspberry Pi OS
#     - <https://github.com/alsa-project/alsa-utils/blob/ccc108fb83bf31d6995c80ba9716ef3760f49637/seq/aconnect/aconnect.c>
#   - or the latest one
#     - <https://github.com/alsa-project/alsa-utils/blob/master/seq/aconnect/aconnect.c>
#----------------------------------------

use strict;
use warnings;

#----------------------------------------
# Constants
#----------------------------------------

my $pattern_device = q|
	^
	\s*
	client			# keyword
	\s*
	( [0-9]+ ) :	# $1: device #
	\s*
	' ( .+ ) '		# $2: device label
	\s*
	( \[ .+ \] )?	# $3: device attributes ([...])
	\s*
	$
|;

my $pattern_port = q|
	^
	\ \ 			# leading whitespaces
	\s*
	( [0-9]+ )		# $1: port #
	\s*
	' ( .+ ) '		# $2: port label
	\s*
	$
|;

my $pattern_conn_to = q|
	^
	\t					# leading tab
	\s*
	Connecting\ To:		# keyword
	\s*
	( .* )				# $1: connections
	\s*
	$
|;

my $pattern_conn_from = q|
	^
	\t					# leading tab
	\s*
	Connected\ From:	# keyword
	\s*
	( .* )				# $1: connections
	\s*
	$
|;

my $pattern_conn_splitter = q|
	,
|;

my $pattern_conn_unit = q|
	^
	\s*
	( [0-9]+ )			# $1: device #
	:
	( [0-9]+ )			# $2: port #
	\s*
	( \[ .+ \] )?		# $3: connection attributes ([...][...]...)
	\s*
	$
|;

#----------------------------------------
# Globl Variables
#----------------------------------------

my $opt_verbose = 0;
my $opt_action_list = 1;	# as a default action

my %map_device = ();
my %map_port_in = ();
my %map_port_out = ();

#----------------------------------------
# Main
#----------------------------------------

check_options();
handle_actions();

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

# Handle actions.
sub handle_actions {
	if ($opt_action_list > 0) {
		# Create maps
		my @list_port_in = `aconnect -i`;
		my @list_port_out = `aconnect -o`;
		create_input_map(@list_port_in);
		create_output_map(@list_port_out);

		# Print all
		my @list_port_con = `aconnect -l`;
		print_header();
		print_maps();
		print_all(@list_port_con);
		print_connections_by_name(@list_port_con);
	}
}

# Create the map for input ports and devices.
sub create_input_map {
	my $client;
	my $port;
	foreach (@_) {
		chomp;
		if (m|$pattern_device|x) {
			$client = $1;
			$map_device{$client} = $2;
		}
		if (m|$pattern_port|x) {
			$port = $1;
			$map_port_in{"$client:$port"} = $2;
		}
	}
}

# Create the map for input ports and devices.
sub create_output_map {
	my $client;
	my $port;
	foreach (@_) {
		chomp;
		if (m|$pattern_device|x) {
			$client = $1;
			$map_device{$client} = $2;
		}
		if (m|$pattern_port|x) {
			$port = $1;
			$map_port_out{"$client:$port"} = $2;
		}
	}
}

# Print header.
sub print_header {
	print "# Dev: Device\n";
	print "# In:  Device's Input Port\n";
	print "# Out: Device's Output Port\n";
	print "# Src: Connected Source Port\n";
	print "# Dst: Connected Destination Port\n";
	print "# Con: Connected Device Names\n";
}

# Print maps.
sub print_maps {
	if ($opt_verbose > 0) {
		foreach my $key (sort keys %map_device) {
			print "+ Dev ${key} = '$map_device{$key}'\n";
		}
		foreach my $key (sort keys %map_port_in) {
			print "+ In  ${key} = '$map_port_in{$key}'\n";
		}
		foreach my $key (sort keys %map_port_out) {
			print "+ Out ${key} = '$map_port_out{$key}'\n";
		}
	}
}

# Print all devices, ports and connections.
sub print_all {
	my $client;
	my $port;
	foreach (@_) {
		chomp;
		if (m|$pattern_device|x)
		{
			$client = $1;
			if (defined $3) {
				print "Dev $1   '$2' $3\n";
			}
			else {
				print "Dev $1   '$2'\n";
			}
		}
		elsif (m|$pattern_port|x)
		{
			$port = $1;
			if (exists($map_port_in{"$client:$port"})) {
				print "In  $client:$port '$2'\n";
			}
			if (exists($map_port_out{"$client:$port"})) {
				print "Out $client:$port '$2'\n";
			}
		}
		elsif (m|$pattern_conn_to|x) {
			my @connections = split(/$pattern_conn_splitter/x, $1);
			foreach (@connections) {
				if (m|$pattern_conn_unit|x) {
					if (defined $3) {
						print "Src $client:$port -> $1:$2 $3\n";
					}
					else {
						print "Src $client:$port -> $1:$2\n";
					}
				}
			}
		}
		elsif (m|$pattern_conn_from|x) {
			my @connections = split(/$pattern_conn_splitter/x, $1);
			foreach (@connections) {
				if (m|$pattern_conn_unit|x) {
					if (defined $3) {
						print "Dst $client:$port <- $1:$2 $3\n";
					}
					else {
						print "Dst $client:$port <- $1:$2\n";
					}
				}
			}
		}
		else {
			if ($opt_verbose > 0) {
				print "+ Unknown: $_\n";
			}
		}
	}
}

# Print connections by name.
sub print_connections_by_name {
	my $client;
	foreach (@_) {
		chomp;
		if (m|$pattern_device|x)
		{
			$client = $1;
		}
		elsif (m|$pattern_conn_to|x) {
			my @connections = split(/$pattern_conn_splitter/x, $1);
			foreach (@connections) {
				if (m|$pattern_conn_unit|x) {
					print "Con $map_device{$client} -> $map_device{$1}\n";
				}
			}
		}
	}
}

#----------------------------------------
