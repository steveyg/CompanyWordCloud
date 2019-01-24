import urllib.request
import ssl
import json
import time
import jieba
import jieba.posseg as pseg
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

#检测分词词性，创建自定义词典
def word_type(string):
    words = pseg.cut(string)
    temp = None
    for word, flag in words:
        if flag == 'n':
            if temp == None:
                temp = word
        elif flag == 'v':
            if temp != None:
                print(temp + word)
                temp = None
        # print('%s %s' % (word, flag))

def handle(list,keywords):
    word = ""
    for item in list:
        s = p.sub("", item['main']['title'])
        # word_type(s)
        seg_list = jieba.cut(s, cut_all=False)
        for seg in seg_list:
            if seg != keywords:
                word = word + " "
                word = word + seg.strip()
    return word

def init():
    del_list = ["订单","取消"] #移除单词
    suggest_list = ["取消订单","单方面取消","单方取消","单方面违约","无故退款","不发货","按时发货"]   #增加词库

    for word in del_list:
        jieba.del_word(word)

    for word in suggest_list:
        jieba.suggest_freq(word,True)

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(
        description='Company Word Cloud')
    argparser.add_argument(
        '-k','--keyword',
        help='The keyword you want to serach'
    )
    args = argparser.parse_args()
    init()
    main(args.keyword)