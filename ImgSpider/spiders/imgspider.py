# -*- coding: utf-8 -*-
import scrapy
from ..items import ImgspiderItem

class ImgspiderSpider(scrapy.Spider):
    name = 'imgspider'
    allowed_domains = ['pic.netbian.com']
    start_urls = ['http://pic.netbian.com/']

    def parse(self, response):
        imgUrls = response.xpath('//ul[@class="clearfix"]/li/a//@src').extract()
        for img in imgUrls:
            url = "http://pic.netbian.com" + img
            item = ImgspiderItem()
            item['url']=[url]
            yield item
            nextPage = response.xpath('//div[@class="page"]/a/@href').extract()
            for next in nextPage:
                if(len(next) != 0 ):
                    pageUrl = "http://pic.netbian.com" + next
                    yield scrapy.Request(url=pageUrl, callback=self.parse)

