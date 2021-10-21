import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

from leroi_merlin.items import LeroiMerlinItem


class LeroiSpider(scrapy.Spider):
    name = 'leroi'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/catalogue/ugol-drova-i-sredstva-dlya-rozzhiga/']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[contains(@aria-label, "Следующая страница")]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//a[@data-qa="product-image"]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.parse_item)

    def parse_item(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroiMerlinItem(), response=response)
        loader.add_value('link', response.url)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('price', '//span[@slot="price"]/text()')
        loader.add_xpath(
            'photos',
            "//img[@alt='product image']/@src"
        )
        yield loader.load_item()
