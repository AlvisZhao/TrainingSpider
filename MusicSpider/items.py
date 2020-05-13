# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MusicspiderItem(scrapy.Item):
    # define the fields for your item here like:
    musicName = scrapy.Field()
    player = scrapy.Field()
    lyric = scrapy.Field()
    likesNumber = scrapy.Field()
    pass
