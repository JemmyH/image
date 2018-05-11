# -*- coding: utf-8 -*-
import scrapy
from image.items import ImageItem

class GetImageSpider(scrapy.Spider):
    name = 'get_image'
    allowed_domains = ['http://pic.netbian.com/']
    start_urls = ["http://pic.netbian.com/4kmeinv/"]
    for i in range(2, 167):
        start_urls.append("http://pic.netbian.com/4kmeinv/index_" + str(i) + ".html")

    def parse(self, response):
        item = ImageItem()
        srcs = []
        gotttn_urls = response.xpath("/html/body/div[2]/div[3]/ul/li//img/@src").extract()
        for i in gotttn_urls:
            srcs.append("http://pic.netbian.com" + i)
        item["image_urls"] = srcs
        yield item
