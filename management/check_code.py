# !/usr/local/bin/python
# -*- coding:utf-8 -*-
import httplib
import urllib


# import random
#
# rand_number = random.randint(1000, 9999)

def send_sms(text, mobile):
    host = "106.ihuyi.com"
    sms_send_uri = "/webservice/sms.php?method=Submit"

    # 用户名请登录用户中心->验证码、通知短信->帐户及签名设置->APIID
    account = ""
    # 密码 查看密码请登录用户中心->验证码、通知短信->帐户及签名设置->APIKEY
    password = ""

    # global rand_number

    # text = '您的验证码是：' + str(rand_number) + '。请不要把验证码泄露给其他人。'

    params = urllib.urlencode(
        {'account': account, 'password': password, 'content': text, 'mobile': mobile, 'format': 'json'})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPConnection(host, port=80, timeout=30)
    conn.request("POST", sms_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str

    # if __name__ == '__main__':
    #     mobile = '15062984159'
    #     rand_number = random.randint(1000, 9999)
    #     text = '您的验证码是：' + str(rand_number)+ '。请不要把验证码泄露给其他人。'
    #     print(send_sms(text, mobile))
    #     print(send_sms(mobile))
    #     print(rand_number)
