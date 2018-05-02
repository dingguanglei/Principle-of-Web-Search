# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
from prompt_toolkit import prompt
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.keys import Keys
from prompt_toolkit.filters import Condition
import requests
import sys
from bs4 import BeautifulSoup
import jieba

def login(studentID="2017140245", passwd="110831"):
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

        print('Response HTTP Status Code : {status_code}'.format(status_code=r.status_code))
        content = r.content
        soup = BeautifulSoup(content, 'lxml')
        title = soup.find('title').string
        msg = ""

        again
        if r.status_code == 200 :
            print("登陆成功！")

        for i in str(ps):
            if is_chinese(i):
                msg+=i
        print(msg)



        # print('Response HTTP Response Body : {content}'.format(content=r.content))
    except requests.exceptions.RequestException as e:
        print('HTTP Request failed')


def logout():
    # My API (2) (GET http://gw.bupt.edu.cn/F.html)
    try:
        print("Login out ...")
        r = requests.get(
            url="http://gw.bupt.edu.cn/F.html",
        )
        print('Response HTTP Status Code : {status_code}'.format(status_code=r.status_code))
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
            studentID = "2017140245"
            passwd = "110831"
        login(studentID, passwd)


if __name__ == '__main__':
    login()
    logout()
    exit(1)
    main()
