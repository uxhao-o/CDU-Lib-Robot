## 一、CDU-Lib-Robot 图书管全自动机器人

### 1. CDU-Lib-Robot简介

`CDU-Lib-Robot`为成都大学图书馆座位预约系统全自动工具。`每天定时预约座位（预约的是第二天的位置, 支持多时间段预约）` + `自动签到签退`。每天的`座位预约` 和 `签到签退`情况会在 完成后 自动推送到你的微信，实时反馈每日`座位预约`和`签到签退`情况。无需人工操作。特别提醒：自动`签到签退`可能会存在第一次使用需要绑定账号的情况，目前未解决，后续版本会更新。



GitHub链接： https://github.com/ahaox/CDU-Lib-Robot

Gitee链接： https://gitee.com/ahaox/CDU-Lib-Robot

作者：`ahao`。

### 2. 发布日志

##### 2021.05.31 发布 v1

### 3. 发布初心

`方便成大考研学子 和 图书馆常驻专家 使用，摆脱每天都要预约位置 和 签到签退的烦扰！`

### 4. 注意事项

① 本脚本完全免费，如果您通过其他渠道消费购买，请一定口吐芬芳对方！！！

② 本脚本不设计第三方信息收集，不存在保存使用者的账号密码等信息。

③ 本仓库发布的`CDU-Lib-Robot`项目中涉及的任何脚本，仅用于`CDU-图书馆座位预约`系统，禁止用于商业用途，不能保证其合法性，准确性，完整性和有效性，请根据情况自行判断。

④ `ahao` 对任何脚本问题概不负责，包括但不限于由任何脚本错误导致的任何损失或损害.

⑤ 请勿将`CDU-Lib-Robot`项目的任何内容用于商业或非法目的，否则后果自负。

⑥ 如果任何单位或个人认为该项目的脚本可能涉嫌侵犯其权利，则应及时通知并提供身份证明，所有权证明，我们将在收到认证文件后删除相关脚本。

⑦ 以任何方式查看此项目的人或直接或间接使用`CDU-Lib-Robot`项目的任何脚本的使用者都应仔细阅读此声明。`ahao` 保留随时更改或补充此免责声明的权利。一旦使用并复制了任何相关脚本或`CDU-Lib-Robot`项目，则视为您已接受此免责声明。

⑧ 您必须在下载后的24小时内从计算机或手机中完全删除以上内容。



## 二、主要功能

### 1.  提前一天预约座位

### 2. 支持多时间段预约

### 3. 支持自动签到签退



## 三、使用教程（小白版）

### 1. 下载项目代码

进入本项目代码仓下载ZIP压缩包到本地，并解压到桌面。

<img src="https://gitee.com/ahaox/images-picgo/raw/master/img/20210531225656.png" alt="image-20210531225649629" style="zoom: 33%;" />



解压到桌面

<img src="https://gitee.com/ahaox/images-picgo/raw/master/img/20210531225844.png" alt="image-20210531225844896" style="zoom:50%;" />



### 2. 进入云函数

腾讯云函数免费开通地址，地址：https://console.cloud.tencent.com/scf/list-create?rid=1&ns=default

登录以后按照流程自行开通。

### 3. 新建函数

① 创建函数名`CDU-Lib-Robot-Reserve` ，创建方式选择 **自定义创建** ，运行环境选**Python 3.6**，

执行方法设置为 `MainReserve.main`

<img src="https://gitee.com/ahaox/images-picgo/raw/master/img/20210601083127.png" alt="image-20210601083120850" style="zoom:50%;" />

② 创建函数名`CDU-Lib-Robot-Reserve`



### 4. 上传代码

确保环境为**python 3.6**，执行方法改为：`index.main`，提交方式一定要选 **本地上传文件夹** ，然后选择解压到桌面的文件夹 **isp-cdu-master** ，然后点击这个上传把文件夹上传进来。

![image-20210208221947302](https://cdn.jsdelivr.net/gh/ahaox/pictures/image20210208221947.png)

文件夹上传成功后，点击`高级配置`

<img src="https://gitee.com/ahaox/images-picgo/raw/master/img/20210601083232.png" alt="image-20210601083232099"  />

### 5. 高级配置

内存用不了太大，**128MB**就够了，超时时间改为最大的**900秒**，然后点击最下面的完成。

<img src="https://gitee.com/ahaox/images-picgo/raw/master/img/20210601083205.png" alt="image-20210601083204885" style="zoom: 33%;" />

### 6. 配置账号

自己改下`config.ini`里的`账号密码`、`预约时间`、`座位信息`及`Server酱密匙`，更改完后点击保存，部署并测试。如果你的配置没有错，稍等几分钟便可以看到结果，在此期间不要刷新页面。结果会在执行日志里。 

预约座位信息的获取方式： [点击这里](GetSeatInfo.md)

**Server酱密匙** 用于微信推送打卡情况，需要自己申请，申请地址： http://sc.ftqq.com/

![image-20210601084129561](https://gitee.com/ahaox/images-picgo/raw/master/img/20210601084129.png)



### 7. 安装依赖

点击终端，然后选择新终端，显示终端窗口，在终端窗口里面输入：

```bash
cd src/ && /var/lang/python3/bin/python3 -m pip install -r requirements.txt -t .
```

![image-20210601090443503](https://gitee.com/ahaox/images-picgo/raw/master/img/20210601090443.png)

输入命令后回车执行，等待安装完成。大概1分钟左右。

如下图所示，出现Successfully 表示成功

![image-20210601090530237](https://gitee.com/ahaox/images-picgo/raw/master/img/20210601090530.png)



① 部署函数

![image-20210601090722643](https://gitee.com/ahaox/images-picgo/raw/master/img/20210601090722.png)

② 部署成功，点击测试

![image-20210601090812453](https://gitee.com/ahaox/images-picgo/raw/master/img/20210601090812.png)



![image-20210601091438051](https://gitee.com/ahaox/images-picgo/raw/master/img/20210601091438.png)



### 8. 设置定时

新建触发器，触发周期为自定义，表达式就是每天的什么时候做任务，我选择的早上8点30分，可以自行修改，填好后点击提交即可，到此你的ISP-CDU疫情自动打卡项目便部署完成，感谢使用！！

![image-20210208230222605](https://cdn.jsdelivr.net/gh/ahaox/pictures/image20210208230222.png)



## 四、打赏作者

![pay](https://cdn.jsdelivr.net/gh/ahaox/pictures/image20210208232946.png "在这里输入图片标题")

 **金额不论大小。一分也是爱。** 

