import scrapy
from ..items import FahasaBookList


class FahasaSpider(scrapy.Spider):
    name = "fahasa_series_spider"
    allowed_domains = ["www.fahasa.com"]
    custom_settings = {
        'FEEDS': {
            'fahasa_product_series.csv': {'format': 'csv', 'overwrite': True, 'encoding': 'utf-8-sig'}
        }
    }
    '''Final version'''
    @staticmethod
    def read_file(filename):
        data = []
        with open(filename, 'r') as file:
            for line in file:
                data.append(line.strip())
        return data

    file_name = 'url_list\\fahasa_books_vanhoc_1.txt'
    start_urls = read_file(file_name)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print('\n' + '*' * 100)
        ##############################################################################
        urls = response.xpath(
            '//*[@id="products_grid"]/li/div/div'
            '//h2[@class = "product-name-no-ellipsis p-name-list fhs-series"]//a/@href').getall()
        ##############################################################################
        lastest_chaps = response.css(
            '#products_grid > li> div > div > div.fhs-series-episode-label::text').getall()
        ##############################################################################
        names = response.xpath(
            '//*[@id="products_grid"]/li/div/div'
            '//h2[@class = "product-name-no-ellipsis p-name-list fhs-series"]//a/text()').getall()
        ##############################################################################
        follows = response.css(
            '#products_grid > li > div > div > div.fhs-series-subscribes::text').getall()
        ##############################################################################
        for url, lastest_chap, name, follow in zip(urls, lastest_chaps, names, follows):
            product_item = FahasaBookList()
            product_item['url'] = url
            product_item['lastest_chap'] = lastest_chap
            product_item['name'] = name
            product_item['follow'] = follow
            yield product_item
