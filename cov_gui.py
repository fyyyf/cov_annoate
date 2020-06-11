# -*- coding=utf-8 -*-
# any issue , please contact yuan.fei@mediatek.com

import re
import os
import sys

import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox

import base64
#import win32api
#import win32con
from logo_pic import *


class cov_gui(tk.Tk):
	
	def __init__(self, version,func):
		super().__init__()
		self.func = func
		self.version = version
		self.xml_name = None
		self.doc_name = None
		self.prefix   = None
		self.setup_UI()


	
##===========================================================================================
	def xz(self, lb_tmp , file_type):
		filename = tk.filedialog.askopenfilename(initialdir =os.getcwd())
		filename = os.path.basename(filename)
		print (filename)
		if filename != '':
			lb_tmp.config(text = filename);
			if file_type == 'xml':
				self.xml_name=filename
			elif file_type == 'doc':
				self.doc_name=filename
		else:
			lb_tmp.config(text = "No file selected");
	
	
	
	def get_pic(self, pic_code, pic_name):
	    image = open(pic_name, 'wb')
	    image.write(base64.b64decode(pic_code))
	    image.close()
	
	##======================================================
	
	def setup_UI(self):
		#window = tk.Tk();

		self.title("cov_annotate v%s"%self.version)

		
		## XML
		lb_xml=tk.Label(self,text=' '*50)
		btn_xml=tk.Button(self,text="open xml file",command=lambda:self.xz(lb_xml, 'xml'))
		btn_xml.grid(row=0, column=0)
		lb_xml.grid(row=0, column=1)
		
		##DOC
		lb_doc=tk.Label(self,text=' '*50)
		btn_doc=tk.Button(self,text="open doc file",command=lambda:self.xz(lb_doc, 'doc'))
		btn_doc.grid(row=1, column=0)
		lb_doc.grid(row=1, column=1)
		
		##PREFIX
		search_text = tk.StringVar()
		lb_prefix=tk.Label(self,text='Prefix (optional)')
		en_prefix=tk.Entry(self,textvariable=search_text)
		lb_prefix.grid(row=2, column=0)
		en_prefix.grid(row=2, column=1)
		
		
		#产生临时图片，保存在当前目录下
		if not os.path.exists('logo.gif') :
			self.get_pic(logo_gif, 'logo.gif')

		#隐藏图片
		#win32api.SetFileAttributes('logo.gif', win32con.FILE_ATTRIBUTE_HIDDEN)
		
		logo_path = 'logo.gif'
		#logo_path = '\\\\mbjnas02\Public\CD3\DV3\Personal_schedule\Yuan\logo.gif'

		photo = tk.PhotoImage(file=logo_path)
		tk.Label(self, image=photo).grid(row=0, column=2, rowspan=3, padx=5, pady=5) #rowspan=2 跨两行
		
		
		btn_run=tk.Button(self,text="annotate coverage",command=lambda:self.func(self.xml_name, self.doc_name, en_prefix.get()))
		btn_run.grid(row=3,columnspan=3, pady=5)
		#btn_run.pack()
		#
		self.mainloop()
		
		


