# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from .items import  YhcqItem, YhcqVolumeItem
import simplejson as json

class YhcqPipeline(object):
    def __init__(self):
        self.volume_data = open("/home/shen/temp/yhcq/volumes.json",'w')
        self.content_data = open("/home/shen/temp/yhcq/contents.json",'w')

    def process_item(self, item, spider):
        if isinstance(item, YhcqItem):
            self.content_data.write(json.dumps(dict(item)) + "\n")
        else:
            self.volume_data.write(json.dumps(dict(item)) + "\n")

    def close_spider(self, spider):
        self.volume_data.close()
        self.content_data.close()
