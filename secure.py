#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import lxml
import re

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

base = "http://regi.zju.edu.cn/learning.php"
outline = requests.get(base).content
content = BeautifulSoup(outline, 'lxml')
dir_li = content.find_all('li')

with open('secure.txt', 'a') as f:
	for d_li in dir_li:
		href = "http://regi.zju.edu.cn/" + d_li.find('a').get('href')
		url = href
		content = requests.get(url).content
		content = BeautifulSoup(content, 'lxml')
		table = content.find('table')
		all_tr = table.find_all('tr')

		all_page = all_tr[1].find_all('a')[-1].get('href')
		all_page = int(re.search("page=(\d+)", all_page).group(1))

		print d_li.text
		f.write(d_li.text + '\n')

		for page in range(1, all_page+1):
			print page
			url = href + "&&page=" + str(page)
			content = requests.get(url).content.decode('gbk')
			content = BeautifulSoup(content, 'lxml')
			table = content.find('table')
			all_tr = table.find_all('tr')
			all_div =  all_tr[0].find_all('div', attrs={'class':"shiti"})
			print url
			all_span = all_tr[0].find_all('span')
			print len(all_div), len(all_span)
			chinese = u"标准答案：.*([\u4e00-\u9fa5]{2})"
			for i in range(len(all_div)):
				question = all_div[i].find('h3').text.strip()
				answer = all_span[i].text
				match = re.search(chinese, answer)
				if match:
					answer = match.group(1)
				# ABCD
				else:
					answer = re.search("[A-D]", answer).group()
					if answer == "A":
						li = all_div[i].find('ul').find_all('li')[0]
						answer = li.text.strip()
					elif answer == "B":
						li = all_div[i].find('ul').find_all('li')[1]
						answer = li.text.strip()
					elif answer == "C":
						li = all_div[i].find('ul').find_all('li')[2]
						answer = li.text.strip()
					elif answer == "D":
						li = all_div[i].find('ul').find_all('li')[3]
						answer = li.text.strip()
				f.write(question + '\n' + answer + '\n\n')