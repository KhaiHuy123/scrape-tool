import scrapy
from ..items import FahasaBook


class FahasaSpider(scrapy.Spider):
    name = "fahasa_spider"
    allowed_domains = ["www.fahasa.com"]
    custom_settings = {
        'FEEDS': {
            'fahasa_product.csv': {'format': 'csv', 'overwrite': True, 'encoding': 'utf-8-sig'}
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
        if response.status == 499:
            print(f"Retry : {response.status} {response.url}")
        books = response.css('#products_grid > li > div > div > div.products.clearfix > div > a::attr(href)').getall()
        lastest_chap = response.css(
            '#products_grid > li> div > div > div.fhs-series-episode-label::text').getall()
        navigate_link = response.xpath(
            '//*[@id="products_grid"]/li/div/div'
            '//h2[@class = "product-name-no-ellipsis p-name-list fhs-series"]//a/@href').getall()
        follow = response.css(
            '#products_grid > li > div > div > div.fhs-series-subscribes::text').getall()
        for book in books:
            if book in navigate_link:
                continue
            yield response.follow(book, callback=self.parse_page)

    def parse_page(self, response):
        print('\n' + '*' * 100)
        product_item = FahasaBook()
        ##############################################################################
        product_item['url'] = response.url
        ##############################################################################
        product_item["title"] = response.xpath(
            '//*[@id="product_addtocart_form"]/div/div[1]/div[2]/h1/text()[2]').get()
        ##############################################################################
        supplier = response.xpath(
            '//*[@id="product_addtocart_form"]/div/div[1]/div[2]/div[2]/div'
            '//div[@class="product-view-sa-supplier"]//a/text()').get()
        if supplier is None or supplier == '' or supplier == 'None':
            supplier = response.xpath(
                '//*[@id="product_addtocart_form"]/div/div[1]/div[2]/div[2]/div'
                '//div[@class="product-view-sa-supplier"]//span[contains(text(), "Nhà cung cấp:")]'
                '/following-sibling::span[1]/text()').get()
            if supplier is None or supplier == '' or supplier == 'None':
                supplier = response.css(
                    '#product_addtocart_form > div > div.product-essential '
                    '> div.product-essential-detail > div.product-view-sa > div.product-view-sa_one '
                    '> div.product-view-sa-supplier > a::text').get()
        product_item["supplier"] = supplier
        ##############################################################################

        product_item['picture'] = response.css(
            '#image::attr(data-src)').get()
        ##############################################################################
        try:
            product_item["author"] = response.css(
                '//*[@id="product_addtocart_form"]/div/div[1]/div[2]/div[2]/div//div[@class="product-view-sa-author"]'
                '//span[contains(text(), "Tác giả:")]/following-sibling::span[1]/text()').get()
        except:
            product_item["author"] = response.css(
                '#product_addtocart_form > div > div.product-essential > div.product-essential-detail '
                '> div.product-view-sa > div.product-view-sa_one > div.product-view-sa-author > span:nth-child(2)::text').get()
        ##############################################################################
        try:
            product_item["publisher"] = response.xpath(
                '//*[@id="product_addtocart_form"]/div/div[1]/div[2]/div[2]/div//div[@class="product-view-sa-supplier"]'
                '//span[contains(text(), "Nhà xuất bản:")]/following-sibling::span[1]/text()').get()
        except:
            product_item["publisher"] = response.css(
                '#product_addtocart_form > div > div.product-essential > div.product-essential-detail >'
                'div.product-view-sa > div.product-view-sa_two > div.product-view-sa-supplier > span:nth-child(2)::text').get()
        ##############################################################################
        try:
            product_item["current_price"] = response.xpath(
                '//*[contains(@id, "product-price-")]/text()').get()
        except:
            product_item["current_price"] = response.css(
                '[id*="product-price-"]::text')[1].get()
        ##############################################################################
        try:
            product_item["old_price"] = response.xpath(
                '//*[contains(@id, "old-price-")]/text()').get()
        except:
            product_item["old_price"] = response.css(
                '[id*="old-price-"]::text')[1].get()
        ##############################################################################
        try:
            product_item["discount"] = response.xpath(
                '//*[@id="product_addtocart_form"]/div/div[1]/div[2]/div[1]/div/div[1]/div/div/p'
                '//span[@class="discount-percent"]/text()').get()
        except:
            product_item["discount"] = response.css(
                '#catalog-product-details-price > div > p.old-price > span.discount-percent::text').get()
        ##############################################################################
        product_item["release_day"] = response.css(
            '#product_addtocart_form > div > div.product-essential > div.product-essential-detail '
            '> div.product_view_msg::text').getall()
        ##############################################################################
        book_cover_type = response.xpath(
            '//*[@id="product_addtocart_form"]/div/div[1]/div[2]/div[2]/div[2]'
            '/div[@class="product-view-sa-author"]//span[contains(text(), "Hình thức bìa:")]'
            '/following-sibling::span[1]/text()').get()
        if book_cover_type == 'None' or book_cover_type == '' or book_cover_type is None :
            book_cover_type = response.xpath(
                "//*[@id='product_addtocart_form']/div/div[1]/div[2]/div[2]/div"
                "//div[@class='product-view-sa-supplier']//span[contains(text(), 'Hình thức bìa:')]"
                "/following-sibling::span[1]/text()").get()
            if book_cover_type == 'None' or book_cover_type == '' or book_cover_type is None:
                book_cover_type = response.css(
                   '#product_addtocart_form > div > div.product-essential > div.product-essential-detail '
                   '> div.product-view-sa > div.product-view-sa_two > div.product-view-sa-author'
                   ' > span:nth-child(2)::text').get()
                if book_cover_type == 'None' or book_cover_type == '' or book_cover_type is None:
                    book_cover_type = response.xpath(
                        '//*[@id="product_view_info"]/div[2]/div[1]/table/tbody'
                        '/tr[th[contains(text(),"Hình thức")]/text()]/td/text()').get()
        product_item["book_cover_type"] = book_cover_type
        ##############################################################################
        product_item["product_id"] = response.xpath(
            '//*[@id="product_view_info"]/div[2]/div[1]/table/tbody/tr[th[contains(text(),"Mã hàng")]/text()]/td/text()').get()
        ##############################################################################
        product_item["product_discription"] = response.xpath(
            '//*[@id="desc_content"]/p/text()').getall()
        ##############################################################################
        product_item["weight"] = response.xpath(
            '//*[@id="product_view_info"]/div[2]/div[1]/table/tbody'
            '/tr[th[contains(text(),"Trọng lượng (gr)")]/text()]/td/text()').get()
        ##############################################################################
        product_item["book_cover_size"] = response.xpath(
            '//*[@id="product_view_info"]/div[2]/div[1]/table/tbody'
            '/tr[th[contains(text(),"Kích Thước Bao Bì")]/text()]/td/text()').get()
        ##############################################################################
        product_item["page_number"] = response.xpath(
            '//*[@id="product_view_info"]/div[2]/div[1]/table/tbody'
            '/tr[th[contains(text(),"Số trang")]/text()]/td/text()').get()
        ##############################################################################
        yield product_item

