#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:     chenjianzhong
@contact:    530827182.com
@others:     All by Jianzhong, All rights reserved-- Created on 2019/05/18
@desc:
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# 下面是用qq邮箱发送邮件

def sendEmailFile(file_new, content, filename):
    # 设置smtplib所需的参数
    # 下面的发件人，收件人是用于邮件传输的。
    # 成功开启POP3 / SMTP服务, 在第三方客户端登录时，密码框请输入以下授权码：grbfdibcqgajbijb
    # 成功开启IMAP / SMTP服务, 在第三方客户端登录时，密码框请输入以下授权码：ganrvmfopgxobiec
    # smtpserver = 'smtp.qq.com'
    username = '530827182@qq.com'
    password = 'grbfdibcqgajbijb'
    sender = '530827182@qq.com'
    # receiver = '1160505973@qq.com'
    # 收件人为多个收件人
    receiver = ['1160505973@qq.com', 'tangn@deepblueai.com']

    subject = '----API test report--------'

    # 下面的主题，发件人，收件人，日期是显示在邮件页面上的。
    msg = MIMEMultipart('mixed')
    msg['Subject'] = subject
    msg['From'] = '530827182@qq.com <软件测试组>'
    msg['To'] = '1160505973@qq.com'
    # 收件人为多个收件人,通过join将列表转换为以;为间隔的字符串
    # msg['To'] = ";".join(receiver)

    # 文本内容
    text_content = MIMEText(content)
    msg.attach(text_content)


    # 构造附件
    # sendfile = open(r'D:\pythontest\1111.txt', 'rb').read()
    with open(file_new, 'rb') as emailfile:
        sendfile = emailfile.read()
    # sendfile = open(file_new, 'rb').read()
    text_att = MIMEText(sendfile, 'base64', 'utf-8')
    text_att["Content-Type"] = 'application/octet-stream'
    # 以下附件可以重命名成aaa.txt
    # text_att["Content-Disposition"] = 'attachment; filename="aaa.txt"'
    # 另一种实现方式---将后面的filename直接写死----可以跑通
    # text_att.add_header('Content-Disposition', 'attachment', filename='TestReport.html')
    text_att.add_header('Content-Disposition', 'attachment', filename='%s' % filename)
    msg.attach(text_att)

    # 发送邮件
    smtp = smtplib.SMTP()
    try:
        smtp.connect('smtp.qq.com')
        smtp.login(username, password)
        smtp.sendmail(sender, receiver, msg.as_string())
    except Exception as e:
        print(str(e))
        print("发送失败")
    finally:
        smtp.quit()
