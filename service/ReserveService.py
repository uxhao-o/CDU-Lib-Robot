#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Author: ahao
# Time: 2021/5/31 16:16
"""
座位预约服务文件
"""
import datetime
import json
import requests
from util.Utils import *
from service.VpnService import CduAuthentication
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class CduLibService:
    """
    图书馆座位预约服务类
    """

    def __init__(self, cduAuthentication: CduAuthentication, config: Config):
        self.cduAuthentication = cduAuthentication
        self.Cookie = ''
        self.config = config
        self.msn = ''
        self.name = ''
        self.msg= []
        self.flag = False

    def login(self):
        """
        图书馆登录
        :return:
        """
        self.cduAuthentication.login()
        header = Header.loginHeader(False, self.cduAuthentication.TWFID)
        url = "http://libzwyy-cdu-edu-cn.vpn.cdu.edu.cn:8118/ClientWeb/pro/ajax/login.aspx?sf_request_type=ajax"
        data = {
            'id': self.config['username'],
            'pwd': self.config['userPwd'],
            'act': 'login',
        }
        resp = requests.post(url=url, headers=header, data=data, allow_redirects=False, verify=False)
        # json字符串转字典
        res = json.loads(resp.text)  # 根据字符串书写格式，将字符串自动转换成 字典类型
        if res['msg'] == 'ok':
            self.Cookie = header['Cookie'] + '; ' + resp.headers['Set-Cookie'].split(';')[0]
            # 签到系统需要用到
            self.msn = res['data']['msn']
            self.name = res['data']['name']
            NotifyService.myPrint('图书馆登录成功, 学号: {0}, 姓名: {1}'.format(res['data']['id'], self.name))
        else:
            NotifyService.myPrint('图书馆登录失败')

    def seatReserve(self):
        """
        座位预约
        :return:
        """
        self.login()
        # 获取预约的时间段
        startList = self.config['startTime'].split(',')
        endList = self.config['endTime'].split(',')
        for reserveTime in zip(startList, endList):
            # 当前时间加 1 天
            day = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            # 拼接时间字符串
            start = day + '+' + reserveTime[0][:2] + '%3A' + reserveTime[0][2:]
            end = day + '+' + reserveTime[1][:2] + '%3A' + reserveTime[1][2:]
            header = Header.setReserveHeader(self.Cookie)
            url = "http://libzwyy-cdu-edu-cn.vpn.cdu.edu.cn:8118/ClientWeb/pro/ajax/reserve.aspx?dialogid=&dev_id={0}" \
                  "&lab_id=&kind_id=&room_id=&type=dev&prop=&test_id=&term=&number=&classkind=&test_name=" \
                  "&start={1}&end={2}&start_time={3}&end_time={4}&up_file=&memo=&" \
                  "act=set_resv&sf_request_type=ajax".format(self.config['devId'], start, end,
                                                             reserveTime[0], reserveTime[1])
            resp = requests.get(url=url, headers=header, allow_redirects=False, verify=False)
            # json字符串转字典
            res = json.loads(resp.text)
            time = day + ' ' + reserveTime[0][:2] + ':' + reserveTime[0][2:] + '—' + reserveTime[1][:2] + ':' + reserveTime[1][2:]
            if res['msg'] == '操作成功！':
                self.msg.append('预约座位: {0}, 预约时间段: {1} 成功'.format(self.config['devId'], time))
                NotifyService.myPrint('预约座位: {0}, 预约时间段: {1} 成功'.format(self.config['devId'], time))
                self.flag = True
            else:
                self.flag = False
                NotifyService.myPrint('预约座位:{0}, 时间段:{1}, 失败, msg: {2}'.format(self.config['devId'], time, res['msg']))
                self.msg.append('预约座位:{0}, 时间段:{1}, 失败, msg: {2}'.format(self.config['devId'], time, res['msg']))
        if self.flag:
            NotifyService.server(config=self.config, title='座位预约成功', name=self.name, msg=self.msg)
        else:
            self.msg.append("请自行访问CDU图书馆公众号预约座位")
            NotifyService.server(config=self.config, title='座位预约失败', name=self.name, msg=self.msg)