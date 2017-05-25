#! /usr/bin/env python

import extargsparse
import time
import sys
import os
import pandas as pd
import logging

def _insert_path(path,*args):
    _curdir = os.path.join(path,*args)
    if _curdir  in sys.path:
        sys.path.remove(_curdir)
    sys.path.insert(0,_curdir)
    return

_insert_path(os.path.dirname(os.path.realpath(__file__)))

import tushare as ts

from cmnfile import set_logging

def get_list_data(infile=None):
	data = None
	if infile is None:
		data = ts.get_today_all()
	else:
		data = pd.read_csv(infile,encoding='gbk')
	return data

def list_handler(args,parser):
	set_logging(args)
	data = get_list_data(args.input)
	for c in data.columns:
		s = repr(c)
		sys.stdout.write('%s'%(s))
	sys.exit(0)
	return

def dump_handler(args,parser):
	set_logging(args)
	if args.output is None:
		raise Exception('please specify cvs file')
	data = get_list_data(args.input)
	data.to_csv(args.output)
	sys.exit(0)
	return

def code_handler(args,parser):
	set_logging(args)
	data = get_list_data(args.input)
	allcodes = []
	for c in data.code:
		cv = '%06d'%(c)
		allcodes.append(cv)
	sys.stdout.write('%s\n'%(repr(allcodes)))		
	sys.exit(0)
	return


def main():
	command='''
	{
		"verbose|v" : "+",
		"date|d" : null,
		"output|o" : null,
		"input|i" : null,
		"list<list_handler>" : {
			"$" : 0
		},
		"dump<dump_handler>" : {
			"$" : 0
		},
		"code<code_handler>" : {
			"$" : 0
		}
	}
	'''
	parser = extargsparse.ExtArgsParse()
	parser.load_command_line_string(command)
	args = parser.parse_command_line(None,parser)
	raise Exception('[%s] not supported'%(args.subcommand))
	return

if __name__ == '__main__':
	main()