#!/usr/bin/python
#coding:utf8
#author shengaofeng@gmail.com
import sys
reload(sys)
sys.setdefaultencoding('utf-8') 

#import xml.etree.ElementTree as ET
import copy
from lxml import etree
import os
import lxml.html.soupparser as soupparser
import simplejson as json
import pdb

NCX_OUTPUT = 'out.ncx'
OPF_OUTPUT = 'out.opf'

tree = etree.parse('lxb.opf')
root = tree.getroot()

infos = json.loads(open(sys.argv[1]).readline())
#print(type(infos))

book_info = {
    "title":infos['volume'],
    "author":u'炎黄春秋编辑部',
    "date":"none",
    "type":"none",
    "language":"zh-cn",
    }

def chap_cmp(x, y):
    if int(x[4:-5]) - int(y[4:-5]) > 0:
        return 1
    elif int(x[4:-5]) - int(y[4:-5]) < 0:
        return -1
    else:
        return 0


book = root.find("./main:metadata/main:dc-metadata",
                    namespaces = dict(main = "http://www.idpf.org/2007/opf"))
for x in book:
    if x.text:
#        try:
        x.text = etree.CDATA(x.text.format(**book_info).decode('utf8'))
#        except:
#            pdb.set_trace()

items = root.find("./main:manifest",
                  namespaces = dict(main = "http://www.idpf.org/2007/opf"))

files = [ x for x in os.listdir(".") if x.endswith(".html") and  x.startswith("chap") ]
files.sort(cmp=chap_cmp)
print files
ids = []
for f in files:
    zz = etree.SubElement(items,'{%s}item' % ("http://www.idpf.org/2007/opf"), 
                          nsmap={None: "http://www.idpf.org/2007/opf"})
    zz.set("id",f.split(".")[0])
    ids.append(f.split(".")[0])
    zz.set("href",f)
    zz.set("media-type","application/xhtml+xml")

spine = root.find("./main:spine", 
                  namespaces = dict(main = "http://www.idpf.org/2007/opf"))

for i in ids:
    zz = etree.SubElement(spine,'{%s}itemref' % ("http://www.idpf.org/2007/opf"), nsmap={None: "http://www.idpf.org/2007/opf"})
    zz.set("idref", i)

tree.write(OPF_OUTPUT)

tree = etree.parse('toc.ncx')
root = tree.getroot()
titles = []
files.insert(0 , "preface.html")
items = root.find("./ns:navMap", namespaces = dict(ns = "http://www.daisy.org/z3986/2005/ncx/"))
for f in files:
    mytree = soupparser.parse(f)
    try:
        titles.append(mytree.xpath('.//h4/text()')[0])
    except:
        titles.append("null")

count = 1
for title in titles:
#    print title[:20]
    zz = etree.SubElement(items,'{%s}navPoint' % ("http://www.daisy.org/z3986/2005/ncx/"), nsmap={None: "http://www.daisy.org/z3986/2005/ncx/"})
    zz.set("id","navPoint-" + str(count))
    zz.set("playOrder",str(count))
    ff = etree.SubElement(zz,'{%s}navLabel' % ("http://www.daisy.org/z3986/2005/ncx/"), nsmap={None: "http://www.daisy.org/z3986/2005/ncx/"})
    text = etree.SubElement(ff,'{%s}text' % ("http://www.daisy.org/z3986/2005/ncx/"), nsmap={None: "http://www.daisy.org/z3986/2005/ncx/"})
    text.text = etree.CDATA(title)
    content = etree.SubElement(zz,'{%s}content' % ("http://www.daisy.org/z3986/2005/ncx/"), nsmap={None: "http://www.daisy.org/z3986/2005/ncx/"})
    content.set("src",files[count - 1])
    count += 1

tree.write(NCX_OUTPUT,  encoding='utf-8', pretty_print=True)
