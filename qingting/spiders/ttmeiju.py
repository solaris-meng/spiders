# -*- coding: utf-8 -*-
import scrapy
import requests
import json

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

fd = open('ttmeiju.txt', 'a+')

INDEX = -2
DB = 'local'
#DB = 'test_mongo'
#DB = 'all'

class QingtingSpider(scrapy.Spider):
    name = "ttmeiju"
    allowed_domains = ["ttmeiju.com"]
    start_urls = ['http://www.ttmeiju.com/summary.html']


    def parse(self, response):
        trs = response.xpath("//tr")
        total = 0
        skip = 0
        for tr in trs:
            skip += 1
            if skip < 5:
                continue

            total += 1
            #if total > 2:
            #    break
            tid = tr.xpath("td/text()").extract()[0]
            turl = tr.xpath("td/a/@href").extract()[0]
            tname = tr.xpath("td/a/text()").extract()[0]
            #print(tid, turl,tname)

            if turl[-4:] != 'html':
                continue
            req = scrapy.Request(turl, callback=self.parse_item)
            req.meta['tid'] = tid
            req.meta['tname'] = tname
            yield req
        pass

    def parse_item(self, response):
        t_url = response.url

        t_id = int(response.meta['tid']) - 1
        t_name = response.meta['tname']

        td = response.xpath('//td/text()').extract()
        t_time = td[1]

        tds = response.xpath('//td')[3]
        if tds.xpath('font/text()').extract():
            t_status = tds.xpath('font/text()').extract()[0]
        else:
            t_status = td[3]

        print(t_time)
        print(t_status)
        print(t_url, t_id, t_name)

        line = '%d'% t_id+'*'+t_name+'*'+t_status+'*'+t_time
        with open('ttmeiju.txt', 'a+') as fd:
            fd.write(line+'\n')
