#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author:     chenjianzhong
@contact:    530827182.com
@others:     All by Jianzhong, All rights reserved-- Created on 2019/5/12
@desc:
"""




import datetime
import unittest
import os
from BeautifulReport import BeautifulReport

from utils.output import new_report
from utils.sendEmails import sendEmailFile


if __name__ == '__main__':


    # 测试报告名称
    date = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    reportname = "TestReport_{}".format(date)

    # 测试开始时间
    start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("====== 测试开始时间: " + str(start_time))

    # 获取测试用例和报告路径----当run.py放在项目最外层时使用
    # case_path = os.path.join(os.getcwd(), "testcase")
    # report_path = os.path.join(os.getcwd(), 'report')

    # 获取测试用例和报告路径----当run.py放在testcase文件夹里面时使用
    case_path = os.getcwd()
    projectDir = os.path.abspath(os.path.dirname(os.getcwd()))
    report_path = os.path.join(projectDir, 'report')
    print('====== 测试用例路径：' + case_path)
    print('====== 测试报告路径：' + report_path)

    # 用例加载
    suite = unittest.defaultTestLoader.discover(case_path, pattern="test*.py", top_level_dir=None)
    # 执行并结合beautifulreport生成报告
    # BeautifulReport(suite).report(filename=reportname, description='baidu-UI测试', log_path=report_path)
    run = BeautifulReport(suite)
    run.report(filename=reportname, description='熊猫公交--接口自动化测试', log_path=report_path)
    # testcasesSum = run.all_case_counter
    failcasesSum = run.failure_count
    caseSuccessSum = run.success_count
    skippedCaseSum = run.skipped
    # testcasesSum = failcasesSum + caseSuccessSum + skippedCaseSum
    testcasesSum = run.testsRun   #测试用例总数
    successRate = caseSuccessSum/testcasesSum
    successRateStr = (str(successRate*100))[:5] +"%"
    print('测试用例总数 ： ' + str(testcasesSum))
    print('失败测试用例数 ： ' + str(failcasesSum))
    print('成功测试用例数 ： ' + str(caseSuccessSum))
    print('跳过测试用例数 ： ' + str(skippedCaseSum))
    print('测试用例通过率 ： ' + str(successRateStr))



    # 测试结束时间
    end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("====== 测试结束时间: " + str(end_time))

    # ------测试完成，邮件发送-----实操可用----
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_report('report')



    sendEmailFile(new_report('report'),
                  "---------附件是 熊猫公交后台 testcaseReport--------\n---------caseName : 熊猫公交后台主流程接口用例---------\n----------此报告自动不定时发送，请查阅，谢谢！----------\n---------预览不方便时，建议您下载到本地进行查阅--------\n这份测试报告的生成时间是 ： {nowTime}  \ncase总量：{testcasesSum}    失败数量：{failcasesSum}    成功数量：{caseSuccessSum}  跳过数量：{skippedCaseSum} \ncase通过率：{successRateStr}".format(
                      nowTime = nowTime, testcasesSum = testcasesSum,
                      failcasesSum = failcasesSum,
                      caseSuccessSum = caseSuccessSum,
                      skippedCaseSum = skippedCaseSum,
                      successRateStr=successRateStr
                  ), new_report('report'))
    print("----------发送邮件---------")










