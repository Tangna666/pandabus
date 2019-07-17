#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:     chenjianzhong
@contact:    530827182.com
@others:     All by Jianzhong, All rights reserved-- Created on 2017/2/26
@desc:       
"""
import datetime
import logging
import os
import sys
import time
from logging.handlers import RotatingFileHandler
try:
    iteration_time = os.environ['WEBSERVICE_ITERATION_RUN_TIME']
except KeyError:
    iteration_time = time.strftime("%Y-%m-%d_%H_%M_%S")

# 如果去掉下面这一句，生成的日志就和testcase处于同一个文件夹下面
ROOT_DIR = os.path.abspath(os.path.curdir)

ROOT_DIR = os.path.dirname(ROOT_DIR)

# sys.path.append(ROOT_DIR)
logFile = os.path.join(ROOT_DIR, 'logs')
logFile = os.path.join(logFile, iteration_time)
logLevel = 3   # 1:notset 2:debug  3:info 4:warning 5:error 6:critical

_logLevel = {
    1: logging.NOTSET,
    2: logging.DEBUG,
    3: logging.INFO,
    4: logging.WARNING,
    5: logging.ERROR,
    6: logging.CRITICAL
}

# loggers = {}


def get_logger():
    """    定义2个log handler: RotatingFileHandler and StreamHandler。logLevel 取自配置文件
    :return:
    """
    # global loggers
    funcName = sys._getframe().f_back.f_code.co_filename
    script_name = funcName.split(os.sep)[-1].split('.')[0]

    log_level = logLevel
    log_path = logFile
    if os.path.exists(log_path):
        log_file = os.path.join(log_path, script_name + '.log')
    else:
        os.makedirs(r'%s' % log_path)
        log_file = os.path.join(log_path, script_name + '.log')

    logger = logging.getLogger()    # RootLogger
    logger.setLevel(_logLevel[log_level])
    if not logger.handlers:
        # 1.1 一个handler，用于写入日志文件，每次运行都会产生一个新的日志文件
        # fh = logging.FileHandler(log_file)
        # fh.setLevel(_logLevel[log_level])

        # 1.2 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        # ch.setLevel(logging.ERROR)  # 只有错误信息才会在控制台输出
        ch.setLevel(_logLevel[log_level])

        # 1.3 定义一个RotatingFileHandler，最多备份5个日志文件，每个日志文件最大10M
        # # rh和fh 不要使用
        # rh = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=5)

        rh = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=5, encoding='utf-8')
        rh.setLevel(_logLevel[log_level])

        # 2 定义handler的输出格式
        # formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        formatter = logging.Formatter('%(asctime)s [%(filename)s][line:%(lineno)d][%(name)s][%(levelname)s] %(message)s')
        # fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        rh.setFormatter(formatter)

        # 3 给RootLogger添加handler
        # logger.addHandler(fh)
        logger.addHandler(ch)
        logger.addHandler(rh)
        # loggers.update(dict(name=logger))
    return logger
