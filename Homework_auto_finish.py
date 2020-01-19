from selenium import webdriver
import time
from retrying import retry

# ans_sheet
ans_sheet = {
    '语文第1套试卷': ['C', 'D', 'D', 'D', 'B', 'D', 'A', 'C', 'A', 'B', 'A', 'A', 'D', 'B', 'C'],
    '语文第2套试卷': ['D', 'C', 'A', 'D', 'B', 'B', 'C', 'B', 'D', 'B', 'D', 'C', 'D', 'B', 'C'],
    '语文第3套试卷': ['B', 'C', 'B', 'D', 'D', 'C', 'D', 'B', 'A', 'A', 'D', 'A', 'A', 'C', 'B'],
    '语文第4套试卷': ['D', 'A', 'B', 'B', 'A', 'D', 'A', 'B', 'A', 'D', 'C', 'D', 'A', 'B', 'B'],
    '语文第5套试卷': ['A', 'C', 'D', 'D', 'B', 'B', 'C', 'C', 'A', 'C', 'D', 'A', 'C', 'D', 'B'],
    '语文第6套试卷': ['C', 'A', 'C', 'A', 'C', 'B', 'B', 'C', 'B', 'C', 'B', 'C', 'A', 'A', 'D'],
    '语文第7套试卷': ['D', 'D', 'B', 'C', 'D', 'B', 'D', 'C', 'C', 'A', 'D', 'B', 'C', 'C', 'D'],
    '语文第8套试卷': ['D', 'A', 'A', 'C', 'A', 'B', 'C', 'D', 'A', 'B', 'B', 'C', 'B', 'C', 'C'],
    '语文第9套试卷': ['D', 'A', 'A', 'D', 'C', 'C', 'D', 'B', 'D', 'B', 'A', 'B', 'A', 'C', 'A'],
    '语文第10套试卷': ['B', 'A', 'A', 'D', 'B', 'B', 'B', 'D', 'A', 'A', 'B', 'C', 'C', 'D', 'A'],
    '语文第11套试卷': ['D', 'C', 'A', 'C', 'A', 'C', 'B', 'B', 'C', 'A', 'A', 'D', 'D', 'D', 'D'],
    '语文第12套试卷': ['C', 'D', 'D', 'D', 'B', 'D', 'A', 'C', 'B', 'A', 'C', 'A', 'A', 'D', 'D'],
    '语文第13套试卷': ['C', 'C', 'A', 'D', 'B', 'B', 'C', 'B', 'D', 'D', 'A', 'B', 'A', 'C', 'D'],
    '语文第14套试卷': ['C', 'A', 'C', 'A', 'C', 'D', 'D', 'B', 'C', 'D', 'D', 'A', 'A', 'C', 'A'],
    '语文第15套试卷': ['A', 'B', 'A', 'C', 'A', 'B', 'B', 'D', 'A', 'A', 'D', 'C', 'A', 'C', 'A'],
    '数学第1套试卷': ['A', 'B', 'A', 'B', 'B', 'C', 'D', 'B'],
    '数学第2套试卷': ['D', 'D', 'D', 'B', 'A', 'A', 'B', 'A'],
    '数学第3套试卷': ['C', 'D', 'C', 'A', 'D', 'D', 'A', 'B'],
    '数学第4套试卷': ['C', 'A', 'C', 'C', 'C', 'A', 'D', 'B'],
    '数学第5套试卷': ['C', 'B', 'A', 'B', 'C', 'A', 'C', 'D'],
    '数学第6套试卷': ['C', 'A', 'A', 'B', 'B', 'B', 'C', 'B'],
    '数学第7套试卷': ['C', 'D', 'B', 'C', 'C', 'D', 'C', 'B'],
    '数学第8套试卷': ['C', 'B', 'D', 'A', 'A', 'D', 'A', 'A'],
    '数学第9套试卷': ['A', 'B', 'B', 'D', 'D', 'B', 'C', 'C'],
    '数学第10套试卷': ['C', 'D', 'B', 'A', 'A', 'A', 'D', 'B'],
    '数学第11套试卷': ['B', 'C', 'A', 'D', 'C', 'C', 'A', 'B'],
    '数学第12套试卷': ['B', 'C', 'A', 'B', 'C', 'A', 'C', 'C'],
    '数学第13套试卷': ['C', 'A', 'C', 'B', 'B', 'A', 'C', 'A'],
    '数学第14套试卷': ['D', 'B', 'B', 'B', 'B', 'B', 'C', 'C'],
    '数学第15套试卷': ['B', 'C', 'D', 'A', 'A', 'A', 'D', 'C'],
    '英语第1套试卷': ['A', 'B', 'A', 'B', 'B', 'D', 'D', 'B', 'C', 'B', 'A', 'C', 'B', 'B', 'D', 'C', 'B', 'C', 'C', 'D'],
    '英语第2套试卷': ['D', 'B', 'D', 'D', 'B', 'C', 'D', 'B', 'A', 'A', 'A', 'D', 'A', 'C', 'D', 'B', 'B', 'A', 'A', 'A'],
    '英语第3套试卷': ['B', 'A', 'C', 'B', 'B', 'A', 'A', 'C', 'C', 'B', 'A', 'D', 'D', 'A', 'C', 'B', 'A', 'D', 'D', 'C'],
    '英语第4套试卷': ['C', 'A', 'C', 'C', 'D', 'C', 'A', 'A', 'C', 'A', 'B', 'B', 'A', 'D', 'B', 'D', 'D', 'B', 'D', 'D'],
    '英语第5套试卷': ['A', 'B', 'B', 'D', 'A', 'C', 'D', 'C', 'A', 'B', 'D', 'A', 'D', 'C', 'A', 'B', 'A', 'D', 'C', 'D'],
    '英语第6套试卷': ['D', 'B', 'A', 'B', 'C', 'B', 'C', 'B', 'B', 'A', 'B', 'D', 'C', 'C', 'C', 'B', 'A', 'C', 'A', 'C'],
    '英语第7套试卷': ['C', 'D', 'A', 'C', 'D', 'A', 'B', 'C', 'D', 'C', 'D', 'A', 'A', 'A', 'D', 'D', 'A', 'C', 'B', 'B'],
    '英语第8套试卷': ['B', 'A', 'A', 'B', 'B', 'D', 'C', 'D', 'C', 'B', 'D', 'D', 'A', 'C', 'C', 'C', 'C', 'A', 'D', 'A'],
    '英语第9套试卷': ['A', 'D', 'B', 'A', 'D', 'C', 'B', 'D', 'D', 'B', 'D', 'A', 'A', 'A', 'B', 'D', 'D', 'B', 'D', 'C'],
    '英语第10套试卷': ['A', 'B', 'C', 'B', 'C', 'C', 'D', 'C', 'D', 'C', 'D', 'D', 'B', 'B', 'D', 'A', 'A', 'B', 'C', 'D'],
    '英语第11套试卷': ['C', 'D', 'A', 'A', 'D', 'C', 'C', 'A', 'D', 'B', 'D', 'A', 'D', 'B', 'C', 'A', 'C', 'D', 'A', 'D'],
    '英语第12套试卷': ['A', 'B', 'C', 'D', 'B', 'D', 'C', 'A', 'B', 'D', 'A', 'B', 'C', 'D', 'B', 'A', 'D', 'A', 'C', 'D'],
    '英语第13套试卷': ['B', 'D', 'D', 'A', 'D', 'B', 'D', 'D', 'B', 'A', 'D', 'A', 'B', 'D', 'B', 'B', 'A', 'A', 'A', 'C'],
    '英语第14套试卷': ['A', 'B', 'B', 'A', 'B', 'C', 'A', 'C', 'D', 'B', 'C', 'A', 'C', 'D', 'B', 'B', 'A', 'A', 'C', 'B'],
    '英语第15套试卷': ['A', 'D', 'A', 'C', 'D', 'B', 'B', 'B', 'A', 'D', 'D', 'B', 'D', 'B', 'D', 'A', 'A', 'A', 'A', 'B'],
    '物理第1套试卷': ['C', 'C', 'C', 'B', 'B'],
    '物理第2套试卷': ['C', 'A', 'C', 'B', 'B'],
    '物理第3套试卷': ['A', 'A', 'A', 'B', 'D'],
    '物理第4套试卷': ['A', 'C', 'D', 'B', 'A'],
    '物理第5套试卷': ['A', 'B', 'D', 'A', 'C'],
    '物理第6套试卷': ['C', 'B', 'D', 'A', 'A'],
    '物理第7套试卷': ['C', 'C', 'D', 'D', 'A'],
    '物理第8套试卷': ['B', 'A', 'D', 'D', 'C'],
    '物理第9套试卷': ['A', 'B', 'C', 'B', 'C'],
    '物理第10套试卷': ['D', 'B', 'D', 'D', 'C'],
    '物理第11套试卷': ['D', 'A', 'C', 'D', 'B'],
    '物理第12套试卷': ['D', 'C', 'D', 'B', 'B'],
    '物理第13套试卷': ['C', 'B', 'C', 'B', 'B'],
    '物理第14套试卷': ['D', 'C', 'B', 'B', 'C'],
    '物理第15套试卷': ['A', 'C', 'C', 'A', 'D'],
    '化学第2套试卷': ['C', 'C', 'B', 'C', 'D', 'A', 'D', 'A', 'D', 'C'],
    '化学第3套试卷': ['B', 'C', 'B', 'C', 'B', 'B', 'B', 'B', 'C', 'B'],
    '化学第4套试卷': ['C', 'B', 'A', 'D', 'B', 'C', 'A', 'C', 'A', 'B'],
    '化学第5套试卷': ['C', 'B', 'A', 'B', 'D', 'A', 'A', 'A', 'B', 'A'],
    '化学第6套试卷': ['B', 'B', 'D', 'D', 'B', 'C', 'B', 'A', 'D', 'A'],
    '化学第7套试卷': ['A', 'D', 'C', 'C', 'C', 'C', 'B', 'D', 'A', 'B'],
    '化学第8套试卷': ['B', 'C', 'B', 'D', 'A', 'C', 'C', 'C', 'B', 'D'],
    '化学第9套试卷': ['C', 'C', 'D', 'D', 'A', 'C', 'D', 'A', 'C', 'C'],
    '化学第10套试卷': ['D', 'D', 'D', 'C', 'B', 'D', 'C', 'B', 'B', 'C'],
    '化学第11套试卷': ['B', 'B', 'C', 'B', 'C', 'B', 'C', 'D', 'D', 'A'],
    '化学第12套试卷': ['C', 'D', 'C', 'C', 'B', 'D', 'A', 'D', 'C', 'C'],
    '化学第13套试卷': ['D', 'C', 'C', 'C', 'C', 'A', 'D', 'C', 'D', 'B'],
    '化学第14套试卷': ['B', 'C', 'A', 'C', 'C', 'C', 'A', 'D', 'B', 'C'],
    '化学第15套试卷': ['D', 'D', 'D', 'C', 'B', 'A', 'D', 'A', 'C', 'C'],
    '化学第16套试卷': ['A', 'D', 'D', 'C', 'D', 'D', 'D', 'B', 'C', 'C'],
    '生物第1套试卷': ['D', 'D', 'C', 'C', 'A', 'A', 'C', 'B', 'A', 'C', 'A', 'B', 'B', 'B', 'B'],
    '生物第2套试卷': ['D', 'A', 'C', 'A', 'A', 'C', 'B', 'A', 'D', 'C', 'A', 'A', 'A', 'A', 'C'],
    '生物第3套试卷': ['A', 'C', 'A', 'A', 'A', 'B', 'D', 'B', 'C', 'B', 'A', 'D', 'B', 'C', 'A'],
    '生物第4套试卷': ['D', 'C', 'A', 'C', 'A', 'A', 'C', 'C', 'D', 'C', 'C', 'D', 'B', 'C', 'A'],
    '生物第5套试卷': ['C', 'D', 'D', 'B', 'A', 'B', 'C', 'B', 'C', 'A', 'D', 'B', 'C', 'B', 'D'],
    '生物第6套试卷': ['C', 'B', 'A', 'B', 'D', 'B', 'D', 'C', 'C', 'C', 'B', 'D', 'B', 'C', 'D'],
    '生物第7套试卷': ['B', 'C', 'C', 'A', 'B', 'A', 'C', 'A', 'A', 'A', 'C', 'B', 'B', 'C', 'A'],
    '生物第8套试卷': ['C', 'B', 'A', 'C', 'B', 'A', 'A', 'B', 'B', 'A', 'B', 'A', 'A', 'A', 'B'],
    '生物第9套试卷': ['D', 'B', 'D', 'B', 'D', 'D', 'D', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B'],
    '生物第10套试卷': ['A', 'C', 'D', 'D', 'D', 'A', 'C', 'B', 'C', 'C', 'B', 'B', 'B', 'D', 'C'],
    '生物第11套试卷': ['D', 'A', 'B', 'D', 'A', 'B', 'D', 'D', 'D', 'C', 'C', 'B', 'D', 'C', 'B'],
    '生物第12套试卷': ['D', 'A', 'B', 'D', 'A', 'D', 'D', 'D', 'C', 'D', 'A', 'A', 'D', 'A', 'C'],
    '生物第13套试卷': ['D', 'D', 'D', 'D', 'C', 'C', 'A', 'D', 'B', 'D', 'D', 'B', 'B', 'D', 'C'],
    '生物第14套试卷': ['c', 'A', 'B', 'D', 'C', 'D', 'A', 'A', 'B', 'D', 'D', 'C', 'A', 'D', 'C'],
    '生物第15套试卷': ['A', 'B', 'A', 'D', 'A', 'D', 'B', 'A', 'C', 'D', 'B', 'C', 'D', 'A', 'D'],
    '生物第16套试卷': ['D', 'A', 'D', 'A', 'A', 'D', 'C', 'D', 'B', 'D', 'B', 'A', 'B', 'A', 'B'],
}


# init
url = "http://59.110.136.181:8095/"
class_name = ["语文", "数学", "英语", "物理", "化学", "生物"]
sleep_time = 1
browser = webdriver.Chrome()
browser.set_window_size(400, 1400)
browser.get(url)


# 多次get_element直到好用
@retry(wait_fixed=2)
def click_element(x: str):
    browser.find_element_by_xpath(x).click()


# 登录界面
input_id = browser.find_element_by_xpath("//*[@id=\"txt_loginname\"]")
input_id.send_keys("182122")
click_element("//*[@id=\"btnLogin\"]")


# 学科选择界面
browser.get(browser.current_url)
time.sleep(sleep_time)


# 依次进入每个学科
for i in range(6):
    click_element(f"/html/body/div[2]/div/div/div/div[{i + 1}]/a")
    print(f"进入{class_name[i]}学科！")
    time.sleep(sleep_time)

    # 获取学科内含多少张卷子
    # 先进入一次学科
    click_element("/html/body/div/div[3]/div[1]")
    time.sleep(sleep_time)
    pages = browser.find_elements_by_xpath("/html/body/div[2]/div/div/div/div/a")
    # 返回学科页
    click_element("/html/body/div[1]/a")
    time.sleep(sleep_time)

    # 依次进入每个试卷
    for j in range(len(pages)):
        if i == 4 and j == 0:
            continue
        click_element("/html/body/div/div[3]/div[1]")
        print("进入题目列表页！")
        time.sleep(sleep_time * 1.25)
        click_element(f"/html/body/div[2]/div/div/div/div[{j + 1}]/a")
        print(f"进入第{j+1}张试卷页！")
        time.sleep(sleep_time * 5)

        # 获取题目数量
        question_num = int(str(browser.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]").text).split('/')[1])
        print("本套试卷共有", question_num, "道题目")

        # 答题
        for k in range(question_num):
            # 获取答案
            ans_it = ord(ans_sheet[f"{class_name[i]}第{j+1}套试卷"][k]) - ord('A')
            click_element(
                    f"/html/body/div[1]/div[2]/div/div/div[{k + 1}]/div/div[1]/div/div[3]/a[{ans_it + 1}]/span")
            print(f"完成第{k+1}题, 选择{chr(ord('A')+ans_it)}")
            time.sleep(sleep_time * 1.5)

        # 交卷
        click_element("/html/body/div[1]/div[3]/a[4]")
        print("交卷！！！")
        time.sleep(sleep_time)
        click_element("/html/body/div[5]/div[7]/div/button")
        print("确认交卷！！！")
        time.sleep(sleep_time * 2.5)

        # 获取全部解析
        click_element("/html/body/div[4]/a[1]")
        print("获取全部解析！！！")
        time.sleep(sleep_time * 5)

        # 返回学科页
        click_element("/html/body/div[1]/div[1]/a")
        print("返回学科页！")
        time.sleep(sleep_time * 1.5)

    click_element(f"/html/body/div/div[3]/div[3]")
    print("返回学科选择页！")
    time.sleep(sleep_time * 1.5)

browser.close()
print("圆满完成！！！")
