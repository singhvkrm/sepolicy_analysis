#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# (C) Copyright 2016 Vit Mojzis, vmojzis@redhat.com
# 
# This program is distributed under the terms of the GNU General Public License
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import sys
import policy_data_collection as data
import domain_grouping as grouping
import graph_builder as builder

# parse comma separated list of [boolean_name]:[on/off] 
def parse_bool_config(bool_arg):
	bool_config = {}
	for boolean in bool_arg.split(","):
		b = boolean.split(":")
		if len(b) >= 2:
			bool_config[b[0]] = 1 if (b[1] == "on") else 0
	#print("Bool config:\n", bool_config, "\n", bool_arg)
	return bool_config


parser = argparse.ArgumentParser(description='SELinux policy analysis tool - graph builder.')

parser.add_argument("filename", metavar="FILENAME", help="Name for the new policy graph file.")

parser.add_argument("-dg", "--domain_grouping", action="store_true", dest="domain_grouping",
                  help="Group SELinux domains based on package they belong to. \
                  		Use with caution, generates false positives!")

parser.add_argument("-fb", "--filter_bools", nargs="?", dest="filter_bools", const="",
                  help="Filter rules based on current boolean setting \
                  	    (or boolean config file or comma separated list of [boolean]:[on/off]).")

parser.add_argument("-c", "--class", dest="classes",
                  help="Comma separated list of object classes to be present \
                  		in the graph. All classes assumed if ommited.")

parser.add_argument("-p", "--policy", dest="policy", help="Path to the SELinux policy to be used.", nargs="?")


args = parser.parse_args()

# split list attributes
if args.classes:
	args.classes = args.classes.split(",")

if args.filter_bools != None:
	args.filter_bools = parse_bool_config(args.filter_bools)

builder.build_graph(args.policy, args.domain_grouping, args.filename, args.classes, args.filter_bools)


