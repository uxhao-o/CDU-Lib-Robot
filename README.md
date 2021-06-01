## 一、CDU-Lib-Robot 图书管全自动机器人

### 1. CDU-Lib-Robot简介

`CDU-Lib-Robot`为成都大学图书馆座位预约系统全自动工具。==每天定时预约座位（预约的是第二天的位置, 支持多时间段预约）== + ==自动签到签退==。

每天的==座位预约== 和 ==签到签退==情况会在 完成后 ==自动推送到你的微信==，实时反馈每日==座位预约==和==签到==, ==签退==情况。无需人工操作。



GitHub链接： https://github.com/ahaox/CDU-Lib-Robot

Gitee链接： https://gitee.com/ahaox/CDU-Lib-Robot

作者：`ahao`，网站: https://www.uxhao.com 本项目的实现过程已更新到网站上。



### 2. 发布日志

2021.06.01 发布 v1



### 3. 发布初心

==方便成大考研学子 和 图书馆常驻专家 使用，摆脱每天都要预约位置 和 签到 签退的烦扰！==



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

#### 1.  提前一天预约座位

预约后微信推送 预约消息

<img src="https://gitee.com/ahaox/images-picgo/raw/master/img/20210601204404.png" style="zoom: 33%;" />

#### 2. 支持多时间段预约



#### 3. 支持自动签到签退

<img src="https://gitee.com/ahaox/images-picgo/raw/master/img/20210601204915.png" alt="image-20210601204915855" style="zoom: 33%;" />

签到成功，自动推送消息到微信

<img src="https://gitee.com/ahaox/images-picgo/raw/master/img/20210601205132.png" alt="image-20210601205132903" style="zoom:50%;" />

签退成功，推送微信

<img src="https://gitee.com/ahaox/images-picgo/raw/master/img/20210601205015.png" alt="image-20210601205015350" style="zoom:50%;" />



## 三、使用教程（小白版）

### 1. 下载项目代码

进入本项目代码仓下载ZIP压缩包到本地，并解压到桌面。（建议从gitee下载）

