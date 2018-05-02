# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
from prompt_toolkit import prompt
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.keys import Keys
from prompt_toolkit.filters import Condition
import requests
import sys
from bs4 import BeautifulSoup


# import jieba

def login(studentID="", passwd=""):
    # My API (POST http://10.3.8.211/a11.htm)  http://10.3.8.211/#open
    try:
        print("Login in ...")
        r = requests.post(
            url="http://10.3.8.211/",
            data={
                "DDDDD": studentID,
                "upass": passwd,
                "0MKKey": "",
            },
        )

        # print('Response HTTP Status Code : {status_code}'.format(status_code=r.status_code))
        content = r.content
        soup = BeautifulSoup(content, 'lxml')
        title = soup.find('title').string
        if r.status_code == 200 and title == "登录成功窗":
            again_content = requests.get("http://10.3.8.211/").content
            again_soup = BeautifulSoup(again_content, 'lxml')
            script = again_soup.find("script")
            time = process(script,"time")
            flow = process(script,"flow")
            fee =process(script,"fee")
            print("登陆成功！")
            print("已使用时间：%s 已使用流量：%s 余额：%s" % (time, flow, fee))
        # print('Response HTTP Response Body : {content}'.format(content=r.content))
    except requests.exceptions.RequestException as e:
        print('HTTP Request failed')

def process(script,type):
    out =""
    if type=="time":
        time = str(script).split("=")[2].split("\\")[0].split("'")[1].strip()
        out = time + "Min"

    if type == "flow":
        flow = str(script).split("=")[3].split("\\")[0].split("'")[1].strip()
        out =str(round(int(flow)/1024,2) ) +"MByte"

    if type =="fee":
        fee = str(script).split("=")[5].split("\\")[0].split("'")[1].strip()
        out = str(int(fee)/10000)+ "RMB"
    return out
def logout():
    # My API (2) (GET http://gw.bupt.edu.cn/F.html)
    try:
        again_content = requests.get("http://10.3.8.211/").content
        again_soup = BeautifulSoup(again_content, 'lxml')
        script = again_soup.find("script")
        time = process(script, "time")
        flow = process(script, "flow")
        fee = process(script, "fee")

        print("已使用时间：%s 已使用流量：%s 余额：%s" % (time, flow, fee))
        print("Login out ...")
        r = requests.get(
            url="http://gw.bupt.edu.cn/F.html",
        )

        # print('Response HTTP Status Code : {status_code}'.format(status_code=r.status_code))
        # print('Response HTTP Response Body : {content}'.format(content=r.content))
        if r.status_code == 200:
            print("注销成功！")
    except requests.exceptions.RequestException as e:
        print('HTTP Request failed')


def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False


def main():
    if len(sys.argv) > 1:
        logout()
    else:
        studentID = input("Please Input Your Student ID:")
        hidden = [True]  # Nonlocal
        key_bindings_manager = KeyBindingManager()

        @key_bindings_manager.registry.add_binding(Keys.ControlT)
        def _(event):
            hidden[0] = not hidden[0]

        passwd = prompt('Password: ',
                        is_password=Condition(lambda cli: hidden[0]),
                        key_bindings_registry=key_bindings_manager.registry)
        if len(studentID) < 1 and len(passwd) < 1:
            studentID = ""
            passwd = ""
        login(studentID, passwd)


if __name__ == '__main__':
    main()
