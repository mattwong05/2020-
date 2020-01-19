from selenium import webdriver
import requests
import time
import os
import re


# test
work_path = os.getcwd()
print(work_path)
answer_path = os.path.join(work_path, "answer.txt")
print("答案位置:", answer_path)
ans_file = open(answer_path, mode="w", encoding="utf-8")
print("{")
ans_file.write("{\n")


# init
url = "http://59.110.136.181:8095/"
class_name = ["语文", "数学", "英语", "物理", "化学", "生物"]
sleep_time = 1.5
browser = webdriver.Chrome()
browser.set_window_size(400, 1400)
browser.get(url)

# 登录界面
input_id = browser.find_element_by_xpath("//*[@id=\"txt_loginname\"]")
input_id.send_keys("182122")
browser.find_element_by_xpath("//*[@id=\"btnLogin\"]").click()

# browser.close()

# 学科选择界面
browser.get(browser.current_url)
time.sleep(sleep_time)


# 依次进入每个学科
for i in range(4, 6):
    browser.find_element_by_xpath(f"/html/body/div[2]/div/div/div/div[{i+1}]/a").click()
    # print(f"进入{class_name[i]}学科！")
    time.sleep(sleep_time)

    # 获取学科内含多少张卷子
    # 先进入一次学科
    browser.find_element_by_id("aLiNianLX").click()
    time.sleep(sleep_time)
    pages = browser.find_elements_by_xpath("/html/body/div[2]/div/div/div/div/a")
    # 返回学科页
    browser.find_element_by_xpath("/html/body/div[1]/a").click()
    time.sleep(sleep_time)

    # 依次进入每个试卷
    for j in range(len(pages)):
        if i == 4 and j in range(11):
            continue
        browser.find_element_by_id("aLiNianLX").click()
        # print("进入题目列表页！")
        time.sleep(sleep_time)
        browser.find_element_by_xpath(f"/html/body/div[2]/div/div/div/div[{j + 1}]/a").click()
        # print(f"进入第{j+1}张试卷页！")
        time.sleep(sleep_time * 2)
        # 获取题目数量
        question_num = int(str(browser.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]").text).split('/')[1])
        # print("本套试卷共有", question_num, "道题目")
        for k in range(question_num):
            browser.find_element_by_xpath(f"/html/body/div[1]/div[2]/div/div/div[{k+1}]/div/div[1]/div/div[3]/a[1]/span").click()
            # browser.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div[3]/div/div[1]/div/div[3]/a[1]/span")
            # print(f"完成第{k+1}题, 选择{'A'}")
            time.sleep(sleep_time)
        # 对于每一道题, 本次全部选C，获取正确答案
        # 交卷
        browser.find_element_by_xpath("/html/body/div[1]/div[3]/a[4]").click()
        # print("交卷！！！")
        time.sleep(sleep_time)
        browser.find_element_by_xpath("/html/body/div[5]/div[7]/div/button").click()
        # print("确认交卷！！！")
        time.sleep(sleep_time*2.5)

        # 获取答案
        browser.find_element_by_xpath("/html/body/div[4]/a[1]").click()
        # print("获取全部解析！！！")
        time.sleep(sleep_time * 3)

        # 获取答案的实际地址
        source = str(browser.page_source)
        ans_url = url + re.findall(r'url:(.+?),', source)[-1].split('\"')[1]
        ans_url = re.sub(r'&amp;', '&', ans_url)
        # print("找到实际答案地址:", ans_url)
        # 打开答案实际地址
        ans_list = re.findall(r'\\\"ANSWER\\\":\\\"(.+?)\\\"', requests.get(ans_url).text)
        print(f"\t\'{class_name[i]}第{j + 1}套试卷\': " + str(ans_list) + ",")
        ans_file.write(f"\t\'{class_name[i]}第{j + 1}套试卷\': " + str(ans_list) + ",\n")
        time.sleep(sleep_time * 5)

        # 返回学科页
        browser.find_element_by_xpath("/html/body/div[1]/div[1]/a").click()
        # print("返回学科页！")
        time.sleep(sleep_time * 1.5)

    browser.find_element_by_xpath(f"/html/body/div/div[3]/div[3]").click()
    # print("返回学科选择页！")

    time.sleep(sleep_time)

ans_file.write("}\n")
print("}")
ans_file.close()
browser.close()

