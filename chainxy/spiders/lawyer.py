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

from lxml import etree

from lxml import html

import pdb

import random



class lawyer(scrapy.Spider):

	name = 'lawyer'

	domain = ''

	history = []

	output = []

	user_agent_list = [
	   #Chrome
	    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
	    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
	    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
	    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
	    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
	    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
	    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
	    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
	    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
	    #Firefox
	    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
	    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
	    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
	    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
	    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
	    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
	    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
	    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
	    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
	    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
	    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
	    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
	    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
	]

	def __init__(self):

		script_dir = os.path.dirname(__file__)

		file_path = script_dir + '/proxies.txt'

		with open(file_path, 'rb') as text:

			self.proxy_list =  [ "http://" + x.strip() for x in text.readlines()]

	
	def start_requests(self):

		url = "https://www.sav-fsa.ch/en/anwaltssuche.html?"

		headers = {
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
			"Accept-Encoding": "gzip, deflate, br",
			"Content-Type": "application/x-www-form-urlencoded",
			"Upgrade-Insecure-Requests": "1",
			"User-Agent": random.choice(self.user_agent_list)
		}

		formdata = {
			"ort": "",
			"plz": "",
			"umkreis": "200",
			"kanton_id[0]": "AR",
			"sprache_id[0]": "",
			"geschlecht": "",
			"sav_code[0]": "",
			"sav_fachanwalt_id": "",
			"sav_fachanwalt_id_mediation": "",
			"name": "",
			"vorname": "",
			"suche": "search",
		}

		yield scrapy.FormRequest(url, callback=self.parse, headers=headers, formdata=formdata, method="POST", meta={'proxy' : random.choice(self.proxy_list)}, dont_filter=True)


	def parse(self, response):

		if 'Access to find a lawyer is not permitted from your country.' in response.body:

			url = "https://www.sav-fsa.ch/en/anwaltssuche.html?"

			headers = {
				"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
				"Accept-Encoding": "gzip, deflate, br",
				"Content-Type": "application/x-www-form-urlencoded",
				"Upgrade-Insecure-Requests": "1",
				"User-Agent": random.choice(self.user_agent_list)
			}

			formdata = {
				"ort": "",
				"plz": "",
				"umkreis": "200",
				"kanton_id[0]": "AR",
				"sprache_id[0]": "",
				"geschlecht": "",
				"sav_code[0]": "",
				"sav_fachanwalt_id": "",
				"sav_fachanwalt_id_mediation": "",
				"name": "",
				"vorname": "",
				"suche": "search",
			}

			yield scrapy.FormRequest(url, callback=self.parse, headers=headers, formdata=formdata, method="POST", meta={'proxy' : random.choice(self.proxy_list)}, dont_filter=True)

		else:

			profile_list = response.xpath('//table[@class="suchresultat"]//tr/@id').extract()

			for profile in profile_list:

				url = "https://www.sav-fsa.ch/modules/Anwaltssuche/templates/detail.ajax.php"

				formdata = {
					"sav_person_id": profile
				}

				headers = {
					"Accept": "*/*",
					"Accept-Encoding": "gzip, deflate, br",
					"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
					"User-Agent": random.choice(self.user_agent_list),
				}
			
				yield scrapy.FormRequest(url, callback=self.parse_detail, headers=headers, formdata=formdata, method="POST", meta={'proxy' : random.choice(self.proxy_list), 'profile' : profile }, dont_filter=True)


	def parse_detail(self, response):

		if 'Access to find a lawyer is not permitted from your country.' in response.body or 'we protect personal data with reCAPTCHA' in response.body:

			url = "https://www.sav-fsa.ch/modules/Anwaltssuche/templates/detail.ajax.php"

			formdata = {
				"sav_person_id": response.meta['profile']
			}

			headers = {
				"Accept": "*/*",
				"Accept-Encoding": "gzip, deflate, br",
				"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
				"User-Agent": random.choice(self.user_agent_list),
			}
		
			yield scrapy.FormRequest(url, callback=self.parse_detail, headers=headers, formdata=formdata, method="POST", meta={'proxy' : random.choice(self.proxy_list), 'profile' : response.meta['profile']}, dont_filter=True)

		else:


			item = ChainItem()

			tree = etree.HTML(response.body)

			data = self.eliminate_space(tree.xpath('//div[@class="kanzlei"]//text()'))

			item['name'] = self.validate(''.join(tree.xpath('//h2/text()')))

			for idx, val in enumerate(data):

				if 'address' in val.lower():

					item['address'] = data[idx+1] + ' ' + data[idx+2]

					if ':' not in data[idx+3]:

						item['address'] += ' ' + data[idx+3]

				if 'telephone' in val.lower():

					item['phone'] = data[idx+1]

				if 'mail' in val.lower():

					item['email'] = data[idx+1].replace('[at]', '@').replace('[dot]', '.')

				if 'office' in val.lower():

					item['office'] = data[idx+1]

			yield item


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