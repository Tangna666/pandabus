#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:     chenjianzhong
@contact:    530827182.com
@others:     All by Jianzhong, All rights reserved-- Created on 2018/8/12
@desc:
"""


import re

# 正则表达式
'''
@功能：在接口返回的response中匹配特定的字符串
@para：
stringOrg：返回的response文本
stringReg：正则表达式
@return：如果匹配成功，则返回匹配结果，否则返回none
'''


def regSearchString( stringOrg, stringReg, substr1, substr2):
    pattern = re.compile(stringReg)
    search = pattern.search(stringOrg)
    if search:
        regSearchStr = search.group(0)
        newStr1 = regSearchStr[substr1:]
        newStr2 = newStr1[:substr2]
        return newStr2
    else:
        return "正则获取失败"


# 断言  assert("About Baidu" in response.text)  # 断言
def assertResponse(strTobeAssert, responseText):
    try:
        assert (strTobeAssert in responseText)
        # return "%s 断言成功" % strTobeAssert
        return True

    except:
        # return "%s 断言失败" % strTobeAssert
        return False


# 多个断言  asserts("About Baidu", "aiqiyi" in response.text)  # 断言
def assertsResponse(strsTobeAssert, responseText):

    for strTobeAssert in strsTobeAssert:
        if strTobeAssert not in responseText:
            print("断言失败的关键字----------"+strTobeAssert)
            return False
    return True


# 多个断言---返回值中不包含   asserts("About Baidu", "aiqiyi" not in response.text)  # 断言
def assertsNotinResponse(strsTobeAssert, responseText):

    for strTobeAssert in strsTobeAssert:
        if strTobeAssert in responseText:
            print("断言失败的关键字----------"+strTobeAssert)
            return False
    return True