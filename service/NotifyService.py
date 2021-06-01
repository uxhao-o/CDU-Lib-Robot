#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Author: ahao
# Time: 2021/5/31 18:52
"""
server酱通知服务文件
"""
import datetime
import json
import requests

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class NotifyService:

    @staticmethod
    def server(**kwargs):
        """
        Server酱推送
        """
        if kwargs['config']['sckey'] == '':
            return
        url = 'https://sc.ftqq.com/' + kwargs['config']['sckey'] + '.send'
        # 构造发送内容
        title, content = NotifyService.diyText(config=kwargs['config'], title=kwargs['title'], name=kwargs['name'],
                                               msg=kwargs['msg'])
        response = requests.get(url, params={"text": title, "desp": content},)
        data = json.loads(response.text)
        if data['errno'] == 0:
            NotifyService.myPrint('学号:' + kwargs['config']['username'] + '  Server酱推送成功')
        else:
            NotifyService.myPrint('学号:' + kwargs['config']['username'] + '  Server酱推送失败,请检查sckey是否正确')

    @staticmethod
    def diyText(**kwargs):
        """
        自定义要推送到微信的内容
        title:消息的标题
        content:消息的内容,支持MarkDown格式
        """
        msg1 = ''
        if isinstance(kwargs['msg'], list):  # 判断msg数据类型是否为列表类型
            for i in kwargs['msg']:
                msg1 = msg1 + '- `' + i + "`\n"
        else:
            msg1 = "- `" + kwargs['msg'] + "` \n"
        title = "CDU-Lib-Robot -- " + kwargs['title']
        content = (
                "------\n"
                "#### CDU-Lib-Robot 图书馆全自动机器人 \n"
                "- `学号：" + str(kwargs['config']['username']) + "  姓名：" + kwargs['name'] + "`\n"
                + msg1 + "\n"
                "<br/>      </br>" + "\n"
                "- CDU-Lib-Robot永久免费。请勿倒卖！！！" + "\n"
                "- 脚本定制,期末项目代做(Python,Java,C,Vue),网课代看" + "\n"
                "- 实习盖章,实习报告代写,毕业设计代做" + "\n"
                "- 冒充男朋友😄" + "\n"
                "- `请联系ahao，VX：CSRF5XX`" + "\n"
                "- ahao个人网站：https://www.uxhao.com" + "\n"
                "- 不定时更新技术贴子" + "\n"
        )
        return title, content

    @staticmethod
    def myPrint(text):
        """
        打印日志
        """
        time_stamp = datetime.datetime.now()
        print(time_stamp.strftime('%Y.%m.%d-%H:%M:%S') + '   ' + str(text))

