# -*- coding: utf-8 -*-
import scrapy


class AllrecipesmxSpider(scrapy.Spider):
    name = 'allrecipesmx'
    allowed_domains = ['allrecipes.com.mx']
    start_urls = ['file:///home/hian/Downloads/Empanadas de jamón y queso receta - Recetas de Allrecipes.html',
    # 'http://allrecipes.com.mx/'
    ]

    def parse(self, response):
        recipe = {}

        recipe['name'] = response.xpath(
            '//*[@id="pageContent"]/div[2]/div/div/div[1]/div/section[1]/div/div[2]/h1/span/text()').extract()[0].strip()
        recipe['description'] = response.xpath(
            '//*[@id="pageContent"]/div[2]/div/div/div[1]/div/section[1]/div/div[2]/p/text()').extract()[0].strip()
        recipe['metainfo'] = response.xpath(
            '/html/head/meta[23]/@content').extract()[0]

        recipe['portions'] = int(response.xpath(
            '//*[@id="pageContent"]/div[2]/div/div/div[1]/div/section[2]/h2/small/span/text()').extract()[0][1:-1])
        ingredients = response.xpath(
            '//*[@id="pageContent"]/div[2]/div/div/div[1]/div/section[2]/ul/li/span/@data-original')

        recipe['ingredients'] = [ingredient.extract()
                                 for ingredient in ingredients]

        instructions = response.xpath(
            '//*[@id="pageContent"]/div[2]/div/div/div[1]/div/section[3]/ol/li/span/text()')

        recipe['instructions'] = [instruction.extract()
                                  for instruction in instructions]

        times = response.xpath(
            '//*[@id="pageContent"]/div[2]/div/div/div[1]/div/section[3]/h2/small')

        recipe['preparation'] = ''.join(
            [s + ' ' for s in times.xpath('span[1]/span/text()').extract()]).strip()

        recipe['cooktime'] = ''.join(
            [s + ' ' for s in times.xpath('span[2]/span/text()').extract()]).strip()

        recipe['totaltime'] = ''.join(
            [s + ' ' for s in times.xpath('span[3]/span/text()').extract()]).strip()

        link = response.xpath(
            '//*[@id="currentMainPhotoContainer"]/span/img/@src').extract()

        image = link[0][2:] if link else None

        recipe['image'] = image

        recipe['categories'] = [e for i, e in enumerate(response.xpath(
            '//*[@id="pageContent"]/div[2]/div/div/div[1]/div/ul/li/a/span/text()').extract()) if i > 1]

        recipe['related_recipe'] = [e.strip() for e in response.xpath(
            '//*[@id="pageContent"]/div[2]/div/div/div[1]/div/section[4]/div[1]/ul/li/div/a/div/h3/text()').extract()]

        yield recipe

        for link in response.xpath('//*[@id="pageContent"]/div[2]/div/div/div[1]/div/section[4]/div[1]/ul/li/div/a/@href'):
            yield scrapy.Request(link, callback=self.parse_recipe)
            print(link.extract())


    def parse_recipe(self, response):
        pass
        
