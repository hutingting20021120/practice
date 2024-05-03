"""
@filename:testinfo.py
@author:Hu Tingting
@time:2024-05-03

"""
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time
import csv
import json

# 启动 Chrome 服务
chrome_path = r'C:\Program Files\Python312\Scripts\chromedriver.exe'  # 你的 chromedriver 路径
chrome_service = Service(chrome_path)
chrome_service.start()

driver = webdriver.Chrome(service=chrome_service)

# 先建立连接, 随后才可以可修改cookie
driver.get('https://www.bilibili.com/')
driver.maximize_window()
# 删除这次登录时，浏览器自动储存到本地的cookie
driver.delete_all_cookies()

# 读取之前已经储存到本地的cookie
cookies_filename = './data/my_cookies.json'
cookies_file = open(cookies_filename, 'r', encoding='utf-8')
cookies_list = json.loads(cookies_file.read())
print(cookies_list)

for cookie in cookies_list:  # 把cookie添加到本次连接
    driver.add_cookie(cookie)

# 再次访问网站，由于cookie的作用，从而实现免登陆访问
driver.get("https://www.bilibili.com/")
time.sleep(3)

# 爬取数据

link_text1 = "纪录片"
link_element1 = driver.find_element(By.LINK_TEXT, link_text1)
link_element1.click()
input('按回车')

# 获取当前所有窗口句柄
all_windows = driver.window_handles

# 切换到新窗口
new_window = all_windows[-1]  # 最后一个窗口是新打开的窗口
driver.switch_to.window(new_window)

link_text2 = "最高评分"
link_element2 = driver.find_element(By.LINK_TEXT, link_text2)
link_element2.click()
input('按回车')

with open('./output/docuinfo.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    fieldnames = ['片名', '评分', '热度', '主题', '年份', '简介', 'BV码']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    page = 1
    while page <= 5:
        # 访问列表页
        driver.get(
            f'https://www.bilibili.com/documentary/index/?from_spmid=666.9.function.0#style_id=-1&producer_id=-1&release_date=-1&season_status=-1&order=4&st=3&sort=0&page={page}')
        time.sleep(2)  # 等待页面加载完成

        # 获取当前所有窗口句柄
        all_windows = driver.window_handles

        # 切换到新窗口
        new_window = all_windows[-1]  # 最后一个窗口是新打开的窗口
        driver.switch_to.window(new_window)

        # 等待所有链接加载完成
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.cover-wrapper')))

        bangumi_links = driver.find_elements(By.CSS_SELECTOR, 'a.cover-wrapper')

        # 存储链接的href属性值
        hrefs = [link.get_attribute('href') for link in bangumi_links]

        # 遍历每个链接，并打开相应页面
        for href in hrefs:
            driver.get(href)
            # 获取当前所有窗口句柄
            all_windows = driver.window_handles
            # 切换到新窗口
            new_window = all_windows[-1]  # 最后一个窗口是新打开的窗口
            driver.switch_to.window(new_window)
            # 等待元素加载完成
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.mediainfo_mediaTitle__Zyiqh')))
            title = driver.find_element(By.CSS_SELECTOR, 'a.mediainfo_mediaTitle__Zyiqh').text
            score = driver.find_element(By.CSS_SELECTOR, 'div.mediainfo_score__SQ_KG').text
            Play_volume = driver.find_element(By.CSS_SELECTOR, 'div.mediainfo_mediaDesc__jjRiB').text
            theme = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div/div[2]/div/div[2]/span[1]').text
            year = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div/div[2]/div/div[2]/span[2]').text
            intro = driver.find_element(By.CSS_SELECTOR, 'p.mediainfo_content__rexOq').text
            BV = driver.find_element(By.CSS_SELECTOR, 'a.mediainfo_avLink__iyzyV').text
            print(title,score,Play_volume,theme,year,intro,BV)
            writer.writerow(
                {'片名': title, '评分': score, '热度': Play_volume, '主题': theme, '年份': year, '简介': intro,
                 'BV码': BV})

        page+=1

driver.quit()  # 关闭浏览器

