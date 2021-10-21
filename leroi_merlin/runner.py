from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from leroi_merlin import settings
from leroi_merlin.spiders.leroi import LeroiSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeroiSpider)

    process.start()
