# -*- coding: utf-8 -*-
import scrapy
from china_rental_scrapy.items import CityURLItem, DistrictURLItem
from selenium import webdriver

class CityrentalurlSpider(scrapy.Spider):
    name = 'cityrentalurl'
    allowed_domains = ['zufang.leju.com']
    start_urls = ['http://zufang.leju.com/city']
    cityurls = []
    districurls = []

    def parse(self, response):
        links = response.css('div#province-con a::attr(href)').extract()
        pinyins = response.css('div#province-con a::attr(data-pinyin)').extract()
        citynames = response.css('div#province-con a::attr(title)').extract()
        letter = response.css('div#province-con a::attr(data-letter)').extract()

        for (cityname, pinyin, letter, link) in zip(citynames, pinyins, letter, links):    
            item = CityURLItem()
            rental_link = "http://" + link.split('/')[2].split('.')[0] + ".zufang.leju.com/house/"
            item['cityname'] = cityname
            item['cityname_pinyin'] = pinyin            
            item['link'] = rental_link
            # yield item
            self.cityurls.append(item)


        for item in self.cityurls:
            yield scrapy.Request(item['link'].encode('ascii'), self.district_parse)

    def district_parse(self, response):
        atags = response.css('div.choose div.dt-line a')
        for atag in atags:
            item = DistrictURLItem()
            item['districname'] = atag.xpath('text()').extract()
            item['link'] = atag.xpath('@href').extract()
            item['districname_pinyin'] = 'none'
            yield item
            self.districurls.append(item)