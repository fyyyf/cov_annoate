# -*- coding=utf-8 -*-
# any issue , please contact yuan.fei@mediatek.com

import re
import os
import sys
import getopt
import tkinter as tk

## local
from cov_xml_proc import cov_xml_proc
from cov_doc_proc import cov_doc_proc
from cov_gui	  import cov_gui

debug = 0
version = 0.4


def run(xml_name, doc_name, prefix):
	global debug

	print("#"*50)
	print(f"version={version}")
	print("#"*50)

	#prefix = en_pf.get()
	#print ("PREIFX=%s"%prefix)
	if prefix == '':
		prefix = None
	
	if (xml_name is None) :
		tk.messagebox.showerror('ERROR','xml file not set !')
		return

	if (doc_name is None):
		tk.messagebox.showerror('ERROR','doc file not set !')
		return

	if not os.path.exists(xml_name):
		print (f'ERROR : xml file "{xml_name}" not exist')
		sys.exit()
	if not os.path.exists(doc_name):
		print (f'ERROR : doc file "{doc_name}" not exist')
		sys.exit()

	xml_proc = cov_xml_proc(xml_name, debug)
	cov_dict_all = xml_proc.parser_xml()

	doc_proc = cov_doc_proc(doc_name, debug)
	doc_proc.proc_doc(cov_dict_all, prefix)
	#input("Vplan annotate done ! Press any key to exit")
	print("finish")
	tk.messagebox.showinfo('finish','Vplan annotate done !')

def cmd_mode():
	global debug
	try:
		opts,args = getopt.getopt(sys.argv[1:], 'hd', ['xml=','doc=','prefix='])
	except getopt.GetoptError:
		print ('illegal usage, please use -h to get help')
		sys.exit(2)

	xml_name=None
	doc_name=None
	prefix=None

	for opt, arg in opts:
		if opt == '-h':
			print ('cov_annotate.py --xml <xml_file> --doc <doc_file>  --preifx [prefix]')
			print ('any issue , please contact yuan.fei@mediatek.com')
			sys.exit()
		elif opt == '-d':
			debug = 1
		elif opt =="--xml":
			xml_name = arg
		elif opt =="--doc":
			doc_name = arg
		elif opt =="--prefix":
			prefix = arg

	run(xml_name, doc_name, prefix)

def UI_mode():
	root = cov_gui(version, run)

if __name__ == '__main__':
	if len(sys.argv) <= 1:
		UI_mode()
	else:
		cmd_mode()

	
	


