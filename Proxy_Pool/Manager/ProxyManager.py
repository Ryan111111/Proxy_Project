# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     ProxyManager.py  
   Description :  
   Author :       JHao
   date：          2016/12/3
-------------------------------------------------
   Change Activity:
                   2016/12/3: 
-------------------------------------------------
"""
__author__ = 'JHao'

from DB.DbClient import DbClient
from Util.GetConfig import GetConfig
from Util.LogHandler import LogHandler
from ProxyGetter.getFreeProxy import GetFreeProxy


class ProxyManager(object):
    """
    ProxyManager
    """

    def __init__(self):
        self.db = DbClient()
        self.config = GetConfig()
        self.raw_proxy_queue = 'raw_proxy'
        self.log = LogHandler('proxy_manager')
        self.useful_proxy_queue = 'useful_proxy'

    def refresh(self):
        """
        获取新代理，存放在数据表中
        :return:
        """
        for proxyGetter in self.config.proxy_getter_functions:
            proxy_set = set() #代理去重
            # fetch raw proxy
            ip_list = getattr(GetFreeProxy, proxyGetter.strip())()
            # print "获取iplist：",ip_list
            for proxy in ip_list:
                if proxy.strip():
                    self.log.info('{func}: fetch proxy {proxy}'.format(func=proxyGetter, proxy=proxy))
                    proxy_set.add(proxy.strip())

            #存储到数据表中
            self.db.changeTable(self.raw_proxy_queue)    #打开目标数据表
            for proxy in proxy_set:                      #将数据放入数据库
                self.db.put(proxy)

    def get(self):
        """
        return a useful proxy
        :return:
        """
        self.db.changeTable(self.useful_proxy_queue)
        return self.db.get()
        # return self.db.pop()

    def delete(self, proxy):
        """
        delete proxy from pool
        :param proxy:
        :return:
        """
        self.db.changeTable(self.useful_proxy_queue)
        self.db.delete(proxy)

    def getAll(self):
        """
        get all proxy from pool
        :return:
        """
        self.db.changeTable(self.useful_proxy_queue)
        return self.db.getAll()

    def get_status(self):
        self.db.changeTable(self.raw_proxy_queue)
        total_raw_proxy = self.db.get_status()
        self.db.changeTable(self.useful_proxy_queue)
        total_useful_queue = self.db.get_status()
        return {'raw_proxy': total_raw_proxy, 'useful_proxy': total_useful_queue}

if __name__ == '__main__':
    pp = ProxyManager()
    pp.refresh()
    print(pp.get_status())
