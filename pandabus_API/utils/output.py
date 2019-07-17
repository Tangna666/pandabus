#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:     chenjianzhong
@contact:    530827182.com
@others:     All by Jianzhong, All rights reserved-- Created on 2018/8/12
@desc:
"""
import os
import sys
import time


# # 显示上一级文件夹
# parDir = os.path.abspath(os.path.dirname(__file__))
# print(parDir)
# # 显示上上级文件夹
# print(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

def new_report(report):
    projectDir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    reportPath = os.path.join(projectDir, report)
    print(reportPath)
    lists = os.listdir(reportPath)
    print(('最新测试结果' + lists[-1]))
    file_new = os.path.join(reportPath, lists[-1])
    print(file_new)
    return file_new

# projectDir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# reportPath = os.path.join(projectDir, "report")
# print(reportPath)
# lists = os.listdir(reportPath)
# print(('最新测试结果' + lists[-1]))
# file_new = os.path.join(reportPath, lists[-1])
# print(file_new)
