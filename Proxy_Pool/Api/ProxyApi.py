# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     ProxyApi.py  
   Description :  
   Author :       JHao
   date：          2016/12/4
-------------------------------------------------
   Change Activity:
                   2016/12/4: 
-------------------------------------------------
"""
__author__ = 'JHao'

import sys

from flask import Flask, jsonify, request

sys.path.append('../')

from Manager.ProxyManager import ProxyManager

app = Flask(__name__)


api_list = {
    'get': u'get an usable proxy',
    'refresh': u'refresh proxy pool',
    'get_all': u'get all proxy from proxy pool',
    'delete?proxy=127.0.0.1:27017': u'delete an unable proxy',
}


@app.route('/')
def index():
    return jsonify(api_list)


@app.route('/get/')
def get():
    proxy = ProxyManager().get()
    return proxy


@app.route('/refresh/')
def refresh():
    # TODO refresh会有守护程序定时执行，由api直接调用性能较差，暂不使用
    # ProxyManager().refresh()
    pass
    return 'success'


@app.route('/get_all/')
def getAll():
    proxies = ProxyManager().getAll()
    updata_proxies = list(proxies)[-20:]   #获取后面更新的20条新代理
    return jsonify(updata_proxies)


@app.route('/delete/', methods=['GET'])
def delete():
    proxy = request.args.get('proxy')
    ProxyManager().delete(proxy)
    return 'success'


@app.route('/get_status/')
def get_status():
    status = ProxyManager().get_status()
    return jsonify(status)


def run():
    try:
        app.run(host='0.0.0.0', port=5000)
    except:
        run()

if __name__ == '__main__':
    run()

