# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from ..items import MusicspiderItem

class MusicspiderSpider(scrapy.Spider):
    name = 'musicspider'
    # allowed_domains = ['music.taihe.com']
    start_urls = ['http://music.taihe.com/artist/2517']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url,callback=self.parse_first,endpoint="render.html",args={ 'wait':5, 'image':0,'timeout':90})

    def parse_first(self, response):
        pageUrl = response.xpath("//div[@class='songlist-inline songlist-title']/span/a/@href").extract()
        for url in pageUrl:
            if 'mv' in url:
                continue
            else:
                url = "http://music.taihe.com" + url
                yield SplashRequest(url=url,callback=self.parse_s,endpoint="render.html",args={ 'wait':5, 'image':0,'timeout':90})

    def parse_s(self,reponse):
        item = MusicspiderItem()
        musicName = reponse.xpath("//div[@class='song-info-box fl']/h2/span/text()").extract()
        player = reponse.xpath("//div[@class='song-info-box fl']/p/span/span/a/text()").extract()
        lyric = reponse.xpath("//div[@class='lrc-list pr none muui-lrc lrc']/ul/li/text()").extract()
        likesNumber = reponse.xpath("//ul[@class='song-opera pa']/li/a/span[@class='collect-num to']/text()").extract()
        lyric = ["".join(lyric)]
        item['musicName'] = musicName
        item['player'] = player
        item['lyric'] = lyric
        item['likesNumber'] = likesNumber
        yield item
