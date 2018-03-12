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


if __name__ == '__main__':
	app.debug= True
	app.run(host = '0.0.0.0')