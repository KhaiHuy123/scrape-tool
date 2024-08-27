import scrapy
from ..items import Nettruyen


class NettruyenSpider(scrapy.Spider):
    name = "nettruyen_spider"
    allowed_domains = ["nettruyenco.vn"]
    custom_settings = {
        'FEEDS': {
            'nettruyen.csv': {'format': 'csv', 'overwrite': True,'encoding': 'utf-8-sig'}
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

    file_name = 'url_list\\manga_nettruyen_for_testing.txt'
    start_urls = read_file(file_name)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url,callback=self.parse)

    def parse(self, response):
        print('\n' + '*' * 100)
        ##############################################################################
        url = response.url
        ##############################################################################
        titles = response.css(
            '#ctl00_divCenter > div > div > div.items > div.row > div > figure > figcaption > h3 > a ::text').getall()
        ##############################################################################
        links = response.css(
            '#ctl00_divCenter > div > div > div.items > div.row > div > figure > div > a ::attr(href)').getall()
        ##############################################################################
        pictures = response.css(
            '#ctl00_divCenter > div > div > div.items > div.row > div > figure > div > a > img ::attr(src)').getall()
        ##############################################################################
        lastest_chaps = response.css(
            '#ctl00_divCenter > div > div > div.items > div.row > div > figure >'
            ' figcaption > ul > li:nth-child(1) > a ::text').getall()
        ##############################################################################
        discriptions = response.xpath(
            '*//div[@class="row"]/div//div/div/div/div[@class="row"]/div[@class="item"]'
            '/div/div/div[@class="box_text"]').getall()
        ##############################################################################
        types = response.xpath(
            '*//div[@class="row"]/div//div/div/div/div[@class="row"]/div[@class="item"]'
            '/div/div/div[@class="clearfix"]/div[@class="message_main"]'
            '/p[label[contains( text(),"Thể loại:")]/following-sibling::text()]/text()[2]').getall()
        ##############################################################################
        conditions = response.xpath(
            '*//div[@class="row"]/div//div/div/div/div[@class="row"]/div[@class="item"]'
            '/div/div/div[@class="clearfix"]/div[@class="message_main"]'
            '/p[label[contains(text(),"Tình trạng:")]/following-sibling::text()]/text()[2]').getall()
        ##############################################################################
        views = response.xpath(
            '*//div[@class="row"]/div//div/div/div/div[@class="row"]/div[@class="item"]'
            '/div/div/div[@class="clearfix"]/div[@class="message_main"]'
            '/p[label[contains( text(),"Lượt xem:")]/following-sibling::text()]/text()[2]').getall()
        ##############################################################################
        follows = response.xpath(
            '*//div[@class="row"]/div//div/div/div/div[@class="row"]/div[@class="item"]'
            '/div/div/div[@class="clearfix"]/div[@class="message_main"]'
            '/p[label[contains(text(),"Theo dõi:")]/following-sibling::text()]/text()[2]').getall()
        ##############################################################################
        for title, link, picture, lastest_chap, discription, type, condition, view, follow \
                in zip(titles, links, pictures, lastest_chaps, discriptions, types, conditions, views, follows):
            product_item = Nettruyen()
            product_item['container'] = url
            product_item['title'] = title
            product_item['discription'] = discription
            product_item['lastest_chap'] = lastest_chap
            product_item['type'] = type
            product_item['view'] = view
            product_item['follow'] = follow
            product_item['teaser'] = picture
            product_item['condition'] = condition
            product_item['link'] = link
            yield product_item

