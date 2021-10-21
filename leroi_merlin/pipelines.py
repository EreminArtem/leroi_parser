# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import hashlib

import scrapy
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.python import to_bytes


class LeroiMerlinPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client.leroi

    def process_item(self, item, spider):
        self.db[spider.name].insert_one(item)
        return item


class LeroiMerlinPhotoPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for i in item['photos']:
                try:
                    yield scrapy.Request(i)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f'{item["name"]}/{image_guid}.jpg'
