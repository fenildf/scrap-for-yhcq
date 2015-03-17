# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from .items import  YhcqItem, YhcqVolumeItem
import simplejson as json

class YhcqPipeline(object):
    def __init__(self):
		pass
#        self.volume_data = open("/home/shen/temp/yhcq/volumes.json",'w')
#        self.content_data = open("/home/shen/temp/yhcq/contents.json",'w')

    def process_item(self, item, spider):
        if isinstance(item, YhcqItem):
            myitem = dict(item)
            content = open("/home/shen/temp/yhcq/" + myitem["volumename"].decode("utf8").strip() + ".content.json",'a')
            content.write(json.dumps(myitem) + "\n")
            content.close()
        else:
            myitem = dict(item)
            content = open("/home/shen/temp/yhcq/" + myitem["volumename"].decode('utf8').strip() + ".volume.json",'a')
            content.write(json.dumps(myitem) + "\n")
            content.close()

    def close_spider(self, spider):
        pass
#        self.volume_data.close()
#        self.content_data.close()
