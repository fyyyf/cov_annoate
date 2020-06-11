# -*- coding=utf-8 -*-
# any issue , please contact yuan.fei@mediatek.com

import re
import os
import sys


from collections import defaultdict

import xml.dom.minidom as XmlDocument


class cov_xml_proc:
	#doc = None
	def __init__(self, xml_name, debug):
		self.doc = XmlDocument.parse(xml_name)
		self.debug = debug

	def get_cp_cr_dict(self, xCtypes):
		cov_item_dict = defaultdict(dict)
		for cp in xCtypes:
			cov_dict_tmp = defaultdict(int)
			xCbins_cp = cp.getElementsByTagName('bin')
			name = xCbins_cp[0].getElementsByTagName('name')
			metric = xCbins_cp[0].getElementsByTagName('metric')
			tbins = cp.getElementsByTagName('totalbins')
			cbins = cp.getElementsByTagName('coveredbins')
			mbins = cp.getElementsByTagName('missingbins')
			
			name_str = name[0].firstChild.data
			if name_str in cov_item_dict:
				continue
	
			hit_str  = metric[0].firstChild.data
			tbins_str= tbins[0].firstChild.data
			cbins_str= cbins[0].firstChild.data
			mbins_str= mbins[0].firstChild.data
	
			type_op_cp = cp.getElementsByTagName('type_option')
			op_cp = cp.getElementsByTagName('option')
			if len(type_op_cp)>0 :
				weight = type_op_cp[0].getElementsByTagName('weight')
			else:
				weight = op_cp[0].getElementsByTagName('weight')
			weight_str = weight[0].firstChild.data
	
			if self.debug ==1:
				print("name=%s hit=%s%% tot=%s covered=%s miss=%s" % (name_str, hit_str, tbins_str, cbins_str, mbins_str ))
			cov_dict_tmp['name'] = name_str
			cov_dict_tmp['coverage']  = hit_str  ##+'%'
			cov_dict_tmp['total'] = tbins_str
			cov_dict_tmp['covered'] = cbins_str
			cov_dict_tmp['missing'] = mbins_str
			cov_dict_tmp['weight'] = weight_str
			cov_item_dict['%s'%name_str] = cov_dict_tmp
		return cov_item_dict
		
	
	def parser_xml(self):
		cov_dict = defaultdict(dict)
	
		#doc = XmlDocument.parse(file_name)
		xCtypes = self.doc.getElementsByTagName('covertype')
	
		for ctype in xCtypes :
			cov_cg_dict = defaultdict(dict)
		
			xPaths = ctype.getElementsByTagName('path')
			xCbins = ctype.getElementsByTagName('bin')
			xName = xCbins[0].getElementsByTagName('name')
			path_name = xName[0].firstChild.data
			if self.debug :
				print("cg_name : ", path_name)
			cov_dict['%s' %path_name] = cov_cg_dict
	
			cov_type_dict = defaultdict(dict)
			cov_insts_dict = defaultdict(dict)
				
			## type
			xCPs = ctype.getElementsByTagName('coverpoint')
			cov_tcp_dict = self.get_cp_cr_dict(xCPs)
	
			xCRs = ctype.getElementsByTagName('cross')
			cov_tcr_dict = self.get_cp_cr_dict(xCRs)
	
			cov_type_dict = cov_tcp_dict.copy()
			cov_type_dict.update(cov_tcr_dict)
			cov_cg_dict['TYPE'] = cov_type_dict
	
			## instance
			xInsts = ctype.getElementsByTagName('coverinstance')
			if len(xInsts) > 0:
				for inst in xInsts:
					cov_per_inst_dict = defaultdict(dict)
					xops = inst.getElementsByTagName('option')
					iName = xops[0].getElementsByTagName('name')
					inst_name = iName[0].firstChild.data
					if self.debug :
						print("inst_name : ", inst_name)
					xICPs = inst.getElementsByTagName('coverpoint')
					cov_icp_dict = self.get_cp_cr_dict(xICPs)
	
					xICRs = inst.getElementsByTagName('cross')
					cov_icr_dict = self.get_cp_cr_dict(xICRs)
	
					cov_per_inst_dict = cov_icp_dict.copy()
					cov_per_inst_dict.update(cov_icr_dict)
					cov_insts_dict[inst_name] = cov_per_inst_dict
				cov_cg_dict['INST'] = cov_insts_dict
	
		return cov_dict
