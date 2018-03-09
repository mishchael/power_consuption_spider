#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-06 18:20:31
# @Author  : 张世超


import os
import json

#构建需要查询的用户的字典，格式为 {'日照龙山机床配件制造厂': {'area': '东港区', 'consNo': ['0182653487', '0182824005']}, '日照市龙泉铸造有限公司': {'area': '东港区', 'consNo': ['0180829529', '0180831991']}}
fr = open('用户.csv', 'r', encoding = 'gbk')
cons_dict = {}
cons = fr.readlines()
# print(cons)
for item in cons:
	cons_list = item.split(',')

	for x in range(0, len(cons_list)):
		cons_list[x] = cons_list[x].strip('\n')
	
	cons_dict[cons_list[0]] = {
		'area' : cons_list[1],
		'consNo' : cons_list[2:]
	}

#保存为json格式
fw = open('cons.json', 'w', encoding = 'utf-8')
fw.write(json.dumps(cons_dict))
fw.close()
fr = open('cons.json')
cons_dict2 = json.loads(fr.read())
print(cons_dict2)