# -*- coding: utf-8 -*-

# Scrapy settings for yhcq project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'yhcq'

SPIDER_MODULES = ['yhcq.spiders']
NEWSPIDER_MODULE = 'yhcq.spiders'
IMAGES_STORE = '/home/shen/temp/images'

ITEM_PIPELINES = {
    'scrapy.contrib.pipeline.images.ImagesPipeline': 1,
    'yhcq.pipelines.YhcqPipeline': 800,
}

DOWNLOAD_DELAY = 2

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'yhcq (+http://www.yourdomain.com)'
