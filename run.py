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

@app.route('/get_data', methods = ['GET'])
def get_data():
	# form_data = request.form
	sql = 'SELECT consno,DATE_FORMAT(datadate,"%Y-%m-%d") as datadate,consnamefull,consarea,pape FROM bus_ydcj_power_consumption WHERE consno = "0182653487"'
	power_data = dbhelper.db_select(sql)
	data_list = []
	# return_data = {'data': data_list}
	return_data = {}
	return_data['data'] = data_list
	return_data['draw'] = 1
	return_data['start'] = 1
	return_data['length'] = 10
	return_data['recordsTotal'] = 67
	return_data['recordsFiltered'] = 67
	for row in power_data:
		row_list = []
		row_list.append(row['consno'])
		row_list.append(row['datadate'])
		row_list.append(row['consnamefull'])
		row_list.append(row['consarea'])
		row_list.append(row['pape'])
		data_list.append(row_list)

	return_data = jsonify(return_data)
	return return_data

@app.route('/datatable')
def datatable():
	return render_template('datatable.html')


if __name__ == '__main__':
	app.debug= True
	app.run(host = '0.0.0.0')