#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Author: ahao
# Time: 2021/5/31 18:24
"""
签退入口文件
"""
from service.ReserveService import CduLibService
from service.VpnService import *
from service.ClockService import CduLibClock
from util.Utils import Config


def main(event, content):
    config = Config.getConfig()
    # 创建校园认证对象
    cduAuthentication = CduAuthentication(config)
    # 创建图书馆服务类对象
    cduLibService = CduLibService(cduAuthentication, config)
    # 创建图书馆签到类对象
    cduLibClock = CduLibClock(cduAuthentication, cduLibService, config)
    # 调用签到服务
    cduLibClock.signOut()


if __name__ == '__main__':
    main(1, 1)