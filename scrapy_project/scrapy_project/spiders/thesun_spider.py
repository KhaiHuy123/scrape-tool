import scrapy
from ..items import TheSun


class TheSunSpiderSpider(scrapy.Spider):
    name = "thesun_spider"
    allowed_domains = ["www.thesun.co.uk"]
    custom_settings = {
        'FEEDS': {
            'thesun.csv': {'format': 'csv', 'overwrite': True, 'encoding': 'utf-8-sig'}
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

    file_name = 'url_list\\world_news.txt'
    start_urls = read_file(file_name)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        index_page = 'https://www.thesun.co.uk/'
        start_url = response.xpath(
            '//*[@id="main-content"]/main/section/div[@class ="sun-row teaser teaser--main"]/div/div '
            '/div[@class="teaser__copy-container"]//a/@href').getall()
        special_page = response.xpath(
            '//*[@id="main-content"]/main/section/div[@class="sun-row teaser teaser--main"]/div/div/'
            'div[@class="teaser__image-container"]/'
            'div[@class="teaser-slug"]/span[contains(text(), "Live Blog")]').getall()
        for url in start_url:
            details_page = index_page + url
            if special_page:
                continue
            yield response.follow(details_page, callback=self.parse_page)

    def parse_page(self, response):
        print('\n' + '*' * 100)
        product_item = TheSun()
        ##############################################################################
        url = response.url
        product_item['url'] = url
        ##############################################################################
        title = response.xpath(
            '//*[@id="main-content"]/section/div//main/article//div[@class="article-top-mobile"]'
            '//div[@class="article-top-mobile__text-container"]/header/'
            'div[@class="article__headline-section"]//h1/text()').get()
        if title == '' or title is None or title == 'None':
            title = response.xpath(
                '//*[@id="main-content"]/section/div[ @class ="featured-video-container"]'
                '//div/div//div[@ class ="article-top-mobile__text-container"]/header/'
                'div[@ class ="article__headline-section"]//h1/text()').get()
            if title == '' or title is None or title == 'None':
                title = response.xpath(
                    '//*[@id="main-content"]/section/div//main/article'
                    '//div[@class="article-top-mobile t-s-background-color--shaded article-top-mobile--liveblog"]'
                    '//div[@ class ="article-top-mobile__text-container"]/header/'
                    'div[@class="article__headline-section"]/h1/text()').get()
        product_item["title"] = title
        ##############################################################################
        picture = response.xpath(
            '//*[@id="main-content"]/section/div[@class="sun-row sun-row__article-content"]/main/article'
            '//div[@class ="article__content"]//figure[@class="article__media"]//a/img/@data-src').getall()
        product_item['picture'] = picture
        ##############################################################################
        combined_text = response.xpath(
            '//div[@class="article__content"]//p//text() | //div[@class="article__content"]//p/a//text()').getall()
        normalized_text = [text.strip() for text in combined_text if text.strip()]
        complete_text = ' '.join(normalized_text)
        product_item['content'] = complete_text
        ##############################################################################

        author = response.xpath(
            '//*[@id="main-content"]/section//div[@class="featured-video-container"]/div/div'
            '//div[@class="article-top-mobile__text-container"]'
            '//div[@class="article__meta article_isFeaturedVideo t-p-border-color"]/div/div/ul/li/a/text()').get()
        if author == '' or author is None or author == 'None':
            author = response.xpath(
                '//*[@id="main-content"]/section/div/main/article/div[@class="article-top-mobile"]'
                '//div[@class="article-top-mobile__text-container"]/div/div//'
                'div[@class="article__author"]/ul/li/a/text()').get()
        product_item['author'] = author
        ##############################################################################

        publish_time = response.xpath(
            '//*[@id="main-content"]/section/div/main/article/div[@class="article-top-mobile"]'
            '//div[@class="article-top-mobile__text-container"]/div/div/ul'
            '//li[@class="article__published"]/time//span/text()').getall()
        if publish_time == [] or publish_time is None or publish_time == 'None' or publish_time == '[]':
            publish_time = response.xpath(
                '//*[@id="main-content"]/section//div[@class="featured-video-container"]/div/div'
                '//div[@class="article-top-mobile__text-container"]'
                '//div[@class="article__meta article_isFeaturedVideo t-p-border-color"]/div/ul'
                '//li[@class="article__published"]/time/span/text()').getall()
        product_item['publish_time'] = publish_time
        ##############################################################################

        update_time = response.xpath(
            '//*[@id="main-content"]/section/div/main/article/div[@class="article-top-mobile"]'
            '//div[@class="article-top-mobile__text-container"]/div/div/ul'
            '//li[@class="article__updated"]/time//span/text()').getall()
        if update_time == [] or update_time is None or update_time == 'None' or update_time == '[]':
            update_time = response.xpath(
                '//*[@id="main-content"]/section//div[@class="featured-video-container"]'
                '//div/div//div[@class="article-top-mobile__text-container"]'
                '//div[@class="article__meta article_isFeaturedVideo t-p-border-color"]/div/ul'
                '//li[@class="article__updated"]/time/span/text()').getall()
        product_item['update_time'] = update_time
        ##############################################################################

        yield product_item

