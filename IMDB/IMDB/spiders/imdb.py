# -*- coding: utf-8 -*-
import scrapy
import re


class ImdbSpider(scrapy.Spider):
    name = 'imdb'
    allowed_domains = ['imdb.com']
    start_urls = [
            'http://www.imdb.com/search/title?title_type=documentary&sort=moviemeter,asc&page='+str(i)+'&ref_=adv_nxt' for i in range(200)
        ]

    def parse(self, response):
        for item in response.css('div.lister-item-content'):
            yield {
                'index': [self.parseIndex(item.css('span.lister-item-index::text').extract())],
                'year': [self.parseYear(item.css('span.lister-item-year::text').extract())],
                'title': item.xpath('./h3/a/text()').extract(),
                'url': ['http://www.imdb.com/'+item.xpath('./h3/a/@href').extract()[0]],
                'certificate': [self.parseCert(item.xpath('./p/span[@class="certificate"]/text()').extract())],
                'runtime': [self.parseRuntime(item.xpath('./p/span[@class="runtime"]/text()').extract())],
                'genre': item.xpath('./p/span[@class="genre"]/text()').extract()[0].replace(',','').split(),
                'rating': [self.parseRating(item.xpath('./div/div/strong/text()').extract())],
                'votes': [self.parseVote(item.xpath('./p/span[@name="nv"]/text()').extract())],
                'gross': [self.parseGross(item.xpath('./p/span[@name="nv"]/text()').extract())]
            }
    def parseRating(self, l):
        if l:
            return l[0]
        else:
            return 'NoRating'

    def parseCert(self, l):
        if l:
            return l[0]
        else:
            return 'Unknown'


    def parseYear(self, l):
        if l:
            p = re.compile(r'\d{4}')
            temp = re.findall(p, l[0])
            if temp:
                return temp[0]
            else:
                return '1950'

        else:
            return '1950' # we abort 1950


    def parseIndex(self, l):
        if l:
            a = len(l[0])
            return l[0][:a-1]
        else:
            return '0'

    def parseVote(self, l):
        if l:
            return l[0]
        else:
            return '0'

    def parseGross(self, l):
        if len(l) == 2:
            a = len(l[1]) # get rid of $ and M
            return l[1][1:a-1]
        else:
            return '0.00'

    def parseRuntime(self, l):
        if l:
            return l[0].split()[0]
        else:
            return '0'