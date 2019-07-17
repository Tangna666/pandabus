#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:     chenjianzhong
@contact:    530827182.com
@others:     All by Jianzhong, All rights reserved-- Created on 2018/8/12
@desc:
"""


# 断言assert_True
def assert_True(self, expr, true_msg=None, false_msg=None):
    try:
        if expr:
            print(true_msg)
        else:
            print(false_msg)

    except Exception as e:
        print(e)