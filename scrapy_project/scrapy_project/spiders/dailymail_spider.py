import scrapy
from ..items import DailyMail


class DailyMailSpiderSpider(scrapy.Spider):
    name = "dailymail_spider"
    allowed_domains = ["www.dailymail.co.uk"]
    custom_settings = {
        'FEEDS': {
            'dailymail.csv': {'format': 'csv', 'overwrite': True}
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

    file_name = 'url_list\\topics.txt'
    start_urls = read_file(file_name)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        index_page = "https://www.dailymail.co.uk/"
        recommendations = response.xpath("//*[starts-with(@id, 'p-')]//a/@href").getall()
        main_topic = response.xpath(
            '//*[@id="content"]/div[2]/div[3]/div[1]/div[@class="column-splitter"]/div/div/h2/a').getall()
        hot_topic = response.xpath(
            '//*[@id="content"]/div[2]/div[3]/div[1]/div/h2/a').getall()
        for url in recommendations:
            details_url = index_page + url
            yield response.follow(details_url, callback=self.parse_page)
        for url in main_topic:
            details_url = index_page + url
            yield response.follow(details_url, callback=self.parse_page)
        for url in hot_topic:
            details_url = index_page + url
            yield response.follow(details_url, callback=self.parse_page)

    def parse_page(self, response):
        product_item = Dailymail()
        ##############################################################################
        url = response.url
        product_item["url"] = url
        ##############################################################################
        picture = response.xpath(
            "//*[starts-with(@id, 'i-')]").getall()
        product_item["picture"] = picture
        ###############################################################################
        content = response.xpath(
            "//*[@id='js-article-text']/div/p//text()").getall()
        product_item["content"] = content
        ###############################################################################
        title = response.xpath(
            "//*[@id='js-article-text']/h2/text()").get()
        product_item["title"] = title
        ###############################################################################
        sub_title = response.xpath(
            "//*[@id='js-article-text']/ul/li/strong/text()").getall()
        product_item["sub_title"] = sub_title
        ###############################################################################
        author = response.xpath(
            '//*[@id="js-article-text"]/p[@class="author-section byline-plain"]//a/text()').getall()
        product_item["author"] = author
        ###############################################################################
        publish_time = response.xpath(
            '//*[@id="js-article-text"]/p[@class="byline-section"]'
            '/span[@class="article-timestamp article-timestamp-published"]/time/text()').get()
        product_item["publish_time"] = publish_time
        ###############################################################################
        update_time = response.xpath(
            '//*[@id="js-article-text"]/p[@class="byline-section"]'
            '/span[@class="article-timestamp article-timestamp-updated"]/time/text()').get()
        product_item["update_time"] = update_time
        ###############################################################################

        yield product_item

