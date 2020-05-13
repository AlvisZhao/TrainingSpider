# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class NewsspiderItem(scrapy.Item):
    # define the fields for your item here like:
    #新闻标题
    title = scrapy.Field()
    #新闻发布日期
    date = scrapy.Field()
    #新闻发布时间
    time = scrapy.Field()
    #新闻作者
    author = scrapy.Field()
    #新闻来源
    source = scrapy.Field()
    #新闻内容
    content = scrapy.Field()
    pass