![image-20210601205450235](https://gitee.com/ahaox/images-picgo/raw/master/img/20210601205450.png)



解压到桌面

<img src="https://gitee.com/ahaox/images-picgo/raw/master/img/20210531225844.png" alt="image-20210531225844896" style="zoom:50%;" />



### 2. 进入云函数

腾讯云函数免费开通地址，地址：https://console.cloud.tencent.com/scf/list-create?rid=1&ns=default

登录以后按照流程自行开通。

### 3. 创建座位预约服务云函数

> 注意：如果要使用，座位预约，签到，签退功能需要创建三个云函数

#### 3.1 创建函数

创建函数名`CDU-Lib-Robot-Reserve` （用于座位预约服务），创建方式选择 **自定义创建** ，运行环境选**Python 3.6**，执行方法设置为 `MainReserve.main`

<img src="https://gitee.com/ahaox/images-picgo/raw/master/img/20210601083127.png" alt="image-20210601083120850" style="zoom:50%;" />



#### 3.2 上传代码

确保环境为**python 3.6**，执行方法改为：`index.main`，提交方式一定要选 **本地上传文件夹** ，然后选择解压到桌面的文件夹 **isp-cdu-master** ，然后点击这个上传把文件夹上传进来。

<img src="https://gitee.com/ahaox/images-picgo/raw/master/img/20210601185419.png" alt="image-20210601185419023" style="zoom:67%;" />

文件夹上传成功后，点击`高级配置`

<img src="https://gitee.com/ahaox/images-picgo/raw/master/img/20210601083232.png" alt="image-20210601083232099"  />



#### 3.3 高级配置

内存用不了太大，**128MB**就够了，超时时间改为最大的**900秒**，然后点击最下面的完成。

<img src="https://gitee.com/ahaox/images-picgo/raw/master/img/20210601083205.png" alt="image-20210601083204885" style="zoom: 33%;" />

#### 3.4 配置账号密码、座位信息、预约时间

自己改下`config.ini`里的`账号密码`、`预约时间`、`座位信息`及`Server酱密匙`，更改完后按`Ctrl+S` 保存修改。

预约座位信息的获取方式： [点击这里](GetSeatInfo.md)

**Server酱密匙** 用于微信推送打卡情况，需要自己申请，申请地址： http://sc.ftqq.com/， 

![image-20210601084129561](https://gitee.com/ahaox/images-picgo/raw/master/img/20210601084129.png)



#### 3.5 安装依赖

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



#### 3.6 设置定时

新建触发器，触发周期为自定义，表达式就是每天的什么时候执行，这里设置为每天0点0分40秒，可以自行修改（不建议修改），填好后点击提交即可，此时 `座位预约服务` 就已经部署好了。

时间表达式具体可参考：[云函数 定时触发器 - 开发指南 - 文档中心 - 腾讯云 (tencent.com)](https://cloud.tencent.com/document/product/583/9708#cron-.E8.A1.A8.E8.BE.BE.E5.BC.8F)

![image-20210601192629284](https://gitee.com/ahaox/images-picgo/raw/master/img/20210601192629.png)



### 4. 签到服务

#### 4.1 克隆云函数

直接复制 ==座位预约服务云函数== `CDU-Lib-Robot-Reserve` ,   把函数名称更改为：`CDU-Lib-Robot-SignIn` 

![image-20210601193511214](https://gitee.com/ahaox/images-picgo/raw/master/img/20210601193511.png)



#### 4.2 修改函数执行方法

进入云函数后，修改执行方法为：`MainSignIn.main`

<img src="https://gitee.com/ahaox/images-picgo/raw/master/img/20210601193822.png" alt="image-20210601193822433" style="zoom: 67%;" />

点击部署，部署成功后再测试

![image-20210601193943990](https://gitee.com/ahaox/images-picgo/raw/master/img/20210601193944.png)

#### 4.3 设置定时

签到定时的设置是根据 在 3.4时设置的预约时间段的开始时间来设置的，

比如：我预约的时间段为每天 08:20 - 14:20,    14:25 - 20:25

则这里需要创建两个触发器：

第一个时间段 Cron表达式分别为： `0 16 8 * * * *` （表示每天8点16分开始执行签到服务，也就是比第一个时间段的开始时间提起4分钟进行签到）

第二个时间段 Cron表达式分别为： `0 21 14 * * * *` （表示每天14点21分开始执行签到服务，也就是比第二个时间段的开始时间提起4分钟进行签到）

![image-20210601200014142](https://gitee.com/ahaox/images-picgo/raw/master/img/20210601200014.png)

<img src="https://gitee.com/ahaox/images-picgo/raw/master/img/20210601200931.png" alt="image-20210601200931096" style="zoom:50%;" />

### 5. 签退服务

#### 5.1 克隆项目

直接复制 ==座位预约服务云函数== `CDU-Lib-Robot-Reserve` ,   把函数名称更改为：`CDU-Lib-Robot-SignOut` 

![image-20210601194934489](https://gitee.com/ahaox/images-picgo/raw/master/img/20210601194934.png)

#### 5.2 修改函数执行方法

进入云函数后，修改执行方法为：`MainSignOut.main`

![image-20210601195253055](https://gitee.com/ahaox/images-picgo/raw/master/img/20210601195253.png)

点击部署，部署成功后再测试

![image-20210601195334718](https://gitee.com/ahaox/images-picgo/raw/master/img/20210601195334.png)

#### 5.3 设置定时

设置方式和签到服务一样，但是时间是根据结束时间来设定的。

比如：我预约的时间段为每天 08:20 - 14:20,    14:25 - 20:25

则这里需要创建两个触发器：

第一个时间段 Cron表达式分别为： `0 16 14 * * * *` （表示每天14点16分开始执行签退服务，也就是比第二个时间段的结束时间提起4分钟进行签退）

第二个时间段 Cron表达式分别为： `0 21 20 * * * *` （表示每天20点21分开始执行签退服务，也就是比第二个时间段的结束时间提起4分钟进行签退）

<img src="https://gitee.com/ahaox/images-picgo/raw/master/img/20210601201111.png" alt="image-20210601201111037" style="zoom:50%;" />



## 四、打赏作者

![pay](https://cdn.jsdelivr.net/gh/ahaox/pictures/image20210208232946.png "在这里输入图片标题")

 **金额不论大小, 一分也是爱。** 

