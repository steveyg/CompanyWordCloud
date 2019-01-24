import urllib.request
import ssl
import json
import time
import jieba
import img_utils
import argparse
from urllib import parse
import re
context = ssl._create_unverified_context()
p = re.compile('<[^>]+>')
words = []
class Word():
    def __init__(self,str):
        self.str = str
        self.count = 1

def get(url):
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(url=request,context=context)
    return response.read().decode('utf-8')

def get_list(keywords='亚马逊',page=1):
    url ="https://tousu.sina.cn/api/index/s?keywords="+parse.quote(keywords)+"&type=1&page_size=256&page=" + str(page)
    return get(url)

def main(keywords):
    i = 1
    word = ""
    while True:
        result = get_list(keywords=keywords,page=i)
        json_obj = json.loads(result)
        word = word + handle(json_obj['result']['data']['lists'],keywords)
        current = json_obj['result']['data']['pager']['current']
        page_amount = json_obj['result']['data']['pager']['page_amount']
        print("第{}页处理完成，共{}页".format(current,page_amount))
        if current == page_amount:
            print("处理完成，共{}条投诉数据".format(json_obj['result']['data']['pager']['item_count']))
            break;
        i = i + 1
        time.sleep(1)
    img_utils.draw(word,filename=keywords)

def handle(list,keywords):
    word = ""
    for item in list:
        seg_list = jieba.cut(p.sub("", item['main']['title']), cut_all=False)
        for seg in seg_list:
            if seg != keywords:
                word = word + " "
                word = word + seg.strip()
    return word

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(
        description='Company Word Cloud')
    argparser.add_argument(
        '-k','--keyword',
        help='The keyword you want to serach'
    )
    args = argparser.parse_args()
    main(args.keyword)