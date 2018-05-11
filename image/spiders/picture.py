# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from image.items import ImageItem

class PictureSpider(scrapy.Spider):
    name = 'picture'
    # allowed_domains = ['http://www.5857.com/']
    start_urls = ["http://www.5857.com/meixiong/", "http://www.5857.com/qiaotun/", "http://www.5857.com/siwa/", "http://www.5857.com/neiyi/", "http://www.5857.com/zhifu/", "http://www.5857.com/qingchun/", "http://www.5857.com/rihan/", "http://www.5857.com/om/"]

    def parse(self, response):
        # 获取每一个item的url交给request，并将返回的结果交给parse_detail1
        item_urls = response.xpath("/html/body/div[4]/div[2]/ul//li/div[1]/a/@href").extract()
        for item_url in item_urls:
            yield Request(url=item_url, callback=self.parse_datail1)
        # 获取相同大目录下的下一页
        next_url = "http://www.5857.com" + response.xpath("/html/body/div[4]/div[2]/div[2]//a/@href").extract()[-1]
        if next_url:
            yield Request(url=next_url, callback=self.parse)

    def parse_datail1(self, response):
        if response.url.find("_") == -1:
            try:
                item_image_num = int(response.xpath("/html/body/div[4]/div[2]/div[3]/div[1]/a/text()").extract()[-2])
            except Exception as e:
                print("Error：{0}".format(e))
                item_image_num = 2
            for i in range(2, item_image_num + 1):
                next_url = response.url[:len(response.url) - 5] + str(i) + ".html"
                yield Request(url=next_url, callback=self.parse_datail1)
        # 进入详情页 获取照片url
        image_urls = []
        image_urls.append(response.xpath("/html/body/div[4]/div[2]/div[3]/a/img/@src").extract()[0])
        item = ImageItem()
        item["image_urls"] = image_urls
        yield item



