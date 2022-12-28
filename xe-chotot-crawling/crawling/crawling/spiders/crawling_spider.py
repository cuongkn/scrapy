import time

import scrapy
from scrapy import Request


class CrawlingSpider(scrapy.Spider):
    name = "mycrawler"
    start_urls = [
        'https://xe.chotot.com/mua-ban-xe',
    ]

    def start_requests(self, max_page=4500):
        page = 1
        for url in self.start_urls:
            while page <= max_page:
                tmp = url + '?page=' + str(page)
                yield scrapy.Request(
                    tmp,
                    callback=self.parse)
                page += 1

    def parse(self, response):
        for product in response.xpath("//div[@class='ListAds_ListAds__rEu_9 col-xs-12 no-padding']/ul/div"):
            name = product.xpath(
                ".//li/a[@class='AdItem_adItem__gDDQT']/div[@class='Layout_right__710NU ']/div/h3[@class='commonStyle_adTitle__g520j ']/text()").get()
            info = product.xpath(
                ".//li/a[@class='AdItem_adItem__gDDQT']/div[@class='Layout_right__710NU ']/div/div[@class='AdBody_adUpperBody__4Mt0b']/span/text()").get()
            price = product.xpath(
                ".//li/a[@class='AdItem_adItem__gDDQT']/div[@class='Layout_right__710NU ']/div/div[@class='AdBody_adUpperBody__4Mt0b']/div/p/text()").get()
            yield {
                'name': name,
                'info': info,
                'price': price
            }
        next_page = response.xpath(
            "//button[@class='Paging_redirectPageBtn__KvsqJ']/i[@class='Paging_rightIcon__3p8MS']").get()

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
