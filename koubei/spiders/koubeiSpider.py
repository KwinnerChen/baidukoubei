#! usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Kwinner Chen
# python v3.6.4
# scrapy v1.5.1


import scrapy
import json
from koubei.items import KoubeiItem


class KoubetSpider(scrapy.Spider):

    name = 'koubeispider'
    allowed_domain = ['koubei.baidu.com']

    # url返回的json数据显示totalpage=6，暂不做通用处理
    def start_requests(self):
        start_urls = [
            'https://koubei.baidu.com/search/getsearchresultajax?wd=%%E8%%A3%%85%%E4%%BF%%AE&page=%s' % num for num in range(1,7)
        ]
        header = {
            'Host': 'koubei.baidu.com',
            'Referer': 'https://koubei.baidu.com/search?query=%E8%A3%85%E4%BF%AE&fr=search',
        }
        for url in start_urls:
            yield scrapy.Request(url=url, headers=header)

    def parse(self, response):
        item = KoubeiItem()
        respdic = json.loads(response.body, encoding='utf-8')
        mems = respdic['data']['mems']
        for mem in mems:
            if mem['truthcount']:
                item['praise'] = mem['praise']
                item['memname'] = mem['memname']
                item['compname'] = mem['compname']
                try:
                    item['compdesc'] = mem['compdesc']
                except:
                    item['compdesc'] = '--'
                request = scrapy.Request(
                    url = 'https://koubei.baidu.com/s/%s?tab=truth' % mem['memcode'],
                    callback = self.appraise
                )
                request.meta['item'] = item
                yield request

    def appraise(self, response):
        item = response.meta['item']
        l = list(map(lambda x: x.strip(), response.xpath('//ul[@class="kb-truth-list"]/li//text()').extract()))
        l = list(map(lambda x: x.strip('\n'), l))
        item['cptcontent'] = list(filter(lambda x: x, l))
        cacsi_list = response.xpath('//ul[@class="kb-truth-list"]/li//span[@class="ret-rate"]/i/@class').extract()
        item['cacsi'] = list(map(lambda x: int(x.split('-')[-1]), cacsi_list))
        yield item
        