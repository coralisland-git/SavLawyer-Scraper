# from __future__ import unicode_literals
import scrapy

import json

import os

import scrapy

from scrapy.spiders import Spider

from scrapy.http import FormRequest

from scrapy.http import Request

from chainxy.items import ChainItem

from scrapy import signals

from scrapy.xlib.pydispatch import dispatcher

from selenium import webdriver

from selenium.common.exceptions import TimeoutException

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By

from lxml import etree

from lxml import html

import pdb

import time

import random

import csv,codecs,cStringIO



class lawyer_sel(scrapy.Spider):

	name = 'lawyer_sel'

	domain = ''

	history = []

	output = []

	source_list = []

	timeout = 5

	def __init__(self):

		script_dir = os.path.dirname(__file__)

		file_path = script_dir + '/proxies.txt'

		with open(file_path, 'rb') as text:

			self.proxy_list =  [ "http://" + x.strip() for x in text.readlines()]

		dispatcher.connect(self.spider_closed, signals.spider_closed)

		self.myfile = "AI - Appenzell Inner-Rhodes"

	def spider_closed(self, spider):

		try:

			with open(self.myfile+'.csv', 'wb') as outfile:

				writer = UnicodeWriter(outfile,quoting=csv.QUOTE_ALL)

				writer.writerow(['name', 'address', 'email', 'phone', 'office'])

				for line in self.output:

					try:
						writer.writerow([line['name'], line['address'], line['email'], line['phone'], line['office']])
					except:
						pdb.set_trace()

		except Exception as e:

			pass

	
	def start_requests(self):

		url = "https://www.sav-fsa.ch/en/anwaltssuche.html?"

		headers = {
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
			"Accept-Encoding": "gzip, deflate, br",
			"Content-Type": "application/x-www-form-urlencoded",
			"Upgrade-Insecure-Requests": "1",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
		}


		formdata = {
			"ort":"", 
			"plz": "",
			"umkreis": "200",
			"kanton_id[]": "AI",
			"sprache_id[]": "",
			"geschlecht": "",
			"sav_code[]": "",
			"sav_fachanwalt_id": "",
			"sav_fachanwalt_id_mediation": "",
			"name": "",
			"vorname": "",
			"suche": "search"
		}

		yield scrapy.FormRequest(url, callback=self.parse, headers=headers, formdata=formdata, method="POST", dont_filter=True)


	def parse(self, response):

		chrome_options = webdriver.ChromeOptions()

		# chrome_options.add_argument("headless")

		while True:

			chrome_options.add_argument('--proxy-server=%s' % random.choice(self.proxy_list))

			self.driver = webdriver.Chrome('./chromedriver.exe', chrome_options=chrome_options)

			self.driver.get('https://www.sav-fsa.ch/en/anwaltssuche.html?')

			source = self.driver.page_source.encode("utf8")

			if 'Access to find a lawyer is not permitted from your country' not in source:

				break

			else:

				self.driver.close()


		self.driver.find_element_by_id('umkreis').send_keys('200 km')

		self.driver.find_element_by_id('kanton_id[]').send_keys(self.myfile)

		bt_element_present = EC.presence_of_element_located((By.ID, 'suche'))
			
		WebDriverWait(self.driver, self.timeout).until(bt_element_present)

		try:

			self.driver.find_element_by_xpath('//input[@id="suche"]').click()

		except:

			pdb.set_trace()	

		while True:

			a_element_present = EC.presence_of_element_located((By.ID, 'anwaltssuche'))
			
			WebDriverWait(self.driver, self.timeout).until(a_element_present)

			profile_list = self.driver.find_elements_by_class_name('anwaltssuche_detail')

			for profile in profile_list:

				profile.click()

				time.sleep(4)

				source = self.driver.page_source.encode("utf8")

				tree = etree.HTML(source)

				item = ChainItem()

				data_list = self.eliminate_space(tree.xpath('//div[@class="kanzlei"]//text()'))

				data = ' '.join(data_list)

				try:

					item['name'] = self.validate(tree.xpath('//h2/text()')[1])

					item['address'] = ' '.join(self.validate(data.split('Address:')[1].split(':')[0]).split(' ')[:-2])

					item['email'] = ''

					item['phone'] = ''

					for idx, val in enumerate(data_list):

						try:

							if 'telephone' in val.lower():

								item['phone'] = data_list[idx+1]

							if 'mail' in val.lower():

								item['email'] = data_list[idx+1].replace('[at]', '@').replace('[dot]', '.')

						except:

							pass

					item['office'] = self.validate(tree.xpath('//h3/span/text()')[0])


					self.output.append(item)

				except Exception as e:

					print('~~~~~~~~~~~~~~~~~~~~', e)

					pass

			try:

				next_bt = self.driver.find_element_by_xpath('//a[@class="button naechste"]')

				if next_bt:

					next_bt.click()

				else:

					break

			except:

				break



	def validate(self, item):

		try:

			return item.replace('\n', '').replace('\t','').replace('\r', '').strip()

		except:

			pass


	def eliminate_space(self, items):

		tmp = []

		for item in items:

			if self.validate(item) != '':

				tmp.append(self.validate(item))

		return tmp


class UnicodeWriter


	def __init__(self, f, dialect=csv.excel, encoding="utf-8-sig", **kwds):

		self.queue = cStringIO.StringIO()

		self.writer = csv.writer(self.queue, dialect=dialect, **kwds)

		self.stream = f

		self.encoder = codecs.getincrementalencoder(encoding)()


	def writerow(self, row):
		
		self.writer.writerow([s.encode("utf-8") for s in row])

		data = self.queue.getvalue()

		data = data.decode("utf-8")

		data = self.encoder.encode(data)

		self.stream.write(data)

		self.queue.truncate(0)


	def writerows(self, rows):

		for row in rows:

			self.writerow(row)