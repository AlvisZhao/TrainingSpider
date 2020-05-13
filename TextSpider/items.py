# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TextspiderItem(scrapy.Item):
    # define the fields for your item here like:
    bookName = scrapy.Field()
    chapterName = scrapy.Field()
    chapterContent = scrapy.Field()
    pass
