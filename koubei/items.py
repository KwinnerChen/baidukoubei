# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KoubeiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    memname = scrapy.Field()  # 平台名称
    compname = scrapy.Field()  # 企业名称
    compdesc = scrapy.Field()  # 企业简介
    cptcontent = scrapy.Field()  # 投诉内容
    cacsi = scrapy.Field()  # 满意度
    praise = scrapy.Field()  # 好评率