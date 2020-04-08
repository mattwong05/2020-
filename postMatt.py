import json
import requests
import random
import time
import re
from retrying import retry
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common import exceptions


# config
begin_class = 0
begin_text = 0
sleep_time = 0

# random_config
random_flag = False
random_level = 0  # 一个0-1的实数,为蒙题的概率
random_base_string = "ABCD"


# init
begin_time = time.time()
url = "http://59.110.136.181:8095/"
headers = {
  'Connection': 'keep-alive',
  'Accept': 'application/json, text/javascript, */*; q=0.01',
  'X-Requested-With': 'XMLHttpRequest',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
  'Content-Type': 'application/x-www-form-urlencoded',
  'Origin': 'http://59.110.136.181:8095',
  'Accept-Encoding': 'gzip, deflate',
  'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
  'Referer': '',
  'Cookie': '',
}
chrome_option = Options()
# chrome_option.add_argument('--headless')  # 无头模式
browser = webdriver.Chrome(chrome_options=chrome_option)
browser.set_window_size(400, 1400)
browser.get(url)


# 多次get_element直到好用
@retry(wait_fixed=500)
def click_element(x: str):
    browser.find_element_by_xpath(x).click()

# 多次request
@retry(wait_fixed=500)
def get_src(target_url, target_headers):
    return requests.get(target_url, headers=target_headers)


# 获取我们所需格式的cookies以及Referer
def get_headers():
    try:
        cookie = [item["name"] + "=" + item["value"] for item in browser.get_cookies()]
        cookies_iter = ';'.join(item for item in cookie)
        headers["Cookie"] = cookies_iter  # 通过接口请求时需要cookies等信息
        headers["Referer"] = browser.current_url
    except exceptions.UnexpectedAlertPresentException:
        print("接到AlertPresent异常!")
        input("解决异常后请输入1:")
        get_headers()


# 将秒数转化为标准化的时间
def get_str_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%02d:%02d:%02d" % (h, m, s)


# 登录界面 -> (输入id以及验证码)完成登录
user_id = input("请输入学号:")
input_id = browser.find_element_by_xpath("//*[@id=\"txt_loginname\"]")
input_id.send_keys(user_id)
code_id = input("请输入验证码:")
browser.find_element_by_xpath("/html/body/form/div[3]/div[1]/div[2]/input").send_keys(code_id)
click_element("//*[@id=\"btnLogin\"]")

# 学科选择界面 -> 获取各个学科id以及学科名称
time.sleep(sleep_time)
now_url = url+f"/AppService/GetAppData.aspx?action=getsubjectlist&subjectnum=123{user_id}&studentnum=123{user_id}"
get_headers()
subjects_info = json.loads(get_src(now_url, headers).text)
class_num = int(subjects_info["TOTALROW"])
print(f"本在线测评共有{class_num}个课程")
subjects = json.loads(subjects_info["JSONDATA"])
classes = []        # 课程信息
for subject in subjects:
    class_info = {}     # 学科信息
    class_info["id"] = subject["SUBJECTNUM"]
    class_info["name"] = subject["NAME"]
    classes.append(class_info)
# print(classes)
time.sleep(sleep_time)

# 进入每个学科 -> 获取卷子总数及每张卷子的名字、编号和题目数量
for i in range(begin_class, class_num):
    click_element(f"/html/body/div[2]/div/div/div/div[{i + 1}]/a")
    print(f"进入{classes[i]['name']}学科！")
    time.sleep(sleep_time)
    # 获取卷子数量及名称
    now_url = url+f"/AppService/GetAppData.aspx?action=getagoeaxmlist&subjectnum={classes[i]['id']}&studentnum=123{user_id}"
    get_headers()
    tests_dict = json.loads(get_src(now_url, headers).text)
    test_num = int(tests_dict["TOTALROW"])
    print(f"{classes[i]['name']}学科共有{test_num}张试卷")
    tests = []
    for test in json.loads(tests_dict["JSONDATA"]):
        test_info = {}
        test_info['id'] = test["PAPERNUM"]
        test_info['name'] = test["PAPERNAME"]
        test_info['q_num'] = test["ALLCOUNT"]
        tests.append(test_info)
    # print(tests)

    # 先进入一次题目列表页
    click_element("/html/body/div/div[3]/div[1]")
    print("进入题目列表页！")
    time.sleep(sleep_time * 1.25)

    # 依次进入每个试卷 -> 获取题目信息,并拼凑好post所需内容,提交答案
    for j in range(test_num):
        if i == begin_class and j in range(begin_text):
            continue
        click_element(f"/html/body/div[2]/div/div/div/div[{j + 1}]/a")
        print(f"进入第{j+1}张试卷页！")
        print(tests[j]['name'], f"共有{tests[j]['q_num']}道题目")

