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
    global filekey
    global uploadToken
    global accessURL
    global model_id
    global filekey1
    global uploadToken1
    global accessURL1
    global video_id

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


    def test002_get_modules_name(self):
        '''获取所有模块名称'''
        global access_token
        global base_url
        global caseName
        caseName = "2 获取所有模块名称"
        log.info("--------------------" + caseName + "------------------开始测试")
        headers = {'Accept': 'application/json', 'Authorization': 'Bearer  ' + access_token}
        log.info("headers--------------------" + str(headers))
        parameters = "/api/v2/ads-op/module-video-summary?pageNum=1&pageSize=10"
        asserts = ["\"success\":true"]
        url = base_url + parameters
        response = TestMethod.getMethod(self, url,  headers)
        log.info(response.text)
        self.assertTrue(assertsResponse(asserts, response.text),"断言失败")
        log.info("--------------------" + caseName + "------------------测试完毕")
        time.sleep(1)


    def test003_get_filekey_uploadToken(self):
        '''获取filekey和uploadToken和accessURL'''
        global access_token
        global base_url
        global caseName
        global filekey
        global uploadToken
        global accessURL
        caseName = "3 获取filekey和uploadToken和accessURL"
        log.info("--------------------" + caseName + "------------------开始测试")
        headers = {'Accept': 'application/json', 'Authorization': 'Bearer  ' + access_token}
        log.info("headers--------------------" + str(headers))
        parameters = "/api/v2/op/up/token?fileName=熊猫公交图片.jpg"
        asserts = ["\"success\":true",'"filekey":"','"uploadToken":"','"accessURL":"']
        url = base_url + parameters
        response = TestMethod.getMethod(self, url,  headers)
        # "filekey":"3cdd8157-093e-41fd-8e13-310a82eea511.mp4",
        filekey = regSearchString(response.text, '"filekey":"(.+?)",', 11, -2)
        log.info("正则--获取filekey:  " + filekey)
        # "uploadToken":"6IRM4w7Yyl4RfC7l2gPhTd7NbHjD00i3Z4_1wKjT:vOmD4Af-
        uploadToken = regSearchString(response.text, '"uploadToken":"(.+?)",', 15, -2)
        log.info("正则--获取uploadToken:  " + uploadToken)
        # "accessURL":"https://media.quixmart.com/03a4b820-7c12-4b18-b96e-7b3c7897f533.jpg"
        accessURL = regSearchString(response.text, '"accessURL":"(.+?)"},', 13, -3)
        log.info("正则--获取accessURL:  " + accessURL)
        log.info(response.text)
        self.assertTrue(assertsResponse(asserts, response.text), "断言失败")
        log.info("--------------------" + caseName + "------------------测试完毕")
        time.sleep(1)


    def test004_add_new_module(self):
        '''新增影音模块'''
        global access_token
        global base_url
        global caseName
        global accessURL
        caseName = "4 新增影音模块"
        log.info("--------------------" + caseName + "------------------开始测试")
        headers = {'Accept': 'application/json', 'Accept-Encoding':'gzip, deflate, br',
                   'Content-Type':'application/json; charset=utf-8','Authorization': 'Bearer  ' + access_token}
        log.info("headers--------------------" + str(headers))
        parameters = "/api/v2/ads-op/module-video-summary"
        asserts = ["\"success\":true"]
        url = base_url + parameters
        bodyData = {
                        "name":"modelTest00001",
                        "weight":"2",
                        "imageUrl":accessURL,
                        "remark":"model_discription_modelTest00001"
                    }
        response = TestMethod.putMethod(self, url, bodyData,  headers)
        log.info(response.text)
        self.assertTrue(assertsResponse(asserts, response.text),"断言失败")
        log.info("--------------------" + caseName + "------------------测试完毕")
        time.sleep(1)


    def test005_get_modules_name(self):
        '''获取所有模块名称获取model_id'''
        global access_token
        global base_url
        global caseName
        global accessURL
        global model_id
        caseName = "5 获取所有模块名称获取model_id"
        log.info("--------------------" + caseName + "------------------开始测试")
        headers = {'Accept': 'application/json', 'Authorization': 'Bearer  ' + access_token}
        log.info("headers--------------------" + str(headers))
        parameters = "/api/v2/ads-op/module-video-summary?pageNum=1&pageSize=10"
        asserts = ["\"success\":true",'"name":"modelTest00001",','"remark":"model_discription_modelTest00001"',accessURL]
        url = base_url + parameters
        response = TestMethod.getMethod(self, url,  headers)
        # "id":222,"name":"modelTest00001"
        model_id = regSearchString(response.text, '"id":(.+?),"name":"modelTest00001"', 5, -24)
        log.info("正则--获取 model_id:  " + model_id)
        log.info(response.text)
        self.assertTrue(assertsResponse(asserts, response.text),"断言失败")
        log.info("--------------------" + caseName + "------------------测试完毕")
        time.sleep(1)



    def test006_edit_module(self):
        '''编辑影音模块'''
        global access_token
        global base_url
        global caseName
        global model_id
        caseName = "6 编辑影音模块"
        log.info("--------------------" + caseName + "------------------开始测试")
        headers = {'Accept': 'application/json', 'Accept-Encoding':'gzip, deflate, br',
                   'Content-Type':'application/json; charset=utf-8','Authorization': 'Bearer  ' + access_token}
        log.info("headers--------------------" + str(headers))
        parameters = "/api/v2/ads-op/module-video-summary"
        asserts = ["\"success\":true"]
        url = base_url + parameters
        bodyData = {
                        "id":model_id,
                        "name":"modelTest00001_update",
                        "order":1,
                        "weight":"1",
                        "imageUrl":"${accessURL}",
                        "videoCount":0,
                        "remark":"model_discription_modelTest00001"
                    }
        response = TestMethod.postMethod(self, url, bodyData,  headers)
        log.info(response.text)
        self.assertTrue(assertsResponse(asserts, response.text),"断言失败")
        log.info("--------------------" + caseName + "------------------测试完毕")
        time.sleep(1)



    def test007_get_modules_name(self):
        '''获取所有模块：验证编辑成功'''
        global access_token
        global base_url
        global caseName
        caseName = "7 获取所有模块：验证编辑成功"
        log.info("--------------------" + caseName + "------------------开始测试")
        headers = {'Accept': 'application/json', 'Authorization': 'Bearer  ' + access_token}
        log.info("headers--------------------" + str(headers))
        parameters = "/api/v2/ads-op/module-video-summary?pageNum=1&pageSize=10"
        asserts = ["\"success\":true",'"name":"modelTest00001_update",']
        url = base_url + parameters
        response = TestMethod.getMethod(self, url,  headers)
        log.info(response.text)
        self.assertTrue(assertsResponse(asserts, response.text),"断言失败")
        log.info("--------------------" + caseName + "------------------测试完毕")
        time.sleep(1)


    def test008_get_modules_info(self):
        '''查看创建的模块详情'''
        global access_token
        global base_url
        global caseName
        global model_id
        caseName = "8 查看创建的模块详情"
        log.info("--------------------" + caseName + "------------------开始测试")
        headers = {'Accept': 'application/json', 'Authorization': 'Bearer  ' + access_token}
        log.info("headers--------------------" + str(headers))
        parameters = "/api/v2/ads-op/module-video-detail?pageNum=1&pageSize=10&moduleId={model_id}".format(model_id=model_id)
        asserts = ["\"success\":true"]
        url = base_url + parameters
        response = TestMethod.getMethod(self, url,  headers)
        log.info(response.text)
        self.assertTrue(assertsResponse(asserts, response.text),"断言失败")
        log.info("--------------------" + caseName + "------------------测试完毕")
        time.sleep(1)


    def test009_get_filekey_uploadToken(self):
        '''获取filekey和uploadToken和accessURL'''
        global access_token
        global base_url
        global caseName
        global filekey1
        global uploadToken1
        global accessURL1
        caseName = "9 获取filekey和uploadToken和accessURL"
        log.info("--------------------" + caseName + "------------------开始测试")
        headers = {'Accept': 'application/json', 'Authorization': 'Bearer  ' + access_token}
        log.info("headers--------------------" + str(headers))
        parameters = "/api/v2/op/up/token?fileName=熊猫公交图片.jpg"
        asserts = ["\"success\":true",'"filekey":"','"uploadToken":"','"accessURL":"']
        url = base_url + parameters
        response = TestMethod.getMethod(self, url,  headers)
        # "filekey":"3cdd8157-093e-41fd-8e13-310a82eea511.mp4",
        filekey1 = regSearchString(response.text, '"filekey":"(.+?)",', 11, -2)
        log.info("正则--获取filekey1:  " + filekey1)
        # "uploadToken":"6IRM4w7Yyl4RfC7l2gPhTd7NbHjD00i3Z4_1wKjT:vOmD4Af-
        uploadToken1 = regSearchString(response.text, '"uploadToken":"(.+?)",', 15, -2)
        log.info("正则--获取 uploadToken1:  " + uploadToken1)
        # "accessURL":"https://media.quixmart.com/03a4b820-7c12-4b18-b96e-7b3c7897f533.jpg"
        accessURL1 = regSearchString(response.text, '"accessURL":"(.+?)"},', 13, -3)
        log.info("正则--获取 accessURL1:  " + accessURL1)
        log.info(response.text)
        self.assertTrue(assertsResponse(asserts, response.text), "断言失败")
        log.info("--------------------" + caseName + "------------------测试完毕")
        time.sleep(1)



    def test010_upload_video(self):
        '''上传视频'''
        global access_token
        global base_url
        global caseName
        global model_id
        global accessURL1
        caseName = "10 上传视频"
        log.info("--------------------" + caseName + "------------------开始测试")
        headers = {'Accept': 'application/json', 'Accept-Encoding':'gzip, deflate, br',
                   'Content-Type':'application/json; charset=utf-8','Authorization': 'Bearer  ' + access_token}
        log.info("headers--------------------" + str(headers))
        parameters = "/api/v2/ads-op/module-video-detail"
        asserts = ["\"success\":true"]
        url = base_url + parameters
        bodyData = {
                        "name":"test_video_00001",
                        "weight":"2",
                        "imageUrl":accessURL1,
                        "videoUrl":accessURL1,
                        "videoFormat":"mp4",
                        "moduleId":model_id
                    }
        response = TestMethod.putMethod(self, url, bodyData,  headers)
        log.info(response.text)
        self.assertTrue(assertsResponse(asserts, response.text),"断言失败")
        log.info("--------------------" + caseName + "------------------测试完毕")
        time.sleep(1)


    def test011_check_video_in_modules(self):
        '''查询模块里面的视频：验证是否成功上传视频'''
        global access_token
        global base_url
        global caseName
        global model_id
        global accessURL1
        global video_id
        caseName = "11 查询模块里面的视频：验证是否成功上传视频"
        log.info("--------------------" + caseName + "------------------开始测试")
        headers = {'Accept': 'application/json', 'Authorization': 'Bearer  ' + access_token}
        log.info("headers--------------------" + str(headers))
        parameters = "/api/v2/ads-op/module-video-detail?pageNum=1&pageSize=10&moduleId={model_id}".format(model_id=model_id)
        asserts = ["\"success\":true",'"name":"test_video_00001",','"videoFormat":"mp4",',accessURL1]
        url = base_url + parameters
        response = TestMethod.getMethod(self, url,  headers)
        # "id":395,"name":"test_video_00001"
        video_id = regSearchString(response.text, '"id":(.+?),"name":"test_video_00001"', 5, -26)
        log.info("正则--获取 video_id:  " + video_id)
        log.info(response.text)
        self.assertTrue(assertsResponse(asserts, response.text),"断言失败")
        log.info("--------------------" + caseName + "------------------测试完毕")
        time.sleep(1)


    def test012_edit_video_info(self):
        '''编辑视频信息'''
        global access_token
        global base_url
        global caseName
        global video_id
        global accessURL1
        caseName = "12 编辑视频信息"
        log.info("--------------------" + caseName + "------------------开始测试")
        headers = {'Accept': 'application/json', 'Accept-Encoding':'gzip, deflate, br',
                   'Content-Type':'application/json; charset=utf-8','Authorization': 'Bearer  ' + access_token}
        log.info("headers--------------------" + str(headers))
        parameters = "/api/v2/ads-op/module-video-detail"
        asserts = ["\"success\":true"]
        url = base_url + parameters
        bodyData = {
                        "id":video_id,
                        "name":"test_video_00001_update",
                        "order":1,
                        "weight":"3",
                        "imageUrl":accessURL1,
                        "videoUrl":accessURL1,
                        "videoLength":"null",
                        "videoFormat":"mp4",
                        "exposureCount":0
                    }
        response = TestMethod.postMethod(self, url, bodyData,  headers)
        log.info(response.text)
        self.assertTrue(assertsResponse(asserts, response.text),"断言失败")
        log.info("--------------------" + caseName + "------------------测试完毕")
        time.sleep(1)


    def test013_check_video_in_modules(self):
        '''查询模块里面的视频：验证是否成功编辑视频'''
        global access_token
        global base_url
        global caseName
        global model_id
        global accessURL1
        caseName = "13 查询模块里面的视频：验证是否成功上传视频"
        log.info("--------------------" + caseName + "------------------开始测试")
        headers = {'Accept': 'application/json', 'Authorization': 'Bearer  ' + access_token}
        log.info("headers--------------------" + str(headers))
        parameters = "/api/v2/ads-op/module-video-detail?pageNum=1&pageSize=10&moduleId={model_id}".format(model_id=model_id)
        asserts = ["\"success\":true",'"name":"test_video_00001_update",','"videoFormat":"mp4",',accessURL1]
        url = base_url + parameters
        response = TestMethod.getMethod(self, url,  headers)
        log.info(response.text)
        self.assertTrue(assertsResponse(asserts, response.text),"断言失败")
        log.info("--------------------" + caseName + "------------------测试完毕")
        time.sleep(1)


    def test014_delete_video(self):
        '''删除视频'''
        global access_token
        global base_url
        global caseName
        global video_id
        caseName = "14 删除视频"
        log.info("--------------------" + caseName + "------------------开始测试")
        headers = {'Accept': 'application/json', 'Accept-Encoding':'gzip, deflate, br',
                   'Content-Type':'application/json; charset=utf-8','Authorization': 'Bearer  ' + access_token}
        log.info("headers--------------------" + str(headers))
        parameters = "/api/v2/ads-op/module-video-detail"
        asserts = ["\"success\":true"]
        url = base_url + parameters
        bodyData = {"id":video_id}
        response = TestMethod.deletesMethod(self, url, bodyData,  headers)
        log.info(response.text)
        self.assertTrue(assertsResponse(asserts, response.text),"断言失败")
        log.info("--------------------" + caseName + "------------------测试完毕")
        time.sleep(1)


    def test015_check_video_in_modules(self):
        '''查询模块里面的视频：验证是否成功删除视频'''
        global access_token
        global base_url
        global caseName
        global model_id
        global accessURL1
        caseName = "15 查询模块里面的视频：验证是否成功删除视频"
        log.info("--------------------" + caseName + "------------------开始测试")
        headers = {'Accept': 'application/json', 'Authorization': 'Bearer  ' + access_token}
        log.info("headers--------------------" + str(headers))
        parameters = "/api/v2/ads-op/module-video-detail?pageNum=1&pageSize=10&moduleId={model_id}".format(model_id=model_id)
        asserts = ['"name":"test_video_00001_update",',accessURL1]
        url = base_url + parameters
        response = TestMethod.getMethod(self, url,  headers)
        log.info(response.text)
        self.assertTrue(assertsNotinResponse(asserts, response.text),"断言失败")
        log.info("--------------------" + caseName + "------------------测试完毕")
        time.sleep(1)


    def test016_delete_module(self):
        '''删除模块'''
        global access_token
        global base_url
        global caseName
        global model_id
        caseName = "16 删除模块"
        log.info("--------------------" + caseName + "------------------开始测试")
        headers = {'Accept': 'application/json', 'Accept-Encoding':'gzip, deflate, br',
                   'Content-Type':'application/json; charset=utf-8','Authorization': 'Bearer  ' + access_token}
        log.info("headers--------------------" + str(headers))
        parameters = "/api/v2/ads-op/module-video-summary"
        asserts = ["\"success\":true"]
        url = base_url + parameters
        bodyData = {"id":model_id}
        response = TestMethod.deletesMethod(self, url, bodyData,  headers)
        log.info(response.text)
        self.assertTrue(assertsResponse(asserts, response.text),"断言失败")
        log.info("--------------------" + caseName + "------------------测试完毕")
        time.sleep(1)


    def test017_check_modules(self):
        '''获取所有模块：验证编辑删除模块'''
        global access_token
        global base_url
        global caseName
        caseName = "17 获取所有模块：验证编辑删除模块"
        log.info("--------------------" + caseName + "------------------开始测试")
        headers = {'Accept': 'application/json', 'Authorization': 'Bearer  ' + access_token}
        log.info("headers--------------------" + str(headers))
        parameters = "/api/v2/ads-op/module-video-summary?pageNum=1&pageSize=10"
        asserts = ['"name":"modelTest00001_update",']
        url = base_url + parameters
        response = TestMethod.getMethod(self, url,  headers)
        log.info(response.text)
        self.assertTrue(assertsNotinResponse(asserts, response.text),"断言失败")
        log.info("--------------------" + caseName + "------------------测试完毕")
        time.sleep(1)

































































