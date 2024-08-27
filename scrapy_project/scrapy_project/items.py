# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ScrapyProjectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class AmazonProduct(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    picture = scrapy.Field()
    sub_title = scrapy.Field()
    name_author = scrapy.Field()
    role = scrapy.Field()
    rattings = scrapy.Field()
    tag_product = scrapy.Field()
    type_product = scrapy.Field()
    price = scrapy.Field()
    discription = scrapy.Field()
    pass


class FahasaBook(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    publisher = scrapy.Field()
    supplier = scrapy.Field()
    book_cover_type = scrapy.Field()
    book_cover_size = scrapy.Field()
    product_id = scrapy.Field()
    product_discription = scrapy.Field()
    weight = scrapy.Field()
    page_number = scrapy.Field()
    author = scrapy.Field()
    picture = scrapy.Field()
    current_price = scrapy.Field()
    old_price = scrapy.Field()
    discount = scrapy.Field()
    release_day = scrapy.Field()
    pass


class FahasaBookList(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    lastest_chap = scrapy.Field()
    follow = scrapy.Field()


class Nettruyen(scrapy.Item):
    container = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    discription = scrapy.Field()
    lastest_chap = scrapy.Field()
    type = scrapy.Field()
    view = scrapy.Field()
    follow = scrapy.Field()
    teaser = scrapy.Field()
    condition = scrapy.Field()
    pass


class Truyenqqi(scrapy.Item):
    container = scrapy.Field()
    title = scrapy.Field()
    discription = scrapy.Field()
    view = scrapy.Field()
    condition = scrapy.Field()
    follow = scrapy.Field()
    lastest_chap = scrapy.Field()
    link = scrapy.Field()
    teaser = scrapy.Field()
    tag = scrapy.Field()
    pass


class TheSun(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    picture = scrapy.Field()
    author = scrapy.Field()
    publish_time = scrapy.Field()
    update_time = scrapy.Field()
    pass


class DailyMail(scrapy.Item):
    title = scrapy.Field()
    sub_title = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    picture = scrapy.Field()
    author = scrapy.Field()
    publish_time = scrapy.Field()
    update_time = scrapy.Field()
    pass

