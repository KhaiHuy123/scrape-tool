import scrapy
from ..items import Truyenqqi


class TruyenqqiSpider(scrapy.Spider):
    name = "truyenqqi_spider"
    allowed_domains = ["truyenqqq.vn"]
    custom_settings = {
        'FEEDS': {
            'truyenqqi.csv': {'format': 'csv', 'overwrite': True, 'encoding': 'utf-8-sig'}
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

    file_name = 'url_list\\manga_truyenqqi_for_testing.txt'
    start_urls = read_file(file_name)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print('\n' + '*' * 100)
        ##############################################################################
        url = response.url
        ##############################################################################
        titles = response.css(
            '#main_homepage > div.list_grid_out > ul > li > div.book_info > div.book_name.qtip > h3 > a::text').getall()
        ##############################################################################
        links = response.css(
            '#main_homepage > div.list_grid_out > ul > li > div.book_info > div.book_name.qtip > h3 > a ::attr(href)').getall()
        ##############################################################################
        pictures = response.css(
            '#main_homepage > div.list_grid_out > ul > li > div.book_avatar > a > img::attr(src)').getall()
        ##############################################################################
        lastest_chaps = response.css(
            '#main_homepage > div.list_grid_out > ul > li > div.book_info > div.last_chapter > a::attr(title)').getall()
        ##############################################################################
        conditions = response.xpath(
            '//div[@class="book_info"]/div[@class="more-info"]//p[@class="info"][1]/text()').getall()
        ##############################################################################
        views = response.xpath(
            '//div[@class="book_info"]/div[@class="more-info"]//p[@class="info"][2]/text()').getall()
        ##############################################################################
        discriptions = response.xpath(
            '//div[@class="book_info"]/div[@class="more-info"]//div[@class="excerpt"]/text()').getall()
        ##############################################################################
        follows = response.xpath(
            '//div[@class="book_info"]/div[@class="more-info"]//p[@class="info"][3]/text()').getall()
        ##############################################################################
        tags = response.xpath(
            '//div[@class="book_info"]/div[@class="more-info"]//div[@class="list-tags"]')
        ##############################################################################
        for title, link, picture, lastest_chap, discription, tag, condition, view, follow\
                in zip(titles, links, pictures, lastest_chaps, discriptions, tags, conditions, views, follows):
            product_item = Truyenqqi()
            product_item['container'] = url
            product_item['title'] = title
            product_item['discription'] = discription
            product_item['lastest_chap'] = lastest_chap
            tag_data = tag.css('.blue::text').getall()
            product_item['tag'] = tag_data
            product_item['view'] = view
            product_item['follow'] = follow
            product_item['teaser'] = picture
            product_item['condition'] = condition
            product_item['link'] = link
            yield product_item

