import scrapy
from ..items import AmazonProduct
from scrapy.exceptions import NotSupported


class AmazonSpider(scrapy.Spider):
    name = "amazon_spider"
    allowed_domains = ["www.amazon.com.au"]
    custom_settings = {
        'FEEDS': {
            'amazon.csv': {'format': 'csv', 'overwrite': True, 'encoding': 'utf-8'}
        }
    }
    '''Final Version'''
    @staticmethod
    def read_file(filename):
        data = []
        with open(filename, 'r') as file:
            for line in file:
                data.append(line.strip())
        return data

    file_name = '"url_list\\manga_dystopian_amazon.txt"'
    start_urls = read_file(file_name)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        index_page = 'https://www.amazon.com.au/'
        products = response.css(
            '#search > div.s-desktop-width-max.s-desktop-content.s-wide-grid-style-t3'
            '.s-opposite-dir.s-wide-grid-style.sg-row'
            '> div.sg-col-20-of-24.s-matching-dir.sg-col-16-of-20.sg-col.sg-col-8-of-12.sg-col-12-of-16 > div'
            '> span.rush-component.s-latency-cf-section > div.s-main-slot.s-result-list.s-search-results.sg-row'
            '> div > div > div > div > div > div.sg-row')
        for product in products:
            relative_url = product.css('a::attr(href)').get()
            product_url = index_page + relative_url
            yield response.follow(product_url, callback=self.parse_page)
        pass

    def parse_page(self, response):
        print('\n' + '*' * 100)
        product_item = AmazonProduct()
        ##############################################################################
        product_item['url'] = response.url
        ##############################################################################
        product_item["title"] = response.css(
            '#productTitle::text').get()
        ##############################################################################
        product_item["sub_title"] = response.css(
            '#productSubtitle::text').get()
        ##############################################################################
        product_item["name_author"] = response.css(
            '#bylineInfo > span > a::text').get()
        ##############################################################################
        product_item["role"] = response.css(
            '#bylineInfo > span > span > span::text').get()
        ##############################################################################
        product_item["rattings"] = response.css(
            '#acrCustomerReviewText::text').get()
        ##############################################################################
        product_item["tag_product"] = response.css(
            '#zeitgeistBadge_feature_div > div > a > span > span::text').get()
        ##############################################################################
        product_item["type_product"] = response.css(
            '#wayfinding-breadcrumbs_feature_div > ul > li:nth-child(5) > span > a::text').get()
        ##############################################################################

        try:
            product_item['discription'] = response.xpath(
                '//*[@id="bookDescription_feature_div"]/div/div[1]/span/text()').getall()
        except NotSupported:
            product_item['discription'] = response.xpath(
                '//*[@id="bookDescription_feature_div"]/div/div[1]/p/span/text()').getall()
        ##############################################################################
        try:
            product_item["price"] = response.xpath(
                '//*[@id="tmmSwatches"]/ul/li[2]/span/span[3]/span/span/a/text()[2]').get()
        except NotSupported:
            try:
                product_item['price'] = response.xpath(
                    '//*[@id="tmmSwatches"]/ul/li/span/span[3]/span/span/a/text()[2]')
            except NotSupported:
                product_item["price"] = response.xpath(
                    '//*[@id="kcpAppsPopOver"]/span/span/span')
        ##############################################################################
        try:
            product_item['picture'] = response.css(
                '#landingImage::attr(src)').get()
        except NotSupported:
            try:
                product_item['picture'] = response.xpath(
                    '//*[@id="ebooksImgBlkFront"]/@src').get()
            except NotSupported:
                product_item['picture'] = response.xpath(
                    '//*[@id="imgBlkFront"]/@src').get()
        ##############################################################################
        yield product_item

