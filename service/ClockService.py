#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Author: ahao
# Time: 2021/5/31 16:15
"""
打卡服务文件
"""
import json

import requests
from urllib.parse import unquote
from service.ReserveService import CduLibService
from service.VpnService import CduAuthentication
from util.Utils import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class CduLibClock:
    """
    图书馆打卡服务类
    """
    def __init__(self, cduAuthentication: CduAuthentication, cduLibService: CduLibService, config: Config):
        self.cduAuthentication = cduAuthentication
        self.cduLibService = cduLibService
        self.config = Config.getConfig()
        self.msg= ''

    def bindUser(self, baseUrl, TwFid, callerFlag):
        """
        签到系统绑定账号,  签到系统第一次使用需要绑定账号
        :param baseUrl:
        :param TwFid: vpn认证码
        :param callerFlag: 本函数的调用者的标识， 0表示signIn, 1表示signOut
        :return:
        """
        NotifyService.myPrint("第一次使用签到系统，执行绑定账号功能")
        firstUrl = 'http://update.unifound.net/wxnotice/s.aspx?c={0}_Seat_{1}_{2}'.format(self.config['devLab'],
                                                                                          self.config['devId'],
                                                                                          self.config['sysId'])
        # 访问二维码的链接
        firstHeader = Header.bindHeader()
        bindResp = requests.get(url=firstUrl, headers=firstHeader, allow_redirects=False)
        # 中间链接
        intermediaryUrl = baseUrl + unquote(bindResp.headers['Location']).split('cn')[1]
        # 重定向，获取真正的登陆链接
        C1 = 'td_cookie=1071120225; UM_distinctid_-_cdu.edu.cn=179bb09d1a4238-02375d877340e2-4c3f2c72-fa000-179bb09' \
             'd1a51f3; cna_-_.mmstat.com=auY5GbZglz4CAcpzUAq0f71c; cna_-_.cnzz.com=auY5GbZglz4CAcpzUAq0f71c; UM_distin' \
             'ctid=179c56ed9819f5-04f7390162c6ee8-4c3f2c72-fa000-179c56ed982623; isPortal=false; isPortal_-_.cdu.edu.' \
             'cn=false; TWFID='+TwFid
        header = Header.signInHeader(C1)
        bindUserResp = requests.get(url=intermediaryUrl, headers=header, allow_redirects=False)
        extraCookie = bindUserResp.headers['Set-Cookie'].split(';')[0]
        # 重新组装Cookie
        cookie = C1 + '; ' + extraCookie
        Referer = baseUrl + bindUserResp.headers['Location']
        realHeader = Header.signInHeader(cookie, Referer)
        realUrl = baseUrl + '/Pages/WxSeatSign.aspx'
        data = {
            'DoLogon': 'true',
            'sysidform': None,
            'aluseridform': None,
            'wxuseridform': None,
            'szLogonName': self.config['username'],
            'szPassword': self.config['userPwd'],
            'dwBind': '1',
        }
        realBindResp = requests.post(url=realUrl, headers=realHeader, data=data, allow_redirects=False)
        print(unquote(realBindResp.text))
        print(realBindResp.headers['Location'])
        if 'title=登录成功' in unquote(realBindResp.headers['Location']).split('&'):
            # 绑定账号成功, 重新执行本函数的调用者
            if callerFlag == 0:
                NotifyService.myPrint("签到系统账户绑定成功, 重新执行签到功能")
                self.signIn()
            elif callerFlag == 1:
                NotifyService.myPrint("签到系统账户绑定成功, 重新执行签退功能")
                self.signOut()
        else:  # 绑定账号失败
            NotifyService.myPrint("签到系统绑定账号失败, 请用微信扫码座位二维码后继续使用CDU-Lib-Robot")

    def signIn(self):
        """
        打卡, 实现预约座位打卡
        :return:
        """
        # 签到系统登录之前先 通过vpn认证和 图书馆登录
        self.cduLibService.login()
        header = Header.signInHeader(self.cduLibService.Cookie)
        baseUrl = "http://libzwyy-cdu-edu-cn.vpn.cdu.edu.cn:8118"
        url1 = baseUrl + "/Pages/WxSeatSign.aspx?sta=1&sysid={0}&lab={1}&dev={2}&msn={3}".format(self.config['sysId'],
                                                    self.config['devLab'], self.config['devId'], self.cduLibService.msn)

        resp1 = requests.get(url=url1, headers=header, allow_redirects=False)
        location1 = resp1.headers['Location']
        flag = unquote(location1).split('&')
        if 'title=未绑定用户' in flag:  # 签到系统未绑定账号
            # 调用绑定账号的函数
            self.bindUser(baseUrl, self.cduAuthentication.TWFID, 0)
        elif 'title=登录成功' in flag:
            ResvMsg = unquote(location1).split('&')[-2].split(',')[0].split('=')[1]
            NotifyService.myPrint("签到系统登录成功")
            # 没有重定向链接开始签到
            header = Header.signInHeader(self.cduLibService.Cookie, url1)
            # 签到
            url2 = baseUrl + "/pages/WxSeatSign.aspx?Userin=true"
            resp2 = requests.get(url=url2, headers=header, allow_redirects=False)
            location2 = resp2.headers['Location']
            # TODO 签到服务时获取到的是当前座位下一个时间段的信息，非当前时间段，待解决！
            msg = unquote(location2).split('&')[2].split('=')[1]
            if unquote(location2).split('&')[1].split('=')[1] == '操作成功':
                NotifyService.myPrint('座位: {0}, {1}, {2}'.format(self.config['devId'], ResvMsg, msg))
                self.msg = '座位: {0}, {1}, {2}'.format(self.config['devId'], ResvMsg, msg)
                NotifyService.server(config=self.config, title='座位签到成功', name=self.cduLibService.name, msg=self.msg)
            else:
                NotifyService.myPrint('座位: {0}, {1}, {2}'.format(self.config['devId'], ResvMsg, msg))
                self.msg = '座位: {0}, {1}, {2}'.format(self.config['devId'], ResvMsg, msg)
                NotifyService.server(config=self.config, title='座位签到失败', name=self.cduLibService.name, msg=self.msg)
        elif 'title=当前使用中' in flag:
            NotifyService.myPrint('当前正在使用中, 无需签到')
        elif 'title=操作失败' in flag:
            NotifyService.server(config=self.config, title='设备已分配给他人使用', name=self.cduLibService.name, msg=self.msg)
            NotifyService.myPrint('设备已分配给他人使用,未暂离')
        else:
            pass

    @DeprecationWarning
    def signOut(self):
        """
        签退, 实现预约座位签退, 二维码无法签退，已废弃
        :date: 2021.07.17
        :return:
        """
        # 签到系统登录之前先 通过vpn认证和 图书馆登录
        self.cduLibService.login()
        header = Header.signInHeader(self.cduLibService.Cookie)
        baseUrl = "http://libzwyy-cdu-edu-cn.vpn.cdu.edu.cn:8118"
        url1 = baseUrl + "/Pages/WxSeatSign.aspx?sta=1&sysid={0}&lab={1}&dev={2}&msn={3}".format(self.config['sysId'],
                                                    self.config['devLab'], self.config['devId'], self.cduLibService.msn)
        resp1 = requests.get(url=url1, headers=header, allow_redirects=False)
        location1 = resp1.headers['Location']
        url2 = baseUrl + location1
        flag = unquote(location1).split('&')
        if 'title=未绑定用户' in flag:  # 签到系统未绑定账号
            # 调用绑定账号的函数
            self.bindUser(baseUrl, self.cduAuthentication.TWFID, 1)
        elif 'title=当前使用中' in flag:
            header = Header.signInHeader(self.cduLibService.Cookie, url2)
            url2 = baseUrl + "/Pages/WxSeatSign.aspx?DoUserOut=2"
            resp2 = requests.get(url=url2, headers=header, allow_redirects=False)
            location2 = resp2.headers['Location']
            # 去掉微信推送显示resvMsg
            resvMsg = unquote(location1).split('&')[-2].split(',')[0].split('=')[1]
            if unquote(location2).split('&')[1].split('=')[1] == '操作成功':
                NotifyService.myPrint('座位: {0}, {1}, 签退成功'.format(self.config['devId'], resvMsg))
                self.msg = '座位: {0}, {1}, 签退成功'.format(self.config['devId'], resvMsg)
                NotifyService.server(config=self.config, title='座位签退成功', name=self.cduLibService.name, msg=self.msg)
            else:
                NotifyService.myPrint('座位: {0}, {1}, 签退失败'.format(self.config['devId'], resvMsg))
                self.msg = '座位: {0}, {1}, 签退失败'.format(self.config['devId'], resvMsg)
                NotifyService.server(config=self.config, title='座位签退失败', name=self.cduLibService.name, msg=self.msg)
        elif 'title=可用' in flag:
            self.msg = '座位: {0}, 当前座位未使用，请登录CDU图书馆公众号自行查看。'.format(self.config['devId'])
            NotifyService.myPrint('当前座位未使用，请登录CDU图书馆公众号自行查看。')
            NotifyService.server(config=self.config, title='座位未使用无需签退', name=self.cduLibService.name, msg=self.msg)
        else:
            NotifyService.myPrint('签退遇到未知错误')


    def signOutNew(self):
        """
        签退, 实现预约座位签退, 通过预约记录的id进行签退
        :date: 2021.07.17 22:30 更新图书馆二维码无法签退问题
        :return:
        """
        # 签退之前先 通过vpn认证和 图书馆登录
        self.cduLibService.login()
        header = Header.signInHeader(self.cduLibService.Cookie)

        # 先获取当前预约的单号id
        getResvIdUrl = 'http://libzwyy-cdu-edu-cn.vpn.cdu.edu.cn:8118/ClientWeb/pro/ajax/reserve.aspx?stat_flag=9&act='\
                       'get_my_resv'
        resvIdResp = requests.get(url=getResvIdUrl, headers=header, allow_redirects=False)
        # json字符串转字典
        resvIdResp = json.loads(resvIdResp.text)
        resvId = resvIdResp['data'][0]['id']  # 默认当前使用中的预约记录排在第一个
        # 签退链接
        baseUrl = "http://libzwyy-cdu-edu-cn.vpn.cdu.edu.cn:8118"
        url1 = baseUrl + "/ClientWeb/pro/ajax/reserve.aspx?act=resv_leave&type=2&resv_id={0}".format(resvId)
        resp1 = requests.get(url=url1, headers=header, allow_redirects=False)
        resp1 = json.loads(resp1.text)
        msg = resp1['msg']  # 返回的结果
        ret = resp1['ret']  # 成功的状态，1表示成功，0表示失败
        if ret == '1':  # 签退成功
            NotifyService.myPrint('签退成功, 座位: {0}, {1}'.format(self.config['devId'], msg))
            self.msg = '签退成功, 座位: {0}, {1}'.format(self.config['devId'], msg)
            NotifyService.server(config=self.config, title='座位签退成功', name=self.cduLibService.name, msg=self.msg)
        elif ret == '0':  # 签退失败
            NotifyService.myPrint('签退失败, 座位: {0}, {1}'.format(self.config['devId'], self.msg))
            self.msg = '签退失败, 座位: {0}, {1}'.format(self.config['devId'], msg)
            NotifyService.server(config=self.config, title='座位签退失败', name=self.cduLibService.name, msg=self.msg)
        else:
            self.msg = '签退遇到未知错误， 请登录CDU图书馆公众号自行查看'
            NotifyService.myPrint('当前座位未使用，请登录CDU图书馆公众号自行查看')
            NotifyService.server(config=self.config, title='签退遇到未知错误', name=self.cduLibService.name, msg=self.msg)

