# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     utilFunction.py
   Description :  tool function
   Author :       JHao
   date：          2016/11/25
-------------------------------------------------
   Change Activity:
                   2016/11/25: 添加robustCrawl、verifyProxy、getHtmlTree
-------------------------------------------------
"""
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from Util.LogHandler import LogHandler

logger = LogHandler(__name__)


def getHTMLText(url, headers={'user': 'Mozilla/5.0'}):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.text
    except:
        return
        # return response.status_code


# noinspection PyPep8Naming
def robustCrawl(func):
    def decorate(*args, **kwargs):
        try:
            logger.info("开始获取ip")
            return func(*args, **kwargs)
        except Exception as e:
            logger.info(u"sorry, 抓取出错。错误原因:")
            logger.info(e)

    return decorate


def verifyProxy(proxy):
    """
    检查代理格式
    :param proxy:
    :return:
    """
    import re
    verify_regex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}"
    return True if re.findall(verify_regex, proxy) else False


def getHtmlTree(url, **kwargs):
    """
    获取html树
    :param url:
    :param kwargs:
    :return:
    """
    import requests
    from lxml import etree
    header = {'Connection': 'keep-alive',
              'Cache-Control': 'max-age=0',
              'Upgrade-Insecure-Requests': '1',
              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'Accept-Encoding': 'gzip, deflate, sdch',
              'Accept-Language': 'zh-CN,zh;q=0.8',
              }
    # TODO 取代理服务器用代理服务器访问
    html = requests.get(url=url, headers=header, timeout=30).content
    # print html
    return etree.HTML(html)

def getHtmlTreeByBrowser(url, driver):
    """
    获取html树,通过浏览器加载动态资源
    :param url:
    :param kwargs:
    :return:
    """
    from lxml import etree
    import time
    driver.get(url)

    time.sleep(1)
    # TODO 取代理服务器用代理服务器访问
    html = driver.page_source
    # print html
    return etree.HTML(html)



def getHTMLText(url, headers={'user': 'Mozilla/5.0'}):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.text
    except:
        return
        # return response.status_code


def validUsefulProxy(proxy):
    """
    检验代理可以性
    :param proxy:
    :return:
    """
    proxies = {"https": "https://{proxy}".format(proxy=proxy),"http": "http://{proxy}".format(proxy=proxy)}
    try:
        # 超过20秒的代理就不要了，检测网站为美团
        r = requests.get('http://i.waimai.meituan.com/home?lat=32.0513&lng=118.7932', proxies=proxies,timeout=8, verify=False)
       # r = requests.get('https://mainsite-restapi.ele.me/ugc/v2/restaurants/156264754/ratings/scores', proxies=proxies, timeout=8, verify=False)
        if r.status_code == 200:
            logger.debug('%s is ok' % proxy)
            print "ok",proxy
            return True
    except Exception as e:
        logger.info(e)
        print "err",proxy
        return False
