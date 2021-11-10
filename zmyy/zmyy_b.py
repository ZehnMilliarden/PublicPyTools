
#coding=utf-8

import sys
import requests
import time
import random
import configparser
import os

sys.path.append('..')
import utils.captcha.SlideCrack

class czmyy_test:

    def __init_config__(self):
        proDir = os.path.split(os.path.realpath(__file__))[0]
        # 在当前文件路径下查找.ini文件
        configPath = os.path.join(proDir, "config.ini")
        self.conf = configparser.ConfigParser()
        self.conf.read(configPath, encoding='utf-8-sig')
        self.confzmyy = self.conf['zmyy']

    # 关键敏感信息本地配置
    def __init_var__(self):
        # 延迟时间
        self.delaytime = 4
        #
        self.Checks = True
        # 猜测验证码的X坐标？
        self.xsite = 0
        # 验证码的有坐标
        self.ysite = 1
        # url
        self.url = 'https://cloud.cn2030.com/sc/wx/HandlerSubscribe.ashx'
        # Cookies
        self.yi_cookies = self.confzmyy.get('cookies')
        # 请求头
        self.headers = {
            'charset': 'utf-8',
            'Accept-Encoding': 'gzip, deflate, br',
            'referer': 'https://servicewechat.com/wx2c7f0f3c30d99445/73/page-frame.html',
            'cookie': self.yi_cookies,
            'content-type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 9; Redmi Note 7 Build/PKQ1.180904.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36 MicroMessenger/7.0.6.1460(0x27000634) Process/appbrand0 NetType/4G Language/zh_CN',
            'Host': 'cloud.cn2030.com',
            'Connection': 'Keep-Alive',
            'zftsl': self.confzmyy.get('zftsl')
        }
        # 填写预约时间
        self.yi_yytimes = self.confzmyy.get('yytimes')
        # 疫苗种类
        self.yi_ymid = self.confzmyy.getint('ymid')
        # 生日
        self.yi_birthday = self.confzmyy.get('birthday')
        # 身份证
        self.yi_cdid = self.confzmyy.get('cdid')
        # 电话
        self.yi_telphone = self.confzmyy.get('telphone')
        # 名字
        self.yi_name = self.confzmyy.get('name')
        # 城市ID
        self.yi_cityid = self.confzmyy.getint('cityid')
        # 性别
        self.yi_sex = self.confzmyy.getint('sex')

    def __init__(self):
        self.__init_config__()
        self.__init_var__()

    def __generate_random_str(randomlength):
        random_str = ''
        base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
        length = len(base_str) - 1
        for i in range(randomlength):
            random_str += base_str[random.randint(0, length)]
        return random_str

    def __CaptchaSlideCrack(self, tigerpath, dragonath, processedath):
        s =  SlideCrack(tigerpath, dragonath, processedath)
        return s.discern()

    def GetSubscribe(self):
        print(u'（1）开始访问获取客户订阅日期详细信息：GetCustSubscribeDateDetail')
        time.sleep(self.delaytime)
        payload = {
            'act': 'GetCustSubscribeDateDetail',
            'pid': self.yi_ymid,
            'id': self.yi_cityid,
            'scdate': self.yi_yytimes,
        }
        code = requests.get(
            url=self.url,
            headers=self.headers, params=payload, verify=False)
        # 转json
        if int(code.status_code) == 200:
            code_json_dict = code.json()
            print(code_json_dict)
            if int(code_json_dict['status']) == 200:
                if code_json_dict['list']:
                    print(code_json_dict['list'][0]['mxid'])
                    mxid = code_json_dict['list'][0]['mxid']
                    check_mxid = False
                    return check_mxid, mxid
                else:
                    print(u'九价还没开放')
                    check_mxid = True
                    mxid = ''
                    return check_mxid, mxid
            else:
                check_mxid = True
                mxid = ''
                return check_mxid, mxid
        else:
            print(code.status_code)
            check_mxid = True
            print('访问异常,继续访问')
            mxid = ''
            return check_mxid, mxid

    def Submit(self):
        # 获取验证码
        print(u'（2）访问验证码：GetCaptcha')
        time.sleep(self.delaytime)
        payload = {
            'act': 'GetCaptcha',
        }
        code = requests.get(
            url=self.url,
            headers=self.headers, params=payload, verify=False)
        # 转json
        if int(code.status_code) == 200:
            ck_s = self.__CaptchaVerify()
            return ck_s
        else:
            print('访问异常,继续访问%s' % code.status_code)
            ck_s = True
            return ck_s

    def GetCustSubscribeDateDetail(self):
        print(u'访问获取客户订阅日期详细信息：GetCustSubscribeDateDetail')
        time.sleep(self.int_time)
        payload = {
            'act': 'GetCustSubscribeDateDetail',
            'pid': self.yi_ymid,
            'id': self.yi_cityid,
            'scdate': self.yi_yytimes,
        }

        code = requests.get(
            url=self.url,
            headers=self.headers, params=payload, verify=False)
        # 转json

        if int(code.status_code) == 200:
            code_json_dict = code.json()
            print(code_json_dict)
            if int(code_json_dict['status']) == 200:
                print(code_json_dict['list'][0]['mxid'])
                mxid = code_json_dict['list'][0]['mxid']
                check_mxid = False
                return check_mxid, mxid
            else:
                check_mxid = True
                mxid = ''
                return check_mxid, mxid
        else:
            print(code.status_code)
            check_mxid = True
            print(u'访问异常,继续访问')
            mxid = ''
            return check_mxid, mxid

    # 验证码处理
    def __CaptchaVerify(self):
        print(u"（3）开始验证：CaptchaVerify")
        time.sleep(self.delaytime)
        payload = {
            'act': 'CaptchaVerify',
            'token': '',
            'x': self.xsite,
            'y': self.ysite,
        }

        code = requests.get(
            url=self.url,
            headers=self.headers, params=payload, verify=False)
        # 转json
        if int(code.status_code) == 200:
            code_json_dict = code.json()
            print(code_json_dict)
            if int(code_json_dict['status']) != 204 and int(code_json_dict['status']) != 201:
                if int(code_json_dict['status']) != 408:
                    print(u'验证码-验证成功')
                    print(u'guid:%s' % code_json_dict['guid'])
                    guid = code_json_dict['guid']
                    Checks = False
                    # 成功后去访问Save20结果去提交数据=预约成功
                    print(u'（4）马上提交')
                    self.Save20(guid)
                    return Checks
                else:
                    Checks = True
                    print(u'请重新授权Cookies')
                    return Checks
            else:
                Checks = True
                print(u'继续验证')
                return Checks

    def Save20(self, guid):
        payload = {
            'act': 'Save20',
            'birthday': self.yi_birthday,
            'tel': self.yi_telphone,
            'sex': self.yi_sex, # 性别2 女  1 男
            'cname': self.yi_name,
            'doctype': "1",
            'idcard': self.yi_cdid,
            'mxid': self.mxid,
            'date': self.yi_yytimes,
            'pid': self.yi_ymid,
            'Ftime': "1",
            'guid': guid,
        }
        print(payload)
        tongyong = requests.get(
            url=self.url,
            headers=self.headers, params=payload, verify=False)
        # 转json
        json_dict = tongyong.json()
        print(json_dict)
        if int(json_dict['status']) != 201:
            print(json_dict)
            print(u'预约成功')
        else:
            pass

    def run(self):
        requests.packages.urllib3.disable_warnings()
        # 获取订阅日期mxid
        while self.Checks:
            self.Checks, self.mxid = self.GetSubscribe()
        # 获取验证码
        self.Checks2 = True
        while self.Checks2:
            self.Checks2 =self.Submit()
        # 7Q90AC5oAABeYzQB = 26670

def excute_main():
    c = czmyy_test()
    c.run()

if __name__ == '__main__':
    excute_main()