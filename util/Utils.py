#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Author: ahao
# Time: 2021/5/30 11:04
from xml.dom.minidom import parseString
from configparser import ConfigParser
import js
from service.NotifyService import NotifyService


class Util:
    """
    工具类
    """
    @staticmethod
    def getRsaJs():
        """
        读取rsa.js 加密算法文件
        :return:
        """
        f = open("js/rsa.js", encoding='UTF-8')
        line = f.readline()
        htmlstr = ''
        while line:
            htmlstr = htmlstr + line
            line = f.readline()
        return htmlstr

    @staticmethod
    def dealRes(response, *param):
        """
        处理request返回的结果
        :param response:
        :param param:
        :return:
        """
        res = {}
        doc = parseString(response.text)
        collection = doc.documentElement
        # 登录随机码
        for key in param:
            value = collection.getElementsByTagName(key)[0].childNodes[0].data
            res.update({key: value})
        return res


class Config:
    """
    配置文件类
    """
    @staticmethod
    def getConfig():
        """
        从配置文件中获取用户信息和座位ID
        :return:
        """
        config = ConfigParser()
        config.read('./config/config.ini', encoding='UTF-8-sig')
        username = config['token']['username']
        password = config['token']['password']
        startTime = config['reserve']['startTime']
        endTime = config['reserve']['endTime']
        devId = config['reserve']['devId']
        devLab = config['reserve']['devLab']
        sysId = config['reserve']['sysId']
        isEveryDayReserve = config['reserve']['isEveryDayReserve']
        sckey = config['setting']['sckey']
        config = {
            'username': username,
            'userPwd': password,
            'devId': devId,
            'startTime': startTime,
            'endTime': endTime,
            'isEveryDayReserve': isEveryDayReserve,
            'sckey': sckey,
            'devLab': devLab,
            'sysId': sysId
        }
        return config


class Header:
    """
    请求头类
    """

    @staticmethod
    def vpnHeader(isFirst: bool, TwfID: str):
        header = {
            'Host': 'vpn.cdu.edu.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep - alive',
            'Upgrade - Insecure - Requests': '1',
            'Cache-Control': 'max-age=0',
            'If-Modified-Since': 'Mon, 24 Feb 2020 09:42:21 GMT',
            'Cookie': 'privacy=1; UM_distinctid_-_cdu.edu.cn=179bb09d1a4238-02375d877340e2-4c3f2c72-fa000-179bb09d1a51f'
                      '3; cna_-_.mmstat.com=auY5GbZglz4CAcpzUAq0f71c; cna_-_.cnzz.com=auY5GbZglz4CAcpzUAq0f71c; '
                      'language=zh_CN;',
        }
        if isFirst:
            return header
        else:
            header['Cookie'] = 'privacy=1; UM_distinctid_-_cdu.edu.cn=179bb09d1a4238-02375d877340e2-4c3f2c72-fa0' \
                               '00-179bb09d1a51f3; cna_-_.mmstat.com=auY5GbZglz4CAcpzUAq0f71c; cna_-_.cnzz.com=auY5' \
                               'GbZglz4CAcpzUAq0f71c; language=zh_CN; TWFID=' + TwfID
            header.update({
                'Cache-Control': 'no-cache',
                'Content-Length': '607',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Origin': 'https://vpn.cdu.edu.cn',
                'Pragma': 'no-cache',
                'Referer': 'https://vpn.cdu.edu.cn/portal/',
                'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="91", "Chromium";v="91"',
                'sec-ch-ua-mobile': '?0',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
            })
            return header

    @staticmethod
    def loginHeader(isVpnLogin: bool, TwfID: str):
        header = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Length': '607',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'privacy=1; UM_distinctid_-_cdu.edu.cn=179bb09d1a4238-02375d877340e2-4c3f2c72-fa000-179bb09d1a51'
                      'f3; cna_-_.mmstat.com=auY5GbZglz4CAcpzUAq0f71c; cna_-_.cnzz.com=auY5GbZglz4CAcpzUAq0f71c; '
                      'language=zh_CN; TWFID=' + TwfID,
            'Host': 'vpn.cdu.edu.cn',
            'Origin': 'https://vpn.cdu.edu.cn',
            'Pragma': 'no-cache',
            'Referer': 'https://vpn.cdu.edu.cn/portal/',
            'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="91", "Chromium";v="91"',
            'sec-ch-ua-mobile': '?0',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37',
        }
        if isVpnLogin:
            return header
        else:
            header['Content-Length'] = '38'
            header['Host'] = 'libzwyy-cdu-edu-cn.vpn.cdu.edu.cn:8118'
            header['X-Requested-With'] = 'XMLHttpRequest'
            header['Origin'] = 'http://libzwyy-cdu-edu-cn.vpn.cdu.edu.cn:8118'
            header['Referer'] = 'http://libzwyy-cdu-edu-cn.vpn.cdu.edu.cn:8118/ClientWeb/xcus/ic2/Default.aspx'
            return header

    @staticmethod
    def setReserveHeader(cookie):
        header = {
            'Host': 'libzwyy-cdu-edu-cn.vpn.cdu.edu.cn:8118',
            'Referer': 'http://libzwyy-cdu-edu-cn.vpn.cdu.edu.cn:8118/ClientWeb/xcus/ic2/Default.aspx',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Connection': 'close',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cookie': cookie
        }
        return header

    @staticmethod
    def signInHeader(Cookie=None, Referer=None):
        """
        签到
        :return:
        """
        # 使用苹果手机UA
        header = {
            'Host': 'libzwyy-cdu-edu-cn.vpn.cdu.edu.cn:8118',
            'User-Agent': 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 2_0 like Mac OS X; ja-jp) AppleWebKit/525.18.1 '
                          '(KHTML, like Gecko) Version/3.1.1 Mobile/5A347 Safari/52',
            # 'User-Agent': 'Mozilla/5.0 (Linux; U; Android 11; zh-cn; GM1900 Build/RKQ1.201022.002) AppleWebKit/537.36 '
            #               '(KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 '
            #               'HeyTapBrowser/40.7.22.1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'close',
            'Upgrade-Insecure-Requests': '1',
            'Cookie': Cookie
        }
        if Referer is not None:
            header['Referer'] = Referer
        return header

    @staticmethod
    def bindHeader():
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'close',
            'Upgrade-Insecure-Requests': '1',
            'Cookie': 'td_cookie=1071120225; UM_distinctid_-_cdu.edu.cn=179bb09d1a4238-02375d8' \
                      '77340e2-4c3f2c72-fa000-179bb09d1a51f3; cna_-_.mmstat.com=auY5GbZglz4CAcpzU' \
                      'Aq0f71c; cna_-_.cnzz.com=auY5GbZglz4CAcpzUAq0f71c; UM_distinctid=179c56e'
                      'd9819f5-04f7390162c6ee8-4c3f2c72-fa000-179c56ed982623; isPortal=false;'
                      ' isPortal_-_.cdu.edu.cn=false; ASP.NET_SessionId=gmrw1ilkrxni3laijrzwujdr'
                      '; TWFID=0900526778be6c28'
        }