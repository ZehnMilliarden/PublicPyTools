
#coding=utf-8

import requests
import time
import random
import configparser
import os
import sys

class czmyy_test:
    def __init__(self):
        # 延迟时间
        self.int_time = 4
        # Cookies
        self.cookies = 'ASP.NET_SessionId=qfzodsgrd1kl4jmkjzspn3k0'
        self.headers = {
            'charset': 'utf-8',
            'Accept-Encoding': 'gzip, deflate, br',
            'referer': 'https://servicewechat.com/wx2c7f0f3c30d99445/73/page-frame.html',
            'cookie': self.cookies,
            'content-type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 9; Redmi Note 7 Build/PKQ1.180904.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36 MicroMessenger/7.0.6.1460(0x27000634) Process/appbrand0 NetType/4G Language/zh_CN',
            'Host': 'cloud.cn2030.com',
            'Connection': 'Keep-Alive',
            'zftsl': '739a71bd55e8e6b56afcf1d982c10d7e'
        }

        proDir = os.path.split(os.path.realpath(__file__))[0]
        # 在当前文件路径下查找.ini文件
        configPath = os.path.join(proDir, "config.ini")
        self.conf = configparser.ConfigParser()
        self.conf.read(configPath)

        # 猜测验证码的X
        self.x = '33'
        self.Checks = True
        # 填写预约时间
        self.yuyue_times = self.conf.get('zmyy','yuyuetimes')
        # 1= 九价
        self.p_id = '1'
        # 生日
        self.yi_birthday = self.conf.get('zmyy', 'birthday')
        # 身份证
        self.yi_cdid = self.conf.get('zmyy', 'cdid')
        # 电话
        self.yi_telphone = self.conf.get('zmyy', 'telphone')
        # 名字
        self.yi_name = self.conf.get('zmyy', 'name')

    def generate_random_str(randomlength):
        random_str = ''
        base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
        length = len(base_str) - 1
        for i in range(randomlength):
            random_str += base_str[random.randint(0, length)]
        return random_str

    def GetSubscribe(self):
        print('（1）开始访问获取客户订阅日期详细信息：GetCustSubscribeDateDetail')
        time.sleep(self.int_time)
        payload = {
            'act': 'GetCustSubscribeDateDetail',
            'pid': self.p_id,
            'id': '243',
            'scdate': self.yuyue_times,
        }
        code = requests.get(
            url="https://cloud.cn2030.com/sc/wx/HandlerSubscribe.ashx",
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
        print('（2）访问验证码：GetCaptcha')
        time.sleep(self.int_time)
        payload = {
            'act': 'GetCaptcha',
        }
        code = requests.get(
            url="https://cloud.cn2030.com/sc/wx/HandlerSubscribe.ashx",
            headers=self.headers, params=payload, verify=False)
        # 转json
        if int(code.status_code) == 200:
            ck_s = self.YanZheng302()
            return ck_s
        else:
            print('访问异常,继续访问%s' % code.status_code)
            ck_s = True
            return ck_s

    def GetCustSubscribeDateDetail(self):
        print('访问获取客户订阅日期详细信息：GetCustSubscribeDateDetail')
        time.sleep(self.int_time)
        payload = {
            'act': 'GetCustSubscribeDateDetail',
            'pid': self.p_id,
            'id': '243',
            'scdate': self.yuyue_times,
        }

        code = requests.get(
            url="https://cloud.cn2030.com/sc/wx/HandlerSubscribe.ashx",
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
            print('访问异常,继续访问')
            mxid = ''
            return check_mxid, mxid

    def YanZheng302(self):
        print("（3）开始验证：CaptchaVerify")
        time.sleep(self.int_time)
        payload = {
            'act': 'CaptchaVerify',
            'token': '',
            'x': x,
            'y': '5',
        }

        code = requests.get(
            url="https://cloud.cn2030.com/sc/wx/HandlerSubscribe.ashx",
            headers=self.headers, params=payload, verify=False)
        # 转json
        if int(code.status_code) == 200:
            code_json_dict = code.json()
            print(code_json_dict)
            if int(code_json_dict['status']) != 204 and int(code_json_dict['status']) != 201:
                if int(code_json_dict['status']) != 408:
                    print('验证码-验证成功')
                    print('guid:%s' % code_json_dict['guid'])
                    guid = code_json_dict['guid']
                    Checks = False
                    # 成功后去访问Save20结果去提交数据=预约成功
                    print('（4）马上提交')
                    self.Save20(yuyue_times, p_id, mxid, guid)
                    return Checks
                else:
                    Checks = True
                    print('请重新授权Cookies')
                    return Checks
            else:
                Checks = True
                print('继续验证')
                return Checks

    def Save20(self, times, p_id, mxid, guid):
        payload = {
            'act': 'Save20',
            'birthday': self.yi_birthday,
            'tel': self.yi_telphone,
            'sex': "2", # 性别2 女  1 男
            'cname': self.yi_name,
            'doctype': "1",
            'idcard': self.yi_cdid,
            'mxid': mxid,
            'date': times,
            'pid': p_id,
            'Ftime': "1",
            'guid': guid,
        }
        print(payload)
        tongyong = requests.get(
            url="https://cloud.cn2030.com/sc/wx/HandlerSubscribe.ashx",
            headers=self.headers, params=payload, verify=False)
        # 转json
        json_dict = tongyong.json()
        print(json_dict)
        if int(json_dict['status']) != 201:
            print(json_dict)
            print('预约成功')
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