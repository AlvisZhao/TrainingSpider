# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule
from ..items import TextspiderItem
from scrapy.http import Request

class TextspiderSpider(scrapy.Spider):
    name = 'textspider'
    allowed_domains = ['quanshuwang.com']
    start_urls = [
                    'http://www.quanshuwang.com/list/1_2.html',
                    'http://www.quanshuwang.com/list/1_3.html',
                    'http://www.quanshuwang.com/list/1_4.html',
                    'http://www.quanshuwang.com/list/1_5.html',
                    'http://www.quanshuwang.com/list/1_6.html',
                    'http://www.quanshuwang.com/list/1_7.html',
                    'http://www.quanshuwang.com/list/1_8.html',
                    'http://www.quanshuwang.com/list/1_9.html',
                    'http://www.quanshuwang.com/list/1_10.html'
                ]
    
    def parse(self, response):
        classUrls = response.xpath("//span[@class='l']/a/@href").extract()
        for book in classUrls:
            yield Request(url=book, callback=self.parseRead)

    def parseRead(self,response):
        bookUrls = response.xpath("//a[@class='reader']/@href").extract()[0]
        yield Request(url=bookUrls, callback=self.parseContent)

    def parseChapter(self,reponse):

        chapterUrls = reponse.xpath("//div[@class='clearfix dirconone']/li/a/@href").extract()
        for chapterUrl in chapterUrls:
            yield Request(url=chapterUrls, callback=self.parseContent)

    def parseContent(self,response):
        bookName = response.xpath("//em[@class='l']/text()").get()
        chapterName = response.xpath("//strong/text()").get()
        chapterContent = response.xpath("//div[@class='mainContenr']/text()").extract()
        item = TextspiderItem()
        item['bookName'] = bookName
        item['chapterName'] = chapterName
        item['chapterCobtent'] = chapterContent
        yield item



