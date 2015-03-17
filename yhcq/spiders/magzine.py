# -*- coding: utf-8 -*-
import scrapy
from ..items import  YhcqItem, YhcqVolumeItem
from urlparse import urljoin
import random
from scrapy.shell import inspect_response 
import pdb

class MagzineSpider(scrapy.Spider):
    name = "magzine"
    allowed_domains = ["yhcqw.com"]
	
    start_urls = ["http://www.yhcqw.com"]
    allurls = open("/home/shen/yhcq/yhcq/spiders/yhcqurls.txt")
#        "http://www.yhcqw.com/html/wqhg/2015/19/1519221617281CG97410IHDJJDF51GGI4E.html",

    def start_requests(self):
        for line in self.allurls:
            fields = line.split("###")
#            self.start_urls.append(
            yield scrapy.Request(url = fields[1][:-1], meta = {"volumename":fields[0]})
#            )


    def parse(self, response):
#        pdb.set_trace()
        intro = response.xpath("//table[@style='WIDTH: 510px; BORDER-COLLAPSE: collapse']//td[@class='3']/text()").extract()[0]
        preface = urljoin(response.url,response.xpath("//img[@style='BORDER-RIGHT: #b2d3da 1px solid; BORDER-TOP: #b2d3da 1px solid; MARGIN: 2px; BORDER-LEFT: #b2d3da 1px solid; BORDER-BOTTOM: #b2d3da 1px solid']").extract()[0])
        item = YhcqVolumeItem()
        item['intro'] = intro
        item['preface'] = preface
        item['volume'] = response.xpath("//title/text()").extract()[0].split("_")[0]
        item['volumename'] = response.meta['volumename']
        yield item
        news_id = response.xpath("//script").re("NewsId=(.*?)'\s*\}\);")[0]
        url = "http://www.yhcqw.com/showContent.asp?no-cache=" + str(random.random()) + "&NewsId=" + news_id + "&_="
        yield scrapy.Request(url,callback = self.get_columns, meta = {"volumename":response.meta['volumename']})
        
    def get_columns(self,response):
        urls = response.xpath("//a[@href]/@href").extract()
        for url in urls:
            if url == "#":
                continue
            yield scrapy.Request(urljoin(response.url, url),callback = self.get_article, meta = {"volumename":response.meta['volumename']})

    def get_article(self,response):
#                         http://www.yhcqw.com/html/yjy/2015/18/ 151817927EKHJE9718 A199BDAF93CKAJC.html
#        http://www.yhcqw.com/showContent.asp?no-cache=0.19109658612914593&NewsId=A199BDAF93CKAJC&PageBound=0&_=
        meta_content = {}
        news_id = response.xpath("//script").re("NewsId=(.*?)'\s*\}\);")[0]
        url = "http://www.yhcqw.com/showContent.asp?no-cache=" + str(random.random()) + "&NewsId=" + news_id + "&_="
        meta_content['volumename'] = response.meta['volumename']
        try:
            meta_content['author'] = response.xpath("//td[@height='30']/p/font/text()").extract()[0]
        except:
            meta_content['author'] = ""
        meta_content['news_id'] = news_id

        count = 0
        if response.meta.get("news_id"):
            count = response.meta.get("page")
            count += 1
            meta_content['news_id'] = response.meta.get("news_id")
        else:
            count = 1
        meta_content['page'] = count
        meta_content['title'] = response.xpath("//td[@align='middle'][@height='50']//text()").extract()[0] 
        try:
            meta_content['volume'] = response.xpath("//td[@class='xialan1']/p/text()").extract()[0]
        except:
            meta_content['volume'] = ""
        yield scrapy.Request(url,callback = self.get_content, meta = meta_content)
        next_page = response.xpath(u"//a[@title='下一页']")
        if next_page:
            url_next = urljoin(response.url, next_page[0].xpath("./@href").extract()[0])
            yield scrapy.Request(url_next,callback = self.get_article, meta = meta_content)

    def get_content(self, response):

        item = YhcqItem()
        item['news_id'] = response.meta['news_id']
#        try:
        item['image_urls'] = [urljoin(response.url, x) for x in response.xpath("//img/@src").extract()]
#        except:
#            inspect_response(response)
        item['page'] = response.meta['page']
        item['title'] = response.meta['title']
        item['content'] = response.body.decode('gb18030')
        item['author'] = response.meta['author']
        item['volume'] = response.meta['volume']
        item['volumename'] = response.meta['volumename']
        item['url'] = response.url
        yield item
            
            
