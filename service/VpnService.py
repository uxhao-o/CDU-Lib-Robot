#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Author: ahao
# Time: 2021/5/30 10:58
"""
校园VPN认证文件
"""
import warnings
import execjs
from util.Utils import *
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class CduAuthentication:
    """
    Cdu校内网认证
    """
    def __init__(self, config: Config):
        self.username = config['username']
        self.userPwd = config['userPwd']
        self.randCode = ''
        self.TWFID = ''
        self.o = []

    def getTwfia(self):
        """
        第一次访问VPN登录界面，获取到Cookie 里的TWFID 和 CSRF_RAND_CODE码
        CSRF_RAND_CODE 用于前端rsa加密的extraCode  e.id = e.id + "_" + e.extraCode
        :return:
        """
        header = Header.vpnHeader(True, self.TWFID)
        url = 'https://vpn.cdu.edu.cn/por/login_auth.csp?apiversion=1'
        resp = requests.get(url=url, headers=header, verify=False)
        res = Util.dealRes(resp, "TwfID", "RSA_ENCRYPT_EXP", "RSA_ENCRYPT_KEY")
        self.TWFID = res['TwfID']
        # RSA加密扩展
        self.o.append(res['RSA_ENCRYPT_EXP'])
        # RSA加密密匙
        self.o.append(res['RSA_ENCRYPT_KEY'])
        self.o.append("")
        NotifyService.myPrint("访问CDU-VPN系统成功")

    def getRandCode(self):
        """
        vpn post登录之前获取 svpn_req_randcode
        :return:
        """
        header = Header.vpnHeader(False, self.TWFID)
        url = 'https://vpn.cdu.edu.cn/por/login_auth.csp?apiversion=1'
        resp = requests.get(url=url, headers=header, verify=False)
        res = Util.dealRes(resp, "CSRF_RAND_CODE")
        # 登录随机码
        self.randCode = res['CSRF_RAND_CODE']

    @DeprecationWarning
    def rsaPwd(self):
        """
        RSA加密, js2py读取js文件， 已经废弃
        :return:
        """
        warnings.warn("rsaPwd function use js2py is deprecated", DeprecationWarning)
        import js2py
        self.getRandCode()
        # 创建一个js2py环境的上下文对象
        context = js2py.EvalJs()
        pwd_extra = self.userPwd + '_' + self.randCode
        # print(pwd_extra)
        r = self.o[1]
        i = "10001"
        # - 拷贝使用到js文件的内容到本项目中
        # - 读取js文件的内容,使用context来执行它们
        with open('../js/rsa.js', 'r', encoding='utf8') as fp:
            js = fp.read()
        # 执行js内容
        context.execute(js)
        # 调用js函数rasPwd
        rasPwd = context.rasPwd(r, i, pwd_extra)
        return rasPwd


    def RSAPwd(self):
        """
        使用execjs 调用RSA.js加密算法, 加密密码
        :return:
        """
        self.getRandCode()
        jsstr = Util.getRsaJs()
        ctx = execjs.compile(jsstr)
        pwd_extra = self.userPwd + '_' + self.randCode
        r = self.o[1]
        i = "10001"
        NotifyService.myPrint("使用RSA加密密码成功")
        return ctx.call('rasPwd', r, i, pwd_extra)



    def login(self):
        """
        VPN认证
        :return:
        """
        # step1，第一次访问获取TWFID 和 随机码
        self.getTwfia()
        # rasPwd = self.rsaPwd()
        rasPwd = self.RSAPwd()
        NotifyService.myPrint("开始校园VPN认证,认证中......")
        header = Header.loginHeader(True, self.TWFID)
        data = {
            'mitm_result': None,
            'svpn_req_randcode': self.randCode,
            'svpn_name': self.username,
            'svpn_password': rasPwd,
            'svpn_rand_code': None,
        }
        url = 'https://vpn.cdu.edu.cn/por/login_psw.csp?anti_replay=1&encrypt=1&apiversion=1'
        resp = requests.post(url=url, headers=header, data=data, verify=False)
        res = Util.dealRes(resp, "TwfID", "Message")
        if res['Message'] == 'radius auth succ':
            NotifyService.myPrint("校园VPN认证成功")
            # 登录成功以后拿到的TwfID
            self.TWFID = res['TwfID']
        else:
            NotifyService.myPrint("校园VPN认证失败")
