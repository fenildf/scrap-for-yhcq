#!/usr/bin/env python
#coding:utf8
#author shengaofeng@gmail.com
import sys
reload(sys)
sys.setdefaultencoding('utf-8') 
import simplejson as json
import re
import pdb

HTML_PRE = """
<?xml version="1.0" encoding="utf-8" standalone="no"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title></title>
</head>
<body>
"""

HTML_POST = """
</body>
</html>
"""

TITLE_TEMPLATE = """  <header>
    <h4>{title}</h4>
</header> """
AUTHOR_TEMPLATE = "<h5>{author}</h5>"
CONTENT_TEMPLATE = """<article>{content}</article>"""

volume = open(sys.argv[1]) #"2015年第2期.volume.json")
content = open(sys.argv[2]) #"2015年第2期.content.json")
contents = content.readlines()
volumes = json.loads(volume.readline())
volume.close()
content.close()
preface = open("preface.html","w")
preface.write(HTML_PRE)
print(volumes["volume"])
title = TITLE_TEMPLATE.format(title = volumes["volume"].encode('utf8'))
preface.write(title)
#print(volumes['intro'])
pras = volumes['intro'].split("\n")
all_pra = []
for pra in pras:
    all_pra.append("""<p style="text-indent:10%">{pra}</p>""".format(pra = pra.encode('utf8')))
preface.write(CONTENT_TEMPLATE.format(content = "".join(all_pra)))
preface.write(HTML_POST)
preface.close()


articles = []
for cont in contents:
    content = json.loads(cont)
    if content["page"] > 1:
        continue
    article = {}
    article["title"] = content["title"]
    article["author"] = content["author"]
    article["volume"] = content["volume"]
    main = []
    for cnt1 in contents:
        cnt = json.loads(cnt1)
        if cnt.get("news_id").startswith(content['news_id']):
            main.append(cnt)
#    print(len(main))
    article['main'] = main
    articles.append(article)
count = 1
clear_style = re.compile("<.*?FONT.*?>")
static_path = "/home/shen/temp/images/"
for art in articles:
    chap = open("chap" + str(count) + ".html","w")
    chap.write(HTML_PRE)
    title = TITLE_TEMPLATE.format(title = art["title"].encode('utf8'))
    chap.write(title)
    author = AUTHOR_TEMPLATE.format(author = art["author"].encode('utf8'))
    all_content = []
    for cnt in art['main']:
        all_content.append((cnt['page'],cnt['content'],cnt['images'], cnt['image_urls']))
    all_content.sort()
    mm = []
    flag = False
    for page,content,images,img_urls in all_content:
#        print images
        temp_count = 0
        for img_url in img_urls:
            content = (static_path + images[temp_count]['path']).join(content.split(img_url[20:].encode('utf8')))
#            if img_url.find(u"其骧代表作") > 0:
#                flag = True
            temp_count += 1
        mm.append(content)
#        if flag:
#            pdb.set_trace()
    content_to_write = CONTENT_TEMPLATE.format(content = "".join(mm).encode('utf8'))
    chap.write(content_to_write)
    chap.write(HTML_POST)
    chap.close()
    count += 1

if __name__=="__main__":
    pass
