# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from ..items import NewsspiderItem

class NewsspiderSpider(scrapy.Spider):
    name = 'newsspider'
    start_urls = [
        'http://news.baidu.com'
        # 'http://baijiahao.baidu.com/s?id=1648617149670356080',
        # 'http://baijiahao.baidu.com/s?id=1648619076815209601'
    ]

    def start_requests(self):
        for start in self.start_urls:
            yield SplashRequest(url=start,callback=self.parse, endpoint='render.html',args={'wait': 5, 'image':0,'timeout':90})

    def parse(self, response):
        pageUrls = response.xpath("//div[@class='menu-list']/ul/li/a/@href").extract()
        pageUrls = list(set(pageUrls))
        for url in pageUrls:
            url = "https://news.baidu.com" + url
            yield SplashRequest(url=url,callback=self.parse_s, endpoint='render.html',args={'wait': 5, 'image':0,'timeout':90})

    def parse_s(self, response):
        string = str(response)
        print("详情链接======>" + string)
        if "internet" in string:
            contentUrl = response.xpath("//div[@class='item has-picture ']/h3/a/@href").extract()
        elif "house" in string or "game" in string:
            contentUrl = response.xpath("//div[@class='tlc']/ul/li/a/@href").extract()
        elif "auto" in string:
            contentUrl = response.xpath("//div[@class='bd']/ul/li/a/@href").extract()
        elif  "tech" in string or "finance" in string:
            contentUrl = response.xpath("//div[@class='middle-focus-news']/ul/li/a/@href").extract()
        elif "mil" in string or "guonei" in string or "guoji" in string or "ent" in string or "sports" in string or "lady" in string:
            contentUrl = response.xpath("//div[@class='b-left']/ul/li/a/@href").extract()
        for url in contentUrl:
            print("详情页面==>" + url)
            yield SplashRequest(url=url,callback=self.parse_last, endpoint='render.html',args={'wait': 5, 'image':0,'timeout':90})

    def parse_last(self, response):
        print("进入最后一个解析器中.......")
        item = NewsspiderItem()
        print("开始爬取...")
        title = response.xpath("//div[@class='article-title']/h2/text()").extract()
        date = response.xpath("//*[@id='detail-page']/div[3]/div/div[2]/div[2]/div/span[1]/text()").extract()
        time = response.xpath("//*[@id='detail-page']/div[3]/div/div[2]/div[2]/div/span[2]/text()").extract()
        author = response.xpath("//*[@id='detail-page']/div[3]/div/div[2]/div[2]/div/span[3]/text()").extract()
        source = response.xpath("//div[@class='author-txt']/p/text()").extract()
        content = response.xpath("//div[@class='article-content']/p/span/text()").extract()
        content = ["".join(content)]
        item['title'] = title
        item['date'] = date
        item['time'] = time
        item['author'] = author
        item['source'] = source
        item['content'] = content
        yield item

