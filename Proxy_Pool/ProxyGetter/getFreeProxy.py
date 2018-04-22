# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     GetFreeProxy.py
   Description :  抓取免费代理
   Author :       JHao
   date：          2016/11/25
-------------------------------------------------
   Change Activity:
                   2016/11/25: 
                   这一部分考虑用scrapy框架代替
-------------------------------------------------
"""
import re
import requests
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy


try:
    from importlib import reload   #py3 实际不会实用，只是为了不显示语法错误
except:
    import sys     # py2
    reload(sys)
    sys.setdefaultencoding('utf-8')




from Util.utilFunction import robustCrawl, getHtmlTree, getHTMLText,getHtmlTreeByBrowser

# for debug to disable insecureWarning
requests.packages.urllib3.disable_warnings()

HEADER = {'Connection': 'keep-alive',
          'Cache-Control': 'max-age=0',
          'Upgrade-Insecure-Requests': '1',
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
          'Accept-Encoding': 'gzip, deflate, sdch',
          'Accept-Language': 'zh-CN,zh;q=0.8',
          }


class GetFreeProxy(object):
    """
    获取代理
    """
    def __init__(self):
        pass

    @staticmethod
    @robustCrawl
    def freeProxyFirstBYBrowser(page=5):
        """
        抓取快代理IP前5页的内容 http://www.kuaidaili.com/
        :return:
        """
        # 浏览器对象
        driver = webdriver.Chrome()
        url_list = ('http://www.kuaidaili.com/free/inha/{page}/'.format(page=page) for page in range(1, page + 1))
        arr = []

        try:
            for url in url_list:
                tree = getHtmlTreeByBrowser(url, driver)
                proxy_list = tree.xpath('.//div[@id="list"]//table//tbody/tr')
                for proxy in proxy_list:
                    arr.append(':'.join(proxy.xpath('./td/text()')[0:2]))
        except:
            print "获取快代理ip报错"
        finally:
            if driver: driver.close()
        return arr


    @staticmethod
    @robustCrawl
    def freeProxySecondByBrowser():
        """
         http://www.bugng.com/ 爬取虫代理前5页的内容
        :return:
        """
        # 浏览器对象
        driver = webdriver.Chrome()

        url_list = ["http://www.bugng.com/gngn?page=%s" % i for i in range(1, 5)]
        arr = []
        try:
            for url in url_list:
                print url
                tree = getHtmlTreeByBrowser(url, driver)

                proxy_list = tree.xpath('.//tbody[@id="target"]//tr')
                for proxy in proxy_list[1:]:
                    arr.append(':'.join(proxy.xpath('./td/text()')[0:2]))

        except:
            print "抓取bugng理ip报错"
        finally:
            if driver: driver.close()
        return arr


    @staticmethod
    @robustCrawl
    def freeProxyThirdBYBrowser():
        """
         http://www.bugng.com/gngn?page=2  米扑代理 第一页
        :return:
        """
        #TODO 该代理网站端口号是图片
        # 浏览器对象
        driver = webdriver.Chrome()

        url_list = ["https://proxy.mimvp.com/free.php?proxy=in_hp&sort=&page=1"]
        arr = []
        try:
            for url in url_list:
                print url
                tree = getHtmlTreeByBrowser(url, driver)

                proxy_list = tree.xpath('.//div[@class="free-list"]//table//tr')
                for proxy in proxy_list[1:]:
                    arr.append(':'.join(proxy.xpath('./td/text()')[1:3]))

        except:
            print "抓取米扑理ip报错"
        finally:
            if driver: driver.close()
        return arr


    @staticmethod
    @robustCrawl
    def freeProxyFourthBYBrowser():
        """
        抓取西刺代理 http://api.xicidaili.com/第一页内容
        :return:
        """
        url_list = ['http://www.xicidaili.com/nn',  # 高匿
                    #'http://www.xicidaili.com/nt',  # 透明
                    ]
        arr = []
         # 浏览器对象
        driver = webdriver.Chrome()
        try:
            for each_url in url_list:
                tree = getHtmlTreeByBrowser(each_url,driver)
                proxy_list = tree.xpath('.//table[@id="ip_list"]//tr')
                for proxy in proxy_list:
                    arr.append(':'.join(proxy.xpath('./td/text()')[0:2]))
        except:
            print "获取西刺代理ip报错"
        finally:
            if driver: driver.close()
        return arr


    @staticmethod
    @robustCrawl
    def freeProxyFifthBYBrowser():
        """
         http://www.xdaili.cn/freeproxy  讯代理 获取第一页 高匿
        :return:
        """
        # 浏览器对象
        driver = webdriver.Chrome()
        url = "http://www.xdaili.cn/freeproxy"
        arr = []
        try:
            print url

            tree = getHtmlTreeByBrowser(url, driver)

            proxy_list = tree.xpath('.//tr[@class="warning"]')
            for proxy in proxy_list:
                arr.append(':'.join(proxy.xpath('./td/text()')[0:2]))

        except:
            print "抓取讯代理ip报错"
        finally:
            if driver: driver.close()
        return arr

    @staticmethod
    @robustCrawl
    def freeProxySixthBYBrowser():
        """
         http://www.ip181.com/  云代理 前10页 高匿
        :return:
        """
        # 浏览器对象
        driver = webdriver.Chrome()

        url_list = ["http://www.ip3366.net/?stype=1&page=%s" % i for i in range(1,10)]
        arr = []
        try:
            for url in url_list:
                print url
                tree = getHtmlTreeByBrowser(url, driver)

                proxy_list = tree.xpath('.//div[@id="list"]//table//tr')
                for proxy in proxy_list[1:]:
                    arr.append(':'.join(proxy.xpath('./td/text()')[0:2]))

        except:
            print "抓取云代理ip报错"
        finally:
            if driver: driver.close()
        return arr

    #
    # @staticmethod
    # @robustCrawl
    # def freeProxySecondByBrowser(proxy_number=100):
    #     """
    #     抓取代理66 http://www.66ip.cn/  66代理
    #     :param proxy_number: 代理数量
    #     :return:
    #     """
    #     driver = webdriver.Chrome()
    #     arr = []
    #
    #     url_list = ['http://www.66ip.cn/1.html']
    #     print url_list
    #     try:
    #         for each_url in url_list:
    #             tree = getHtmlTreeByBrowser(each_url, driver)
    #             proxy_list = tree.xpath('.//div[@id="main"]//div[@class="containerbox boxindex"]//div[@align="center"]//table//tr')
    #             for proxy in proxy_list[1:]:
    #                 arr.append(':'.join(proxy.xpath('./td/text()')[0:2]))
    #     except:
    #         print "获取代理66ip报错"
    #     finally:
    #         if driver: driver.close()
    #     return arr

    # @staticmethod
    # @robustCrawl
    # def freeProxyFifthBYBrowser():
    #     """
    #     抓取guobanjia http://www.goubanjia.com/free/gngn/index.shtml,透明，匿名，高匿
    #     :return:
    #     """
    #     #浏览器对象
    #     driver = webdriver.Firefox()
    #
    #     url_list = ["http://www.goubanjia.com/free/gngn/index%s.shtml" % i for i in range(1,10)]
    #     arr = []
    #     try:
    #         for url in url_list:
    #             tree = getHtmlTreeByBrowser(url, driver)
    #             proxy_list = tree.xpath('.//div[@id ="list"]//tr')
    #             for each_proxy in proxy_list[1:]:
    #                 ip =''.join(each_proxy.xpath('./td/text()')[0])
    #                 arr.append(ip)
    #     except:
    #         print "抓取guobanjia代理ip报错"
    #     finally:
    #         if driver: driver.close()
    #     return arr

    # @staticmethod
    # @robustCrawl
    # def freeProxySixthBYBrowser():
    #     """
    #     抓取无忧代理 http://www.data5u.com/   高匿，匿名
    #     :return:
    #     """
    #     # 浏览器对象
    #     driver = webdriver.PhantomJS()
    #     url = "http://www.data5u.com/"
    #     arr = []
    #     try:
    #         tree = getHtmlTreeByBrowser(url, driver)
    #
    #         proxy_list = tree.xpath('.//ul[@class="l2"]')
    #         for proxy in proxy_list:
    #             arr.append(':'.join(proxy.xpath('./span/li/text()')[0:2]))
    #
    #     except:
    #         print "抓取无忧代理ip报错"
    #     finally:
    #         if driver: driver.close()
    #     return arr

    # @staticmethod
    # @robustCrawl
    # def freeProxySeventhBYBrowser():
    #     """
    #      http://www.ip181.com/ 普匿，透明
    #     :return:
    #     """
    #     # 浏览器对象
    #     driver = webdriver.Firefox()
    #     url = "http://www.ip181.com/"
    #     arr = []
    #     try:
    #         print url
    #
    #         tree = getHtmlTreeByBrowser(url, driver)
    #
    #         proxy_list = tree.xpath('.//tr[@class="warning"]')
    #         for proxy in proxy_list:
    #             arr.append(':'.join(proxy.xpath('./td/text()')[0:2]))
    #
    #     except:
    #         print "抓取ip181代理ip报错"
    #     finally:
    #         if driver: driver.close()
    #     return arr

if __name__ == '__main__':

    gg = GetFreeProxy()
    arr_list = gg.freeProxyFourthBYBrowser()
    print arr_list
    # from Util.utilFunction import validUsefulProxy
    # for proxy in arr_list:
    #     validUsefulProxy(proxy)
    # for e in gg.freeProxyFirst():
    #     print e

    # for e in gg.freeProxySecond():
    #     print e

    # for e in gg.freeProxyThird():
    #     print e
    #
    # for e in gg.freeProxyFourth():
    #     print e

    # for e in gg.freeProxyFifth():
    #     print(e)