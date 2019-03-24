# -*- coding: utf-8 -*-
import scrapy
import re
from lianjia.items import LianjiaItem


class LianjiaspiderSpider(scrapy.Spider):
    name = 'lianjiaSpider'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://bj.lianjia.com/zufang/dongcheng/']

    # 找到每个行政区的url     https://bj.lianjia.com/zufang/dongcheng/
    def parse(self, response):
        district_url_list = response.xpath('//*[@id="filter"]/ul[2]/li/a/@href').extract()[1:]
        for district_url in district_url_list:
            district_url = 'https://bj.lianjia.com' + district_url
            yield scrapy.Request(url=district_url, callback=self.district_url_parse,
                                 meta={'district_url': district_url})

    # 找到每个行政区的分页url    https://bj.lianjia.com/zufang/dongcheng/pg1/#contentList
    def district_url_parse(self, response):
        district_url = response.meta['district_url']
        district_page_num = response.xpath('//*[@id="content"]/div[1]/div[2]/@data-totalpage').extract_first()
        if district_page_num:    # 有的地区0套房子，比如怀柔区
            for page in range(1, int(district_page_num)+1):
                uptown_url = (district_url + 'pg%s/#contentList') % page
                yield scrapy.Request(url=uptown_url, callback=self.house_url_parse)

    # 找到每个房子的url    https://bj.lianjia.com/zufang/BJ2196273851699306496.html
    def house_url_parse(self, response):
        house_url_list = response.xpath('//*[@id="content"]/div[1]/div[1]/div/div/p[1]/a/@href').extract()
        for house_url in house_url_list:
            house_url = 'https://bj.lianjia.com' + house_url
            yield scrapy.Request(url=house_url, callback=self.detail_parse)

    # 详情页提取数据
    def detail_parse(self, response):
        item = LianjiaItem()
        # 经纬度
        longitude_latitude = response.xpath('/html/body/div[3]/script/text()').extract_first()
        longitude = re.findall("longitude: '(.*)',", longitude_latitude, re.M)[0]
        # longitude = float(longitude)
        latitude = re.findall("latitude: '(.*)'", longitude_latitude, re.M)[0]
        # latitude = float(latitude)

        # 房子详情
        plot = response.xpath('/html/body/div[3]/div[1]/div[3]/p/text()').extract_first().split(' ')[0]   # 小区
        time = response.xpath('/html/body/div[3]/div[1]/div[3]/div[1]/text()').extract()[1].split(' ')[1]  # 上架时间
        money = response.xpath('//*[@id="aside"]/p[1]/span/text()').extract_first()     # 租金
        typ = response.xpath('//*[@id="aside"]/ul[1]/p/span[2]/text()').extract_first()    # 户型
        area = response.xpath('//*[@id="aside"]/ul[1]/p/span[3]/text()').extract_first()    # 面积
        orientation = response.xpath('//*[@id="aside"]/ul[1]/p/span[4]/text()').extract_first()   # 朝向
        subway = response.xpath('//*[@id="around"]/ul/li//text()').extract()   # 地铁
        subway = ''.join(subway).replace(' ', '').replace('\n', '')
        district = response.xpath('//*[@id="mapDetail"]/div[5]/div/div/div[1]/p[1]/span[1]/a[1]/text()').extract_first() # 行政区
        street = response.xpath('//*[@id="mapDetail"]/div[5]/div/div/div[1]/p[1]/span[1]/a[2]/text()').extract_first()  # 街道
        item['plot'] = plot
        item['time'] = time
        item['money'] = money
        item['typ'] = typ
        item['area'] = area
        item['orientation'] = orientation
        item['longitude'] = longitude
        item['latitude'] = latitude
        item['subway'] = subway
        item['district'] = district
        item['street'] = street

        yield item
