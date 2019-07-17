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

class testpandabusAPI(unittest.TestCase):
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
    global vihicle_id

    def setUp(self):
        log.info("-------------------------测试用例开始执行--------------------------")
        global base_url
        base_url = "https://test-vms-panda.deepblueai.com"
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


