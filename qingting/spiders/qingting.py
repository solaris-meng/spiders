# -*- coding: utf-8 -*-
import scrapy
import requests
import json

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

fd = open('qingting_xiangsheng.txt', 'a+')

QT = [
    {'url':'http://www.qingting.fm/s/vcategories/527/0/0', 's1':'相声', 's2':'最热门', 's3':''},
    {'url':'http://www.qingting.fm/s/vcategories/527/1522/855', 's1':'相声', 's2':'郭德纲', 's3':''},
    {'url':'http://www.qingting.fm/s/vcategories/527/1522/0', 's1':'相声', 's2':'德云社', 's3':''},
    {'url':'http://www.qingting.fm/s/vcategories/527/2350/0', 's1':'相声', 's2':'单口相声', 's3':''},
    {'url':'http://www.qingting.fm/s/vcategories/527/2349/0', 's1':'相声', 's2':'大师经典', 's3':''},
    {'url':'http://www.qingting.fm/s/vcategories/527/2353/0', 's1':'相声', 's2':'名家相声', 's3':''},
    {'url':'http://www.qingting.fm/s/vcategories/527/2352/0', 's1':'相声', 's2':'最佳拍档', 's3':''},
]
INDEX = -1
#DB = 'local'
#DB = 'test_mongo'
DB = 'all'

def send_item_v1(item):
    url='http://192.168.10.76:10086/api/qingtingfm/channels'
    data = {
        'id': item['id'],
        'name': item['name'],
        'desc': item['des'],
        'img_url': item['img_url'],
        'clist': item['clist'],
        'ourl': item['ourl'],
        's1': item['s1'],
        's2': item['s2'],
        's3': item['s3']
    }
    rv = requests.post(url, data)
    print 'url-%s, %d' % (url, rv.status_code)
    return 'success'

class QingtingSpider(scrapy.Spider):
    name = "qingting"
    allowed_domains = ["qingting.fm"]
    start_urls = []

    if INDEX == -1:
        start_urls.append(QT[-1]['url'])
    else:
        start_urls.append(QT[INDEX]['url'])

    def parse(self, response):
        items = response.xpath("//a/@href").extract()
        for i in items:
            url = 'http://www.qingting.fm/s%s' % i
            print url
            req = scrapy.Request(url, callback=self.parse_item)
            yield req
        pass

    def parse_item(self, response):
        p_url = response.url

        p_cate_1 = QT[INDEX]['s1']
        p_cate_2 = QT[INDEX]['s2']
        p_cate_3 = QT[INDEX]['s3']

        p_name = response.xpath('//div[@class="channel-name"]/text()').extract()[0]
        p_des = response.xpath('//div[@class="abstract clearfix"]/div[@class="content"]/text()').extract()[0]

        p_list = response.xpath('//div[@class="left-text"]/span/text()').extract()
        p_img = response.xpath('//img/@src').extract()[0]

        item = {}
        item['id'] = p_url.split('/')[-1]
        item['name'] = p_name
        item['des'] = p_des
        item['img_url'] = p_img
        item['ourl'] = p_url
        item['s1'] = p_cate_1
        item['s2'] = p_cate_2
        item['s3'] = p_cate_3


        item['clist'] = ''
        for i in p_list:
            item['clist'] += '%s###' % i
        item['clist'] = item['clist'][:-3]

        if DB == 'local' or DB == 'all':
            item_json = json.dumps(item,ensure_ascii=False)
            fd.write(item_json)
            fd.write('\n')
        elif DB == 'test_mongo' or DB == 'all':
            send_item_v1(item)
        else:
            pass
