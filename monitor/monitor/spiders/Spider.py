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
            url = line.split()[0]
            first_pattern = line.split()[1]
            second_pattern = line.split()[2]
            print(second_pattern)
            if url not in url_patterns:
                url_patterns[url] = []

            url_patterns[url].append(first_pattern)
            url_patterns[url].append(second_pattern)
            urls.append(url)
            line = file.readline()

    def start_requests(self):
        for i in range(len(Spider.urls)):
            yield scrapy.Request(Spider.urls[i], callback=self.parse)

    def parse(self, response):
        if response.status == 200:
            url = response.url
            host = url.split("cn")[0]+ "cn"
            response = Selector(response)
            news_lst = response.xpath(Spider.url_patterns[url][0])
            for news in news_lst:
                item = MonitorItem()
                if (host == "http://www.ict.ac.cn" or host == "http://www.is.cas.cn"):
                    item["news_tiltle"] = news.xpath(Spider.url_patterns[url][1] + "/text()").extract()
                else:
                    item['news_tiltle'] = news.xpath(Spider.url_patterns[url][1] + "/@title").extract()
    
                target_url = news.xpath(Spider.url_patterns[url][1] + "/@href").extract()[0]
                if (re.match("\.{2}", target_url)):
                    item['news_url'] = host + (target_url.split("..")[1])
                else:
                    item['news_url'] = url + target_url

                print(item)
                yield item

