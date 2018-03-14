#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-03-11 00:42:45
# @Author  : Michael (mishchael@gmail.com)

import dbhelper
import datetime
from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify

app = Flask(__name__)

@app.route('/')
def index():
	return 'Hello,This is index!'

@app.route('/get_data', methods = ['POST'])
def get_data():
	#获取get参数
	draw = int(request.form.get('draw'))
	#请求的起始行（比如：第一页： 0，第二页： 1*pagelength）
	start = int(request.form.get('start'))
	#每页的长度
	length = int(request.form.get('length'))
	#搜索
	search_value = request.form.get('search[value]')

	search_sql = " and "

	sql = 'SELECT consno,DATE_FORMAT(datadate,"%Y-%m-%d") as datadate,consnamefull,consarea,pape FROM bus_ydcj_power_consumption WHERE consno in ("0182653487","0182824005")'
	power_data = dbhelper.db_select(sql)
	
	#分页
	data_list = []
	recordsTotal = len(power_data)
	last_row_num = len(power_data)
	
	for i in range(start, start + length):
		if i < last_row_num:
			row = power_data[i]
			data_list.append(row)

	
	return_data = {}
	return_data['data'] = data_list
	return_data['draw'] = draw
	return_data['recordsTotal'] = recordsTotal
	return_data['recordsFiltered'] = recordsTotal

	return_data = jsonify(return_data)
	return return_data

@app.route('/datatable')
def datatable():
	return render_template('datatable.html')

@app.route('/chart_bar_data', methods = ['GET'])
def chart_bar_data():
	sql = 'SELECT consarea,SUM(pape) as pape,SUM(pape1) as pape1,SUM(pape2) as pape2,SUM(pape3) as pape3,SUM(pape4) as pape4 FROM bus_ydcj_power_consumption GROUP BY consarea'
	chart_data = dbhelper.db_select(sql)
	return_data = {}
	area_list = []
	pape_list = []
	pape1_list = []
	pape2_list = []
	pape3_list = []
	pape4_list = []
	for row in chart_data:
		area_list.append(row['consarea'])
		pape_list.append(round(row['pape'], 2))
		pape1_list.append(round(row['pape1'], 2))
		pape2_list.append(round(row['pape2'], 2))
		pape3_list.append(round(row['pape3'], 2))
		pape4_list.append(round(row['pape4'], 2))

	return_data['area'] = area_list
	return_data['pape'] = pape_list
	return_data['pape1'] = pape1_list
	return_data['pape2'] = pape2_list
	return_data['pape3'] = pape3_list
	return_data['pape4'] = pape4_list

	return_data = jsonify(return_data)
	return return_data

@app.route('/chart_cal_effectscatter_data')
def chart_cal_effectscatter_data():
	return_data = []
	sql = 'SELECT DATE_FORMAT(datadate,"%Y-%m-%d") as datadate,pape FROM bus_ydcj_power_consumption WHERE consno = "0180825628"'
	chart_data = dbhelper.db_select(sql)
	
	for row in chart_data:
		row_list =[]
		row_list.append(row['datadate'])
		row_list.append(row['pape'])
		return_data.append(row_list)

	return_data = jsonify(return_data)
	return return_data
		
@app.route('/chart_tree_data')
def chart_tree_data():
	return_data = {}
	
	sql = 'SELECT DISTINCT consno,consarea,consnamefull FROM bus_ydcj_power_consumption'
	chart_data = dbhelper.db_select(sql)
	area_name_dict = {}
	name_no_dict = {}
	return_data['name'] = '日照市机械铸造企业'
	return_data['children'] = []
	for row in chart_data:
		if row['consarea'] not in area_name_dict.keys():
			area_name_dict[row['consarea']] = []
		area_name_dict[row['consarea']].append(row['consnamefull'])
		if row['consnamefull'] not in name_no_dict.keys():
			name_no_dict[row['consnamefull']] = []
		name_no_dict[row['consnamefull']].append(row['consno'])
	# return_data_children = []
	for area,name in area_name_dict.items():
		child_area = {}
		child_area['name'] = area
		child_area['children'] = []
		for name_key,no in name_no_dict.items():
			if name_key in name:
				child_name = {}
				child_name['name'] = name_key
				child_name['value'] = ''
				for no_item in no:
					child_name['value'] = child_name['value'] + '.' + no_item
				child_name['value'] = child_name['value'][1:]
				child_area['children'].append(child_name)
		return_data['children'].append(child_area)
	

	return_data = jsonify(return_data)
	return return_data



@app.route('/chart')
def chart():
	return render_template('chart.html')








if __name__ == '__main__':
	app.debug= True
	app.run(host = '0.0.0.0')