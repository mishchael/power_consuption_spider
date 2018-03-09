#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-06 18:20:31
# @Author  : 张世超


import json
from bs4 import BeautifulSoup
from urllib import request
from urllib import parse
from http import cookiejar
import datetime
import re
import json
import pymysql



if __name__ == '__main__':

	#User-Agent信息
	user_agent = r'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)'
	#Headers信息
	headers = {'User-Agnet': user_agent, 'Connection': 'keep-alive'}
	#保存cookie的文件
	filename = 'cookie.txt';
	#创建MozillaCookieJar实例对象
	cookies = cookiejar.MozillaCookieJar()
	#从文件独处cookie内容
	cookies.load('cookie.txt', ignore_discard = True, ignore_expires = True)

	'''
	处理post请求的函数，返回response
	'''
	def deal_post_request(url, form_data, headers, cookies):
		#引用全局变量urllib的模块request
		global request 
		#利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
		handler = request.HTTPCookieProcessor(cookies)
		#通过CookieHandler创建opener
		opener = request.build_opener(handler)
		#用opener的open方法打开网页
		# response = opener.open(url)
		#POST请求需要创建Request对象，然后用open方法请求网页
		rst = request.Request(url = url, data = form_data, headers = headers)
		rsp = opener.open(rst)
		return rsp

	'''
	数据库插入操作
	'''
	def db_insert(sql):
		global pymysql
		# 打开数据库连接
		db = pymysql.connect(host = '127.0.0.1', user = 'root', password = 'nlcyzqzy.0', db = 'rzdb', port = 3306, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
		# 使用 cursor() 方法创建一个游标对象 cursor
		cursor = db.cursor()
		# 使用 execute()  方法执行 SQL 插入语句
		try:
		   # 执行sql语句
		   cursor.execute(sql)
		   # 提交到数据库执行
		   db.commit()
		   # print("**********数据插入成功**********")
		except:
			# 如果发生错误则回滚
			db.rollback()
		finally:
			# 关闭数据库连接
			cursor.close()
			db.close()


	'''
	数据库查询操作
	返回查询结果，list格式
	'''
	def db_select():
		# 打开数据库连接
		db = pymysql.connect(host = '127.0.0.1', user = 'root', password = 'nlcyzqzy.0', db = 'rzdb', port = 3306, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
		 
		# 使用cursor()方法获取操作游标 
		cursor = db.cursor()
		 
		# SQL 查询语句
		sql = "SELECT * FROM bus_ydcj_power_consumption"
		       
		try:
			# 执行SQL语句
			cursor.execute(sql)
			# 获取所有记录列表
			results = cursor.fetchall()
			for row in results:
				print(row[2])

		   # for row in results:
		   #    fname = row[0]
		   #    lname = row[1]
		   #    age = row[2]
		   #    sex = row[3]
		   #    income = row[4]
		   #     # 打印结果
		   #    print ("fname=%s,lname=%s,age=%d,sex=%s,income=%d" % \
		   #           (fname, lname, age, sex, income ))
		except:
			print ("Error: unable to fetch data")
		finally:
			return results
			# 关闭数据库连接
			db.close()


	'''
	查询用户日电量的页面需要根据用户编号consNo查询用户名称consName，且该名称必须是带*和...的脱敏名称
	根据用户编号查询用户名称,返回str
	'''
	def query_consName(consNo):
		#查询用户名称url
		url_query_consName = 'http://10.158.242.100/dwdsm/lov.do'
		orgNo = "37411"  #供电单位
		# consNo = "0182653487"  #用户编号
		consType = "1"  #专变用户

		form_data_consName = {}
		form_data_consName['method'] = 'queryConsInfo'
		form_data_consName['orgNo'] = orgNo
		form_data_consName['consType'] = consType
		form_data_consName['consNo'] = consNo
		form_data_consName['containerName'] = 'formEnergyDataAnalysis_11'
		form_data_consName['backFillSign'] = ''
		form_data_consName['_jbjgqxfw'] = 'undefined'
		form_data_consName['_sbjbjg'] = 'undefined'
		form_data_consName['_dwqxfw'] = 'undefined'
		form_data_consName = parse.urlencode(form_data_consName).encode('utf-8')

		response_consName = deal_post_request(url = url_query_consName, form_data = form_data_consName, headers = headers, cookies = cookies)
		html_consName = response_consName.read().decode('gbk')

		#创建BeautifulSoup对象，解析html
		consName = ''
		try:
			soup = BeautifulSoup(html_consName, 'lxml')
			html_consName = soup.script.string
			pattern = re.compile(r'.init.*?","consname":"(.*?)","consno":"')
			#获取用户名称，带*和...的脱敏名称
			consName = re.search(pattern,html_consName).group(1)
		except Exception as e:
			print(e.value)
		finally:
			return consName
		
		

		# fw = open('result_consName.txt', 'w', encoding = 'utf-8')
		# fw.write(consName)
		# fw.close()



	'''
	查询之前需要先获取tableMark，不提交具体信息可在返回页面获得tableMark
	返回str
	'''
	def query_power_tablemark():
		#查询用户日电量url
		url_query_power = 'http://10.158.242.100/dwdsm/energyAnalysis.do'
		#查询之前需要先获取tableMark，不提交具体信息可在返回页面获得tableMark
		form_data_tableMark = {}
		form_data_tableMark['method'] = 'enterEnergyDataAnalysis'
		form_data_tableMark['_jbjgqxfw'] = 'null'
		form_data_tableMark['_sbjbjg'] = 'null'
		form_data_tableMark['_dwqxfw'] = 'null'

		form_data_tableMark = parse.urlencode(form_data_tableMark).encode('utf-8')
		response_tableMark = deal_post_request(url = url_query_power, form_data = form_data_tableMark, headers = headers, cookies = cookies)
		html_tableMark = response_tableMark.read().decode('gbk')

		tableMark = ''
		try:
			soup = BeautifulSoup(html_tableMark, 'lxml')
			html_tableMark = soup.find(id = 'dwEnergyDataAnalysis_17')
			#获取tableMark值
			tableMark = html_tableMark.get('tablemark')
		except Exception as e:
			print(e.value)
		finally:
			return tableMark
		
		# print(tableMark)
	

	'''
	根据consNo查询该用户的日电量数据
	返回list，格式[{一天的数据},{一天的数据}]
	'''
	def query_power(consNo, tableMark, startDate, endDate):
		#查询用户日电量url
		url_query_power = 'http://10.158.242.100/dwdsm/energyAnalysis.do'
		#查询用户日电量的POST请求FormData
		
		# consName = "*照市东港区西湖镇..."  #用户名称必须是带*和...的脱敏名称
		#后来发现不用提交consName
		# consName = query_consName(consNo)
		consName = ''

		# tableMark = query_power_tablemark()
		orgNo = '37411'
		consType = '1'
		zrxs = "1"  #逐日显示
		# startDate = "2018-03-04"  #开始日期
		# endDate = "2018-03-06"  #结束日期
		#POST请求的FormData
		form_data_power = {}
		form_data_power['method'] = 'queryEnergyDataInfo'
		form_data_power['_xmlString'] = '<?xml version="1.0" encoding="UTF-8"?><p><s orgNo="' + orgNo+ '" consNo="' + consNo +'" consName="' + consName +'" consType="' + consType +'" zrxs="' + zrxs +'" conditionNodeId="" conditionNodeName="" startDate="' + startDate +'" endDate="'+ endDate +'" /></p>'
		form_data_power['tableMark'] = tableMark
		form_data_power['_jbjgqxfw'] = 'null'
		form_data_power['_sbjbjg'] = 'null'
		form_data_power['_dwqxfw'] = 'null'
		#使用urlencode方法转换标准格式
		form_data_power = parse.urlencode(form_data_power).encode('utf-8')

		response_power = deal_post_request(url = url_query_power, form_data = form_data_power, headers = headers, cookies = cookies)
		html_power = response_power.read().decode('gbk')

		power_data_list = []
		try:
			soup = BeautifulSoup(html_power, 'lxml')
			html_power_data = soup.script.string
			pattern = re.compile(r"init\('true','true','(\[.*?\])',")
			#获取日电量数据
			#电量显示异常的数据改为null
			power_data = re.search(pattern,html_power_data).group(1).replace('--', 'null')
			# power_data_json = json.dumps(power_data)

			#list每一条是一天的数据，格式为dict
			power_data_list = json.loads(power_data)

			#如果有分页数据，处理下一页
			html_page = soup.find(name = 'div', class_ = 'tableFooterDiv').find(name = 'table', class_= 'dataWindowPilot').tr.td.b.string
			# pattern_page = re.compile(r'.?*总计(\d+)条记录.*?(\d+)/(\d+)页')
			pattern_page = re.compile(r'.*?([0-9]+).*?([0-9]+)/([0-9]+).*?')
			# pattern_page = re.compile(u'.*?\(\[0-9\]+\).*?\(\[0-9\]+\)\/(\[0-9\]+\).*?')
			record_count = int(re.match(pattern_page,html_page).group(1))
			current_page = int(re.match(pattern_page,html_page).group(2))
			max_page = int(re.match(pattern_page,html_page).group(3))
			print('**********总计%s条记录，正在爬取第%s页，共%s页**********'%(record_count,current_page,max_page))
			if current_page < max_page:
				for x in range(current_page+1, max_page +1):
					print('**********总计%s条记录，正在爬取第%s页，共%s页**********'%(record_count,x,max_page))
					next_data_list = query_power_next_page(tableMark, x, max_page)
					for data_item in next_data_list:
						power_data_list.append(data_item)
		except Exception as e:
			print(e.value)
		finally:
			print(power_data_list)
			return power_data_list

	'''
	日电量数据分页显示时，查询下一页数据
	返回list，格式[{一天的数据},{一天的数据}]
	'''
	def query_power_next_page(tableMark, nextPage, maxPage):
		url = 'http://10.158.242.100/dwdsm/pilot.do'
		form_data = {}
		form_data['method'] = 'view'
		form_data['nextPage'] = nextPage
		form_data['tableMark'] = tableMark
		form_data['maxPage'] = maxPage
		form_data['_jbjgqxfw'] = 'null'
		form_data['_sbjbjg'] = 'null'
		form_data['_dwqxfw'] = 'null'

		form_data = parse.urlencode(form_data).encode('utf-8')

		response_next = deal_post_request(url = url, form_data = form_data, headers = headers, cookies = cookies)
		html_next = response_next.read().decode('gbk')

		next_data_list = []
		try:
			soup = BeautifulSoup(html_next, 'lxml')
			html_next = soup.script.string
			pattern = re.compile(r"init\('true','true','(\[.*?\])',")
			#获取日电量数据
			#电量显示异常的数据改为null
			next_data = re.search(pattern,html_next).group(1).replace('--', 'null')
			# power_data_json = json.dumps(power_data)

			#list每一条是一天的数据，格式为dict
			next_data_list = json.loads(next_data)
		except Exception as e:
			print(e.value)
		finally:
			return next_data_list
		


	
	power_dict = {
		'papr2' : '峰止度',
		'datadate' : '日期',
		'papr1' : '尖止度',
		'pape4' : '谷电量',
		'consname' : '用户名称',
		'rapr' : '反止度',
		'pape3' : '平电量',
		'pape2' : '峰电量',
		'pape' : '总电量',
		'pape1' : '尖电量',
		# 'startdate' : '开始日期',
		'papr4q' : '谷起度',
		'papr3q' : '平起度',
		'orgname' : '供电单位',
		'paprq' : '总起度',
		'papr' : '总止度',
		'raprq' : '反起度',
		'papr1q' : '尖起度',
		'papr3' : '平止度',
		'consno' : '用户编号',
		'papr2q' : '峰起度',
		'papr4' : '谷止度',
		# 'enddate' : '结束日期',
		'rape' : '反电量'
	}


	#构造数据插入的sql,list格式
	def get_sql_insert(data_list, consNameFull, consArea, consNo, startDate, endDate):
		sql_insert_list = []

		date_delta = (endDate-startDate).days
		#判断查询日期范围内是否每天都有返回数据
		for x in range(0, date_delta+1):
			datadate = str(startDate)
			# print('查询日期%s'%datadate)
			sql_insert = ''
			is_exist = False
			for item in data_list:
				#如果该日期在返回结果中，则构造插入语句
				# print('结果日期%s'%item['datadate'])
				if datadate == item['datadate'].strip():
					sql_insert = 'insert into bus_ydcj_power_consumption(consnamefull,consarea,'
					sql_insert2 = ' select "' + consNameFull +'","' + consArea + '",'
					for key in power_dict.keys():
						datadate = item['datadate']
						sql_insert = sql_insert + key + ','
						if key == 'consname' or key == 'orgname' or key == 'consno' or key == 'datadate':
							sql_insert2 = sql_insert2 + '"' + item[key] + '"' + ','
						else:
							sql_insert2 = sql_insert2 + item[key] + ','
					sql_insert = sql_insert[0:-1] + ')'
					sql_insert2 = sql_insert2[0:-1] + ' from dual where not exists(select id,consno from bus_ydcj_power_consumption where consno="'+ consNo +'" and datadate="'+ datadate +'")'
					sql_insert = sql_insert + sql_insert2
					# print(sql_insert)
					is_exist = True
			#如果该日期不在返回结果中，则构造插入null数据的插入语句
			if not is_exist:
				sql_insert = 'insert into bus_ydcj_power_consumption(consnamefull,consarea,consno,datadate) select "'+ consNameFull +'","'+ consArea +'","'+ consNo+'","'+ datadate +'" from dual where not exists(select id,consno from bus_ydcj_power_consumption where consno="'+ consNo +'" and datadate="'+ datadate +'")'
				# sql_insert_list.append(sql_insert)
				# print(sql_insert)
			is_exist = False
			startDate = startDate + datetime.timedelta(days= 1)
			print(sql_insert)
			sql_insert_list.append(sql_insert)
		return sql_insert_list



	#读取需要查询的用户,dict格式：格式为{'日照龙山机床配件制造厂': {'area': '东港区', 'consNo': ['0182653487', '0182824005']}, '日照市龙泉铸造有限公司': {'area': '东港区', 'consNo': ['0180829529', '0180831991']}}
	fr = open('cons.json')
	cons_dict = json.loads(fr.read())

	#定义爬取的时间范围
	startDate = datetime.date(2018,1,1)
	# endDate = datetime.date(2018,3,3)
	endDate = datetime.date.today() + datetime.timedelta(days = -1)


	for key,value in cons_dict.items():
		consNameFull = key
		consArea = value['area']
		#consNo类型为list
		consNo_list = value['consNo']

		for consNo in consNo_list:
			#按照consNo查询用户日电量
			tableMark = query_power_tablemark()
			print('**********正在爬取用户%s的用电量**********'%consNo)
			power_data_list = query_power(consNo = consNo, tableMark = tableMark, startDate = str(startDate), endDate = str(endDate))
			if len(power_data_list) == 0:
				print('**********用户%s爬取失败！！！**********'%consNo)
				fw = open('failed2.txt', 'a', encoding = 'utf-8')
				fw.write(consNo+'\n')
				fw.close()
			sql_insert_list = get_sql_insert(power_data_list, consNameFull, consArea, consNo, startDate, endDate)
			print('**********存储用户%s的数据**********'%consNo)
			for sql_insert in sql_insert_list:
				db_insert(sql_insert)
			print("**********数据插入成功**********")
	print('**********用户电量全部爬取完成！！！**********')





	


		# db_insert(sql_insert)
		
			
	# print(power_data_dict)
	# print(type(power_data_dict))
	# date = power_data_dict['datadate']
	# print(date)


	# fw = open('result_power.txt', 'a', encoding = 'utf-8')
	# for item in power_data_list:
	# 	fw.write('******************************************\n')
	# 	for k,v in item.items():
	# 		fw.write(k +' : '+v+'\n')
	# fw.close()



	
