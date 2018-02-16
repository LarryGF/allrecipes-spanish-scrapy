# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


class AllrecipesmxSpider(scrapy.Spider):
    name = 'allrecipesmx'
    allowed_domains = ['allrecipes.com.mx', 'allrecipes.com.ar']
    start_urls = [
                  'http://allrecipes.com.ar/recetas/tipo-de-receta.aspx?o_is=Hub_Breadcrumb',
                  'http://allrecipes.com.mx/recetas/tipo-de-receta.aspx?o_is=RD_Breadcrumb'
                 ]
    recipe = 'recetas?/[0-9]+'
    listing = 'recetas?/[a-zA-Z]'

    rules = (
        Rule (LinkExtractor(allow=(listing,)), callback='parse_type'),
        Rule(LinkExtractor(allow=(recipe,)), callback='parse_recipe')
    )


    def parse(self, response):
        for type in response.xpath('//*[@id="hubsRelated"]/div[1]/div/h5/a/@href'):
            yield scrapy.Request(type.extract(), callback=self.parse_type)
        pass

    def parse_type(self, response):
        for recipe in response.xpath('//*[@id="sectionTopRecipes"]/div/div/h3/a/@href'):
            yield scrapy.Request(recipe.extract(), callback=self.parse_recipe)


    def parse_recipe(self, response):
        recipe = {}

        recipe['url'] = response.url
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
            yield scrapy.Request(link.extract(), callback=self.parse_recipe)

