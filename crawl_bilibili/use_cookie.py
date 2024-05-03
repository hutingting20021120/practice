"""
@filename:use_cookie.py
@author:Hu Tingting
@time:2024-04-25

"""
# -*- coding: utf-8 -*-
import time
import json  # 导入json模块
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

options = Options()
# options.add_argument("--headless")  # 不打开浏览器界面，以节省时间
browser = webdriver.Chrome(options=options)

# 先建立连接, 随后才可以可修改cookie
browser.get('https://www.bilibili.com/')
browser.maximize_window()
# 删除这次登录时，浏览器自动储存到本地的cookie
browser.delete_all_cookies()

# 读取之前已经储存到本地的cookie
cookies_filename = './data/my_cookies.json'
cookies_file = open(cookies_filename, 'r', encoding='utf-8')
cookies_list = json.loads(cookies_file.read())
print(cookies_list)

for cookie in cookies_list:  # 把cookie添加到本次连接
    browser.add_cookie(cookie)

# 再次访问网站，由于cookie的作用，从而实现免登陆访问
browser.get("https://www.bilibili.com/")
time.sleep(3)

# 将页面保存为图片，便于查看是否登录成功
browser.save_screenshot("./output/bilibili_login.png")



time.sleep(6)
browser.quit()
