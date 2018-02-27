# -*- coding: utf-8 -*-
import scrapy
from tencent.items import TencentItem
import re


class TencentspiderSpider(scrapy.Spider):
    name = 'tencentSpider'
    allowed_domains = ['hr.tencent.com']

    start_urls = [
        'https://hr.tencent.com/position.php?&start=0'
    ]

    def parse(self, response):
        items = response.xpath('//tr[@class="even"] | //tr[@class="odd"]')
        for each in items:
            item = TencentItem()
            try:
                name = each.xpath('./td[1]/a/text()').extract()
                link = each.xpath('./td[1]/a/@href').extract()
                style = each.xpath('./td[2]/text()').extract()
                num = each.xpath('./td[3]/text()').extract()
                location = each.xpath('./td[4]/text()').extract()
                time = each.xpath('./td[5]/text()').extract()

                item['positionName'] = name[0].encode('utf-8')
                item['positionLink'] = link[0].encode('utf-8')
                item['positionStyle'] = style[0].encode('utf-8')
                item['positionNumber'] = num[0].encode('utf-8')
                item['positionLocation'] = location[0].encode('utf-8')
                item['positionTime'] = time[0].encode('utf-8')
            except:
                pass

            count = re.search(('\d+'), response.url).group(0)
            page = int(count) + 10
            url = re.sub('\d+', str(page), response.url)

            yield scrapy.Request(url, callback=self.parse)

            yield item


