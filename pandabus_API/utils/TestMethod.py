#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:     chenjianzhong
@contact:    530827182.com
@others:     All by Jianzhong, All rights reserved-- Created on 2018/8/12
@desc:
"""

import requests
import json
import re


# post请求
def postMethod(self, url, bodyData, http_headers):
    response = requests.post(url, data=json.dumps(bodyData), headers=http_headers)
    response.encoding = 'utf-8'
    return response


# get请求
def getMethod(self, url, http_headers):
    response = requests.get(url, headers=http_headers)
    response.encoding = 'utf-8'
    return response


# put请求
def putMethod(self, url, bodyData, http_headers):
    response = requests.put(url, data=json.dumps(bodyData), headers=http_headers)
    response.encoding = 'utf-8'
    return response

def putmethod(self, url, http_headers):
    response = requests.put(url,  headers=http_headers)
    response.encoding = 'utf-8'
    return response




# delete请求
def deleteMethod(self, url, http_headers):
    response = requests.delete(url, headers=http_headers)
    response.encoding = 'utf-8'
    return response


# delete请求
def deletesMethod(self, url, bodyData, http_headers):
    response = requests.delete(url, data=json.dumps(bodyData), headers=http_headers)
    response.encoding = 'utf-8'
    return response