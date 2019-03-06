import scrapy
import re
from scrapy.selector import Selector
from monitor.items import MonitorItem
import logging

class Spider(scrapy.Spider):
    name = "monitor"
    allowed_domains = []
    start_urls = []
    urls = []
    url_patterns= {}
    with open("./list") as file:
        line = file.readline()
        while(line):
            url_patterns[line.split()[0]] = line.split()[1]
            urls.append(line.split()[0])
            line = file.readline()

    def start_requests(self):
        for i in range(len(Spider.urls)):
            yield scrapy.Request(Spider.urls[i], callback=self.parse)

    def parse(self, response):
        if response.status == 200:
            url = response.url
            host = url.split("cn")[0]+ "cn"
            response = Selector(response)
            news_lst = response.xpath(Spider.url_patterns[url])
            for news in news_lst:
                item = MonitorItem()
                item['news_tiltle'] = news.xpath("a/@title").extract()
                item['news_url'] = host + (news.xpath("a/@href").extract()[0].split("..")[1])
                print(item)
                yield item

