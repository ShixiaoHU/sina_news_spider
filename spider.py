#!/usr/bin/python
import re
import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime


def getcommentcounts(news_url):
    newsid = re.search('doc-i(.*).shtml',news_url).group(1)
    commenturl = 'http://comment5.news.sina.com.cn/page/info?version=1&format=json&channel=gn&newsid=comos-{}&group=undefined&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=3&t_size=3&h_size=3&thread=1'
    commenturl = commenturl.format(newsid)
    comments = requests.get(commenturl)
    jd = json.loads(comments.text)
    return(jd['result']['count']['show'])


def getnewsdetail(news_url):
    result = {}
    res = requests.get(news_url)
    res.encoding = 'utf-8'
    content = BeautifulSoup(res.text, 'lxml')
    result['title'] = content.select('.main-title')[0].text
    timesource = content.select('.date-source')[0].contents[1].text
    result['time'] = datetime.strptime(timesource,'%Y年%m月%d日 %H:%M')
    result['article'] = '\n'.join([p.text.strip() for p in content.select('#article p')[:-2]])
    result['author'] = content.select('.show_author')[0].text.lstrip('责任编辑： ')
    # result['source'] =
    result['commentcount'] = getcommentcounts(news_url)
    return result

def geturllinks(url):
    res = requests.get(url)
    res.encoding = 'utf-8'
    ss = res.text.replace('try{feedCardJsonpCallback(', '')
    ss = ss.replace(');}catch(e){};', '')
    jd = json.loads(ss)
    newsdetails = []
    for ent in jd['result']['data']:
        newsdetails.append(getnewsdetail(ent['url']))
    return newsdetails

def getnews():
    for i in range(1, 3):
        newslist_url  = 'https://feed.sina.com.cn/api/roll/get?pageid=121&lid=1356&num=20&versionNumber=1.2.4&page={}&encode=utf-8'
        new_url = newslist_url.format(i)
        all_news = geturllinks(new_url)
    return all_news
