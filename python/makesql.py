#! /usr/bin/env python

import extargsparse
import sys
import os
import logging
import re

def _insert_path(path,*args):
    _curdir = os.path.join(path,*args)
    if _curdir  in sys.path:
        sys.path.remove(_curdir)
    sys.path.insert(0,_curdir)
    return

_insert_path(os.path.dirname(os.path.realpath(__file__)))

from cmnfile import set_logging,read_file,write_file

def format_time(s):
	rets = ''
	sarr = re.split('\-',s)
	if len(sarr) >= 3:
		rets = '%s 09:30:00'%(s)
	else:
		try:
			cvalue = int(s)
			sec = cvalue % 100
			cvalue = int(cvalue / 100)
			minute = cvalue % 100
			cvalue = int(cvalue / 100)
			hour = cvalue % 100
			cvalue = int(cvalue / 100)
			day = cvalue % 100
			cvalue = int(cvalue / 100)
			month = cvalue % 100
			cvalue = int(cvalue / 100)
			year = cvalue % 10000
			rets = '%04d-%02d-%02d %02d:%02d:%02d'%(year,month,day,hour,minute,sec)
		except:
			pass
	return rets

def make_insert_sql(sarr,dbname,code):
	outs = ''
	format_time
	if len(sarr) == 6:
		outs += 'insert into %s (code,dt,open,close,high,low,volume) values(\'%s\',\'%s\',%s,%s,%s,%s,%s);\n'%(dbname,code,\
				format_time(sarr[0]),sarr[1],sarr[2],sarr[3],sarr[4],sarr[5])
	return outs


def makeinsert_handler(args,parser):
	set_logging(args)
	if args.code is None or args.dbname is None:
		raise Exception('please specified code or dbname')
	s = read_file(args.input)
	sarr = re.split('\n',s)
	outs = ''
	for l in sarr:
		l = l.rstrip('\r\n')
		barr = re.split(',',l)
		outs += make_insert_sql(barr,args.dbname,args.code)
	write_file(outs,args.output)
	sys.exit(0)
	return


def main():
	command = '''
	{
		"verbose|v" : "+",
		"input|i" : null,
		"output|o" : null,
		"code|c" : null,
		"dbname|d" : null,
		"makeinsert<makeinsert_handler>" : {
			"$" : 0
		}
	}
	'''
	parser = extargsparse.ExtArgsParse()
	parser.load_command_line_string(command)
	args = parser.parse_command_line(None,parser)
	raise Exception('not supported [%s]'%(args.subcommand))
	return

if __name__ == '__main__':
	main()
