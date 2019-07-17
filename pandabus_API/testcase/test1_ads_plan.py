#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:     chenjianzhong
@others:     All by Jianzhong, All rights reserved-- Created on 2018/8/12
@desc:
"""
import time
import datetime
import json
import unittest



from utils import TestMethod
from utils.asserts_Func import assert_True
from utils.baselog import get_logger
from utils.output import new_report
from utils.responseInfo import assertsResponse, regSearchString, assertsNotinResponse
from utils.sendEmails import sendEmailFile

log = get_logger()


# 熊猫公交主流程
class pandabusAPItest(unittest.TestCase):

    global caseName
    global base_url
    global access_token
    global plan_id
    global filekey
    global uploadToken
    global material_id

    # global filekey
    # global uploadToken
    # global accessURL
    # global model_id
    # global filekey1
    # global uploadToken1
    # global accessURL1
    # global video_id

    def setUp(self):
        log.info("-------------------------测试用例开始执行--------------------------")
        global base_url
        base_url = "https://test-ads.deepblueai.com"
        # base_url = Base_Url
        # log.info( 'Base_Url:  '+ Base_Url)

    def tearDown(self):
        global caseName
        log.info("the testcase---------------" + caseName + "-------------- finish !!!")


    def test001_auth_signin(self):
        '''熊猫智行广告平台登陆接口'''
        global access_token
        global caseName
        caseName = "1 熊猫智行广告平台登陆接口"
        log.info("--------------------" + caseName + "------------------开始测试")
        headers = ''
        log.info("headers--------------------" + str(headers))
        parameters = "/api/auth/signin?username=13889813735&password=Admin123456789"
        bodyData = ""
        url = "https://test-sso.deepblueai.com" + parameters
        response = TestMethod.postMethod(self, url, bodyData,  headers)
        # {"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1NjI0MDE2MzMsIn
        access_token = regSearchString(response.text, '"access_token":"(.+?)",', 16, -2)
        log.info("正则--获取运营平台access_token150:  " + access_token)
        log.info("--------------------" + caseName + "------------------测试完毕")
        log.info(response.text)
        time.sleep(1)


    def test002_click_create_adsPlan_btn(self):
        '''点击创建投放计划按钮'''
        global access_token
        global base_url
        global caseName
        caseName = "2 点击创建投放计划按钮"
        log.info("--------------------" + caseName + "------------------开始测试")
        headers = {'Accept': 'application/json','Accept-Encoding':'gzip, deflate, br'
                    ,'Authorization': 'Bearer  ' + access_token}
        log.info("headers--------------------" + str(headers))
        parameters = "/api/v2/ads-op/v3/bus"
        asserts = ['"buses":','"name":"tntest",','"deviceCode":"LJM6HCDC8JAS02698",','"vin":"LJM6HCDC8JAS02698",']
        url = base_url + parameters
        response = TestMethod.getMethod(self, url,  headers)
        log.info(response.text)
        self.assertTrue(assertsResponse(asserts, response.text),"断言失败")
        log.info("--------------------" + caseName + "------------------测试完毕")
        time.sleep(1)


    def test003_add_new_ads_plan(self):
        '''新增投放计划'''
        global access_token
        global base_url
        global caseName
        global plan_id
        caseName = "3 新增投放计划"
        log.info("--------------------" + caseName + "------------------开始测试")
        headers = {'Accept': 'application/json', 'Accept-Encoding':'gzip, deflate, br',
                    'Content-Type':'application/json; charset=utf-8','Authorization': 'Bearer  ' + access_token}
        log.info("headers--------------------" + str(headers))
        parameters = "/api/v2/ads-op/v3/plan"
        asserts = ['"success":true,','"reason":"Created Success.",']
        url = base_url + parameters
        bodyData = {
                        "name":"test00001",
                        "busIds":[
                            15
                        ],
                        "startTime":1625147576097,
                        "endTime":1625233976097
                    }
        response = TestMethod.postMethod(self, url, bodyData,  headers)
        # {"success":true,"reason":"Delete Success","id":43}
        plan_id = regSearchString(response.text, '"id":(.+?)}', 5, -1)
        log.info("正则--获取 plan_id:  " + plan_id)
        log.info(response.text)
        self.assertTrue(assertsResponse(asserts, response.text), "断言失败")
        log.info("--------------------" + caseName + "------------------测试完毕")
        time.sleep(10)


    def test004_get_all_ads_plan(self):
        '''获取所有投放计划--验证成功创建投放计划'''
        global access_token
        global base_url
        global caseName
        global plan_id
        caseName = "4 获取所有投放计划--验证成功创建投放计划"
        log.info("--------------------" + caseName + "------------------开始测试")
        headers = {'Accept': 'application/json', 'Authorization': 'Bearer  ' + access_token}
        log.info("headers--------------------" + str(headers))
        parameters = "/api/v2/ads-op/v3/plan"
        asserts = ['"name":"test00001"',plan_id]
        url = base_url + parameters
        response = TestMethod.getMethod(self, url,  headers)
        log.info(response.text)
        self.assertTrue(assertsResponse(asserts, response.text),"断言失败")
        log.info("--------------------" + caseName + "------------------测试完毕")
        time.sleep(1)


    def test005_add_new_ads_plan(self):
        '''新增投放计划：时间冲突'''
        global access_token
        global base_url
        global caseName
        caseName = "5 新增投放计划：时间冲突"
        log.info("--------------------" + caseName + "------------------开始测试")
        headers = {'Accept': 'application/json', 'Accept-Encoding':'gzip, deflate, br',
                    'Content-Type':'application/json; charset=utf-8','Authorization': 'Bearer  ' + access_token}
        log.info("headers--------------------" + str(headers))
        parameters = "/api/v2/ads-op/v3/plan"
        asserts = ['"success":false,','"code":"1999",','"message":"系统错误",','"data":"所选公交列表中的车部分已经有该时段的计划",']
        url = base_url + parameters
        bodyData = {
                        "name":"test00002",
                        "busIds":[
                            15
                        ],
                        "startTime":1625147576097,
                        "endTime":1625233976097
                    }
        response = TestMethod.postMethod(self, url, bodyData,  headers)
        log.info(response.text)
        self.assertTrue(assertsResponse(asserts, response.text), "断言失败")
        log.info("--------------------" + caseName + "------------------测试完毕")
        time.sleep(1)


    def test006_edit_ads_plan(self):
        '''编辑投放计划'''
        global access_token
        global base_url
        global caseName
        global plan_id
        caseName = "6 编辑投放计划"
        log.info("--------------------" + caseName + "------------------开始测试")
        headers = {'Accept': 'application/json', 'Accept-Encoding':'gzip, deflate, br',
                   'Content-Type':'application/json; charset=utf-8','Authorization': 'Bearer  ' + access_token}
        log.info("headers--------------------" + str(headers))
        parameters = "/api/v2/ads-op/v3/plan/{plan_id}".format(plan_id=plan_id)
        asserts = ['"success":true,','"reason":"Update Success",',plan_id]
        url = base_url + parameters
        bodyData = {
                        "planId":plan_id,
                        "name":"test00001_update",
                        "busNames":[
                            {
                                "busId":15,
                                "busName":"tntest"
                            }
                        ],
                        "positionNames":'null',
                        "startTime":1627741854000,
                        "endTime":1630420254000,
                        "updateTime":1560263512000,
                        "materialCount":'null',
                        "exposeCount":'null',
                        "viewCount":'null',
                        "status":"0",
                        "materials":'null',
                        "id":plan_id,
                        "busIds":[
                            15
                        ]
                    }
        response = TestMethod.putMethod(self, url, bodyData,  headers)
        log.info(response.text)
        self.assertTrue(assertsResponse(asserts, response.text),"断言失败")
        log.info("--------------------" + caseName + "------------------测试完毕")
        time.sleep(1)



    def test007_get_ads_plan_info(self):
        '''获取投放计划详情--验证成功编辑'''
        global access_token
        global base_url
        global caseName
        caseName = "7 获取投放计划详情--验证成功编辑"
        log.info("--------------------" + caseName + "------------------开始测试")
        headers = {'Accept': 'application/json', 'Authorization': 'Bearer  ' + access_token}
        log.info("headers--------------------" + str(headers))
        parameters = "/api/v2/ads-op/v3/plan/{plan_id}".format(plan_id=plan_id)
        asserts = ['"positionNames":null','"materialCount":null','"materials":null','"name":"test00001_update"']
        url = base_url + parameters
        response = TestMethod.getMethod(self, url,  headers)
        log.info(response.text)
        self.assertTrue(assertsResponse(asserts, response.text),"断言失败")
        log.info("--------------------" + caseName + "------------------测试完毕")
        time.sleep(1)


    def test008_get_material_filekey(self):
        '''获取素材filekey'''
        global access_token
        global base_url
        global caseName
        global filekey
        global uploadToken
        caseName = "8 获取素材filekey"
        log.info("--------------------" + caseName + "------------------开始测试")
        headers = {'Accept': 'application/json', 'Authorization': 'Bearer  ' + access_token}
        log.info("headers--------------------" + str(headers))
        parameters = "/api/v2/op/up/token?fileName=dududu.mp4"
        asserts = ['"success":true,','"filekey":"','"uploadToken":"','"accessURL":"']
        url = base_url + parameters
        response = TestMethod.getMethod(self, url,  headers)
        log.info(response.text)
        # "filekey":"3cdd8157-093e-41fd-8e13-310a82eea511.mp4",
        filekey = regSearchString(response.text, '"filekey":"(.+?)",', 11, -2)
        log.info("正则--获取 filekey:  " + filekey)
        # "uploadToken":"6IRM4w7Yyl4RfC7l2gPhTd7NbHjD00i3Z4_1
        uploadToken = regSearchString(response.text, '"uploadToken":"(.+?)",', 15, -2)
        log.info("正则--获取 uploadToken:  " + uploadToken)
        self.assertTrue(assertsResponse(asserts, response.text),"断言失败")
        log.info("--------------------" + caseName + "------------------测试完毕")
        time.sleep(1)


    def test009_upload_material(self):
        '''上传素材'''
        global access_token
        global base_url
        global caseName
        global filekey
        global material_id
        caseName = "9 上传素材"
        log.info("--------------------" + caseName + "------------------开始测试")
        headers = {'Accept': 'application/json', 'Accept-Encoding':'gzip, deflate, br',
                   'Content-Type':'application/json; charset=utf-8','Authorization': 'Bearer  ' + access_token}
        log.info("headers--------------------" + str(headers))
        parameters = "/api/v2/ads-op/v3/material"
        asserts = ['"name":"create_materials_test00001"']
        url = base_url + parameters
        bodyData = {
                        "materialName":"create_materials_test00001",
                        "positionId":7,
                        "imageUrl":"",
                        "sexTags":[
                            {
                                "tagId":"MALE",
                                "tagName":"男"
                            },
                            {
                                "tagId":"FEMALE",
                                "tagName":"女"
                            }
                        ],
                        "ageTags":[
                            {
                                "tagId":"BABY",
                                "tagName":"幼年"
                            },
                            {
                                "tagId":"YOUNG",
                                "tagName":"少年"
                            },
                            {
                                "tagId":"MATURE",
                                "tagName":"青年"
                            },
                            {
                                "tagId":"MIDLIFE",
                                "tagName":"中年"
                            },
                            {
                                "tagId":"OLD",
                                "tagName":"老年"
                            }
                        ],
                        "materialUrl":"https://media.quixmart.com/{filekey}".format(filekey=filekey),
                        "materialPreview":"https://media.quixmart.com/{filekey}".format(filekey=filekey),
                        "formatCode":"mp4",
                        "positionName":"熊猫公交19寸广告屏"
                    }
        response = TestMethod.postMethod(self, url, bodyData,  headers)
        log.info(response.text)
        # {"id":63,"name":"create_materials_test00001"}
        material_id = regSearchString(response.text, '"id":(.+?),', 5, -1)
        log.info("正则--获取 material_id:  " + material_id)
        self.assertTrue(assertsResponse(asserts, response.text),"断言失败")
        log.info("--------------------" + caseName + "------------------测试完毕")
        time.sleep(10)



    def test010_get_material_list(self):
        '''获取素材列表'''
        global access_token
        global base_url
        global caseName
        global material_id
        caseName = "10 获取素材列表"
        log.info("--------------------" + caseName + "------------------开始测试")
        headers = {'Accept': 'application/json', 'Authorization': 'Bearer  ' + access_token}
        log.info("headers--------------------" + str(headers))
        parameters = "/api/v2/ads-op/v3/material?pageSize=8&pageNum=1"
        asserts = ['"success":true,','"materialName":"create_materials_test00001"','"positionId":7,',
                   '"positionName":"熊猫公交19寸广告屏"',material_id]
        url = base_url + parameters
        response = TestMethod.getMethod(self, url,  headers)
        log.info(response.text)
        self.assertTrue(assertsResponse(asserts, response.text),"断言失败")
        log.info("--------------------" + caseName + "------------------测试完毕")
        time.sleep(1)


    def test011_add_material(self):
        '''添加素材'''
        global access_token
        global base_url
        global caseName
        global plan_id
        global material_id
        caseName = "11 添加素材"
        log.info("--------------------" + caseName + "------------------开始测试")
        headers = {'Accept': 'application/json', 'Accept-Encoding':'gzip, deflate, br',
                   'Content-Type':'application/json; charset=utf-8','Authorization': 'Bearer  ' + access_token}
        log.info("headers--------------------" + str(headers))
        parameters = "/api/v2/ads-op/v3/plan/{plan_id}/materials-add".format(plan_id=plan_id)
        asserts = ['"success":true,', '"reason":"Append success",',
                   '"positionName":"熊猫公交19寸广告屏"', material_id]
        url = base_url + parameters
        bodyData = {"toAppend":[material_id]}
        response = TestMethod.putMethod(self, url, bodyData, headers)
        log.info(response.text)
        self.assertTrue(assertsResponse(asserts, response.text), "断言失败")
        log.info("--------------------" + caseName + "------------------测试完毕")
        time.sleep(1)


    def test012_get_ads_plan_info(self):
        '''获取投放计划详情'''
        global access_token
        global base_url
        global caseName
        global plan_id
        caseName = "12 获取投放计划详情"
        log.info("--------------------" + caseName + "------------------开始测试")
        headers = {'Accept': 'application/json', 'Authorization': 'Bearer  ' + access_token}
        log.info("headers--------------------" + str(headers))
        parameters = "/api/v2/ads-op/v3/plan/{plan_id}".format(plan_id=plan_id)
        asserts = ['"name":"test00001_update",','"materialName":"create_materials_test00001"','"positionId":7,',
                   '"positionName":"熊猫公交19寸广告屏"']
        url = base_url + parameters
        response = TestMethod.getMethod(self, url,  headers)
        log.info(response.text)
        self.assertTrue(assertsResponse(asserts, response.text),"断言失败")
        log.info("--------------------" + caseName + "------------------测试完毕")
        time.sleep(1)


    def test013_start_ads_plan(self):
        '''启动投放计划'''
        global access_token
        global base_url
        global caseName
        global plan_id
        caseName = "13 启动投放计划"
        log.info("--------------------" + caseName + "------------------开始测试")
        headers = {'Accept': 'application/json', 'Accept-Encoding':'gzip, deflate, br',
                   'Content-Type':'application/json; charset=utf-8','Authorization': 'Bearer  ' + access_token}
        log.info("headers--------------------" + str(headers))
        parameters = "/api/v2/ads-op/v3/plan/{plan_id}/status?toStatus=1".format(plan_id=plan_id)
        asserts = ['"result":"success",','"code":0,','"remark":"success"']
        url = base_url + parameters
        response = TestMethod.putmethod(self, url,  headers)
        log.info(response.text)
        self.assertTrue(assertsResponse(asserts, response.text),"断言失败")
        log.info("--------------------" + caseName + "------------------测试完毕")
        time.sleep(1)


    def test014_get_ads_plan_info(self):
        '''获取投放计划详情：验证成功启动投放计划'''
        global access_token
        global base_url
        global caseName
        global plan_id
        caseName = "14 获取投放计划详情：验证成功启动投放计划"
        log.info("--------------------" + caseName + "------------------开始测试")
        headers = {'Accept': 'application/json', 'Authorization': 'Bearer  ' + access_token}
        log.info("headers--------------------" + str(headers))
        parameters = "/api/v2/ads-op/v3/plan/{plan_id}".format(plan_id=plan_id)
        asserts = [plan_id,'"status":"1",']
        url = base_url + parameters
        response = TestMethod.getMethod(self, url,  headers)
        log.info(response.text)
        self.assertTrue(assertsResponse(asserts, response.text),"断言失败")
        log.info("--------------------" + caseName + "------------------测试完毕")
        time.sleep(1)



    def test015_delete_new_ads_plan(self):
        '''删除创建的投放计划：无法删除正在投放的计划'''
        global access_token
        global base_url
        global caseName
        global plan_id
        caseName = "15 删除创建的投放计划：无法删除正在投放的计划"
        log.info("--------------------" + caseName + "------------------开始测试")
        headers = {'Accept': 'application/json', 'Accept-Encoding':'gzip, deflate, br',
                   'Content-Type':'application/json; charset=utf-8','Authorization': 'Bearer  ' + access_token}
        log.info("headers--------------------" + str(headers))
        parameters = "/api/v2/ads-op/v3/plan/{plan_id}".format(plan_id=plan_id)
        asserts = ['"success":false,','"code":"1999",','"message":"系统错误",','"data":"不支持直接删除状态为投放中的计划",']
        url = base_url + parameters
        response = TestMethod.deleteMethod(self, url,  headers)
        log.info(response.text)
        self.assertTrue(assertsResponse(asserts, response.text),"断言失败")
        log.info("--------------------" + caseName + "------------------测试完毕")
        time.sleep(1)


    def test016_stop_ads_plan(self):
        '''暂停投放计划'''
        global access_token
        global base_url
        global caseName
        global plan_id
        caseName = "16 暂停投放计划"
        log.info("--------------------" + caseName + "------------------开始测试")
        headers = {'Accept': 'application/json', 'Accept-Encoding':'gzip, deflate, br',
                   'Content-Type':'application/json; charset=utf-8','Authorization': 'Bearer  ' + access_token}
        log.info("headers--------------------" + str(headers))
        parameters = "/api/v2/ads-op/v3/plan/{plan_id}/status?toStatus=0".format(plan_id=plan_id)
        asserts = ['"result":"success",','"code":0,','"remark":"success"']
        url = base_url + parameters
        response = TestMethod.putmethod(self, url,  headers)
        log.info(response.text)
        self.assertTrue(assertsResponse(asserts, response.text),"断言失败")
        log.info("--------------------" + caseName + "------------------测试完毕")
        time.sleep(1)


    def test017_get_ads_plan_info(self):
        '''获取投放计划详情：验证成功暂停投放计划'''
        global access_token
        global base_url
        global caseName
        global plan_id
        caseName = "17 获取投放计划详情：验证成功暂停投放计划"
        log.info("--------------------" + caseName + "------------------开始测试")
        headers = {'Accept': 'application/json', 'Authorization': 'Bearer  ' + access_token}
        log.info("headers--------------------" + str(headers))
        parameters = "/api/v2/ads-op/v3/plan/{plan_id}".format(plan_id=plan_id)
        asserts = [plan_id,'"status":"0",']
        url = base_url + parameters
        response = TestMethod.getMethod(self, url,  headers)
        log.info(response.text)
        self.assertTrue(assertsResponse(asserts, response.text),"断言失败")
        log.info("--------------------" + caseName + "------------------测试完毕")
        time.sleep(1)


    def test018_delete_new_material(self):
        '''删除刚刚添加的素材'''
        global access_token
        global base_url
        global caseName
        global plan_id
        global material_id
        caseName = "18 删除刚刚添加的素材"
        log.info("--------------------" + caseName + "------------------开始测试")
        headers = {'Accept': 'application/json', 'Accept-Encoding':'gzip, deflate, br',
                   'Content-Type':'application/json; charset=utf-8','Authorization': 'Bearer  ' + access_token}
        log.info("headers--------------------" + str(headers))
        parameters = "/api/v2/ads-op/v3/plan/{plan_id}/materials-del".format(plan_id=plan_id)
        asserts = ['"success":true,','"reason":"Remove Ads Item from Plan success",',plan_id]
        url = base_url + parameters
        bodyData = {"toRemove":[material_id]}
        response = TestMethod.putMethod(self, url, bodyData,  headers)
        log.info(response.text)
        self.assertTrue(assertsResponse(asserts, response.text),"断言失败")
        log.info("--------------------" + caseName + "------------------测试完毕")
        time.sleep(1)


    def test019_get_ads_plan_info(self):
        '''获取投放计划详情：验证成功删除视频'''
        global access_token
        global base_url
        global caseName
        global plan_id
        caseName = "19 获取投放计划详情：验证成功删除视频"
        log.info("--------------------" + caseName + "------------------开始测试")
        headers = {'Accept': 'application/json', 'Authorization': 'Bearer  ' + access_token}
        log.info("headers--------------------" + str(headers))
        parameters = "/api/v2/ads-op/v3/plan/{plan_id}".format(plan_id=plan_id)
        asserts = ['"materialName":"create_materials_test00001"']
        url = base_url + parameters
        response = TestMethod.getMethod(self, url,  headers)
        log.info(response.text)
        self.assertTrue(assertsNotinResponse(asserts, response.text),"断言失败")
        log.info("--------------------" + caseName + "------------------测试完毕")
        time.sleep(1)


    def test020_delete_new_material(self):
        '''素材库里面删除刚刚创建的素材'''
        global access_token
        global base_url
        global caseName
        global material_id
        caseName = "20 素材库里面删除刚刚创建的素材"
        log.info("--------------------" + caseName + "------------------开始测试")
        headers = {'Accept': 'application/json', 'Accept-Encoding':'gzip, deflate, br',
                   'Content-Type':'application/json; charset=utf-8','Authorization': 'Bearer  ' + access_token}
        log.info("headers--------------------" + str(headers))
        parameters = "/api/v2/ads-op/v3/material/{material_id}".format(material_id=material_id)
        asserts = ['"result":true,','"remark":"Delete Success"']
        url = base_url + parameters
        response = TestMethod.deleteMethod(self, url,  headers)
        log.info(response.text)
        self.assertTrue(assertsResponse(asserts, response.text),"断言失败")
        log.info("--------------------" + caseName + "------------------测试完毕")
        time.sleep(1)



    def test021_get_material_list(self):
        '''获取素材列表--验证成功删除素材'''
        global access_token
        global base_url
        global caseName
        global material_id
        caseName = "21 获取素材列表--验证成功删除素材"
        log.info("--------------------" + caseName + "------------------开始测试")
        headers = {'Accept': 'application/json', 'Authorization': 'Bearer  ' + access_token}
        log.info("headers--------------------" + str(headers))
        parameters = "/api/v2/ads-op/v3/material?pageSize=8&pageNum=1"
        asserts = ['"materialName":"create_materials_test00001"','"materialId":{material_id},'.format(material_id=material_id)]
        url = base_url + parameters
        response = TestMethod.getMethod(self, url,  headers)
        log.info(response.text)
        self.assertTrue(assertsNotinResponse(asserts, response.text),"断言失败")
        log.info("--------------------" + caseName + "------------------测试完毕")
        time.sleep(1)


    def test022_delete_new_ads_plan(self):
        '''删除创建的投放计划'''
        global access_token
        global base_url
        global caseName
        global plan_id
        caseName = "22 删除创建的投放计划"
        log.info("--------------------" + caseName + "------------------开始测试")
        headers = {'Accept': 'application/json', 'Accept-Encoding':'gzip, deflate, br',
                   'Content-Type':'application/json; charset=utf-8','Authorization': 'Bearer  ' + access_token}
        log.info("headers--------------------" + str(headers))
        parameters = "/api/v2/ads-op/v3/plan/{plan_id}".format(plan_id=plan_id)
        asserts = ['"success":true,','"reason":"Delete Success"',plan_id]
        url = base_url + parameters
        response = TestMethod.deleteMethod(self, url,  headers)
        log.info(response.text)
        self.assertTrue(assertsResponse(asserts, response.text),"断言失败")
        log.info("--------------------" + caseName + "------------------测试完毕")
        time.sleep(1)


    def test023_get_all_ads_plan(self):
        '''获取所有投放计划--验证成功删除投放计划'''
        global access_token
        global base_url
        global caseName
        global plan_id
        caseName = "23 获取所有投放计划--验证成功删除投放计划"
        log.info("--------------------" + caseName + "------------------开始测试")
        headers = {'Accept': 'application/json', 'Authorization': 'Bearer  ' + access_token}
        log.info("headers--------------------" + str(headers))
        parameters = "/api/v2/ads-op/v3/plan"
        asserts = ['"name":"test00001"',plan_id]
        url = base_url + parameters
        response = TestMethod.getMethod(self, url,  headers)
        log.info(response.text)
        self.assertTrue(assertsNotinResponse(asserts, response.text),"断言失败")
        log.info("--------------------" + caseName + "------------------测试完毕")
        time.sleep(1)


















