#   post
        # 获取答案的实际地址
        now_url = url+f"/AppService/GetAppData.aspx?action=getquestionlist&id={tests[j]['id']}&papertype=2&subjectnum={classes[i]['id']}&studentnum=123{user_id}"
        get_headers()
        print("获取试卷信息ing")
        dataFile = json.loads(get_src(now_url, headers).text)
        print("成功获取试卷信息")
        # print(type(dataFile))
        # print(f"卷子名称为：{dataFile['RETURNVALUE']}")
        # print(f"题目数量为：{dataFile['TOTALROW']}")
        questions = json.loads(dataFile['JSONDATA'])
        # print(type(questions))
        wrong_num = 0
        post_text = "questionlist="
        for k in range(len(questions)):
            # print(f"第{k + 1}题:" + f"题目ID为{questions[k]['QUESTIONNUM']},答案为{questions[k]['ANSWER']}")
            if not k == 0:
                post_text += '%3B'
            # 这里有一道题,答案正常是"A\B\C\D",它答案是"选C。",为了这道题,我只能写一个特判
            if len(questions[k]['ANSWER']) == 1:
                # 当选择了随机标签，并且在所设定的概率内，将会随机从“A B C D”中选择一个提交
                if random_flag and random.random() <= random_level:
                    post_text += questions[k]['QUESTIONNUM'] + '%2C0%2C' + random.choice(random_base_string) + '%2C0%2C0'
                    wrong_num += 1
                else:
                    post_text += questions[k]['QUESTIONNUM'] + '%2C1%2C' + questions[k]['ANSWER'] + '%2C0%2C0'
            # 神奇的是高一有的题干脆没有答案,所以又加了一个特判
            elif len(questions[k]['ANSWER']) == 0:
                post_text += questions[k]['QUESTIONNUM'] + '%2C1%2C' + 'C' + '%2C0%2C0' # 都选C
            else:
                post_text += questions[k]['QUESTIONNUM'] + '%2C1%2C' + re.findall(r'[A-Z]', questions[k]['ANSWER'])[0] + '%2C0%2C0'
        post_text += "&usetime=" + str(random.randint(300, 600))
        get_headers()
        now_url = url+f"AppService/GetAppData.aspx?action=jiaojuan&id={tests[j]['id']}&papertype=2&subjectnum={classes[i]['id']}&studentnum=123{user_id}"
        # 错题数量报告
        if random_flag:
            print(f"本套试卷随机选错了{wrong_num}道题目!")
        # 提交
        return_code = '0'
        while return_code == '0':
            print("正在提交答卷!")
            response = json.loads(requests.request("POST", now_url, headers=headers, data=post_text).text)
            if response['RETURNMSG']:
                print("Return message = ", response['RETURNMSG'])
            return_code = response['RETURNCODE']
            print("Return code = ", return_code)
        print("已提交试卷")
        time.sleep(sleep_time * 1.5)

        # 返回学科页
        browser.back()

    browser.back()  # 返回学科页
    click_element(f"/html/body/div/div[3]/div[3]")
    print("返回学科选择页！")
    time.sleep(sleep_time * 1.5)

browser.close()
end_time = time.time()
print(f"用户{user_id}圆满完成！！！共耗时{get_str_time(end_time - begin_time)}")
