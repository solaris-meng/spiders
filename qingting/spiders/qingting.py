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
    {'url':'http://www.qingting.fm/s/vcategories/527/1809/0', 's1':'相声', 's2':'段子精选', 's3':''},
    {'url':'http://www.qingting.fm/s/vcategories/527/856/0', 's1':'相声', 's2':'小品荟萃', 's3':''},
    {'url':'http://www.qingting.fm/s/vcategories/527/0/0', 's1':'相声', 's2':'相声评书', 's3':''},
    {'url':'http://www.qingting.fm/s/vcategories/527/1809/0', 's1':'相声', 's2':'综艺荟萃', 's3':''},
    {'url':'http://www.qingting.fm/s/vcategories/521/2079/0', 's1':'小说', 's2':'神推荐', 's3':''},
    {'url':'http://www.qingting.fm/s/vcategories/521/517/0', 's1':'小说', 's2':'悬疑探险', 's3':''},
    {'url':'http://www.qingting.fm/s/vcategories/521/518/0', 's1':'小说', 's2':'古风言情', 's3':''},
    {'url':'http://www.qingting.fm/s/vcategories/521/510/0', 's1':'小说', 's2':'现代都市', 's3':''},
    {'url':'http://www.qingting.fm/s/vcategories/521/511/0', 's1':'小说', 's2':'惊悚诡异', 's3':''},
    {'url':'http://www.qingting.fm/s/vcategories/521/509/0', 's1':'小说', 's2':'现代言情', 's3':''},
    {'url':'http://www.qingting.fm/s/vcategories/521/508/0', 's1':'小说', 's2':'玄幻超能', 's3':''},
    {'url':'http://www.qingting.fm/s/vcategories/521/2127/0', 's1':'小说', 's2':'影视原著', 's3':''},
    {'url':'http://www.qingting.fm/s/vcategories/521/520/0', 's1':'小说', 's2':'官商职场', 's3':''},
    {'url':'http://www.qingting.fm/s/vcategories/521/521/0', 's1':'小说', 's2':'古代武侠', 's3':''},
    {'url':'http://www.qingting.fm/s/vcategories/521/2452/0', 's1':'小说', 's2':'广播剧', 's3':''},
    {'url':'http://www.qingting.fm/s/vcategories/521/2125/0', 's1':'小说', 's2':'实体出版', 's3':''},
    {'url':'http://www.qingting.fm/s/vcategories/521/2135/0', 's1':'小说', 's2':'专题合集', 's3':''},
    {'url':'http://www.qingting.fm/s/vcategories/521/513/0', 's1':'小说', 's2':'文学著作', 's3':''},
    {'url':'http://www.qingting.fm/s/vcategories/521/516/0', 's1':'小说', 's2':'历史军事', 's3':''},
    {'url':'http://www.qingting.fm/s/vcategories/521/2126/809', 's1':'小说', 's2':'黑道总裁', 's3':''},
    {'url':'http://www.qingting.fm/s/vcategories/521/2174/0', 's1':'小说', 's2':'火爆完本', 's3':''},
]
INDEX = -2
DB = 'local'
#DB = 'test_mongo'
DB = 'all'

def send_item_v1(item):
    url='http://101.200.174.136:10086/api/qingtingfm/channels'
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
    print 'name-%s, %d' % (item['name'], rv.status_code)
    return 'success'

class QingtingSpider(scrapy.Spider):
    name = "qingting"
    allowed_domains = ["qingting.fm"]
    start_urls = []

    if INDEX == -1:
        start_urls.append(QT[-1]['url'])
    elif INDEX == -2:
        for i in QT:
            start_urls.append(i['url'])
    else:
        start_urls.append(QT[INDEX]['url'])

    def parse(self, response):
        items = response.xpath("//a/@href").extract()
        for i in items:
            url = 'http://www.qingting.fm/s%s' % i
            #print url
            req = scrapy.Request(url, callback=self.parse_item)
            req.meta['start_url'] = response.url
            yield req
        pass

    def parse_item(self, response):
        p_url = response.url

        start_url = response.meta['start_url']
        for i in QT:
            if i['url'] == start_url:
                p_cate_1 = i['s1']
                p_cate_2 = i['s2']
                p_cate_3 = i['s3']
                break
            else:
                p_cate_1 = 'null'
                p_cate_2 = 'null'
                p_cate_3 = 'null'

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
        if DB == 'test_mongo' or DB == 'all':
            send_item_v1(item)
