from selenium import webdriver
import chromedriver_binary
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome import service as fs
import time
import requests  # bs ファイルデータダウンロード
from bs4 import BeautifulSoup
import re


#ハローワークインターネットサービスのURL
url = "https://www.hellowork.mhlw.go.jp/"

#chromeDriverを任意の場所に保存、DRIVER_PATHに設定
CHROMEDRIVER = "C:/Users/user/.atom/HW/Chromedriver.exe"
chrome_service = fs.Service(executable_path=CHROMEDRIVER)
browser = webdriver.Chrome(service=chrome_service)
browser.get(url)
time.sleep(2)

#求人情報をクリック
browser.find_element_by_css_selector(".button.blue.main.retrieval_icn").click()
time.sleep(2)

#年齢入力
browser.find_element_by_xpath("//*[@id='ID_nenreiInput']").send_keys("24")
time.sleep(2)

#年齢不問を除く
browser.find_element_by_id("ID_LnenreiCKBox2").click()
time.sleep(2)

#大阪府内で探す
element = browser.find_element_by_id("ID_tDFK1CmbBox")
Select(element).select_by_value("27")  # 大阪府
time.sleep(2)

#市区町村を選ぶために選択をクリック
button = browser.find_element_by_id("ID_Btn")
button.click()
time.sleep(2)

#市区町村のドロップダウンリストを選択
element = browser.find_element_by_id("ID_rank1CodeMulti")

# 【西日本】市区町村名コード(5桁・6桁)一覧（更新：2019.9.15）r
# http://www13.plala.or.jp/bigdata/municipal_code_2.html
#市区町村コードを基に、５つまで市区町村名を選択
#Select(element).select_by_value("")
Select(element).select_by_value("27102")  # 都島区
Select(element).select_by_value("27103")  # 福島区
Select(element).select_by_value("27218")  # 大東市
time.sleep(2)

#OKをクリック
browser.find_element_by_id("ID_ok").click()
time.sleep(2)

#職業分類の選択をクリック
buttons = browser.find_elements_by_css_selector("input.button")
buttons[7].click()
time.sleep(2)

#職業分類のドロップダウンリストを選択
element1 = browser.find_element_by_id("ID_rank00Code")

#B 専門的・技術的職業を選択
Select(element1).select_by_value("B")
time.sleep(2)

#下位をクリック
browser.find_element_by_id("ID_down").click()
time.sleep(2)

#下位のドロップダウンリストを選択
element2 = browser.find_element_by_id("ID_rank00Code")

#10 情報処理・通信技術者を選択
Select(element2).select_by_value("10")
time.sleep(2)

#下位をクリック
browser.find_element_by_id("ID_down").click()
time.sleep(2)

#下位のドロップダウンリストを選択
element3 = browser.find_element_by_id("ID_rank00Code")

#ソフトウェア開発技術者を選択
Select(element3).select_by_value("104")
time.sleep(2)

#下位をクリック
browser.find_element_by_id("ID_down").click()
time.sleep(2)

#下位のドロップダウンリストを選択
element4 = browser.find_element_by_id("ID_rank00Code")

#気になる職業を選択
Select(element4).select_by_value("10401")  # WEBオープン系
Select(element4).select_by_value("10402")  # 組み込み・制御系
Select(element4).select_by_value("10403")  # 汎用機系
Select(element4).select_by_value("10404")  # プログラマー
time.sleep(2)

#決定をクリック
browser.find_element_by_id("ID_ok").click()
time.sleep(2)

#雇用形態を選択
browser.find_element_by_xpath("//*[@id='ID_koyoFltmCKBox1']").click()
time.sleep(2)

#詳細検索条件をクリック
browser.find_element_by_id("ID_searchShosaiBtn").click()
time.sleep(2)

#賞与アリをクリック
browser.find_element_by_xpath("//*[@id='ID_shoyoAriCKBox1']").click()
time.sleep(2)

#派遣・請負を含まないを選択
browser.find_element_by_id("ID_LhakenUkeoinCKBox3").click()
time.sleep(2)

#学歴不問をクリック
browser.find_element_by_id("ID_grkiFumonCKBox").click()
time.sleep(2)

#OKをクリック
browser.find_element_by_xpath("//*[@id='ID_saveCondBtn']").click()
time.sleep(2)

#検索をクリック
browser.find_element_by_id("ID_searchBtn").click()
time.sleep(2)

#表示件数ドロップダウンリストをクリック
element5 = browser.find_element_by_id("ID_fwListNaviDispTop")

#５０件を選択
Select(element5).select_by_value("50")
time.sleep(2)

#今見ているページをBeautifulSopeで解析
soup = BeautifulSoup(browser.page_source, "html.parser")

#求人のテーブルを検索
jobs = soup.find_all("table", attrs={"class": "kyujin"})

#検索結果を格納する"message"を初期化
message = ""

# 「職種」「月給」「勤務地」「仕事の内容」を取得する
for i, job in enumerate(jobs):
    job_name = str(job.find("td", attrs={"class": "m13"}).text.strip())
    salary_tags = job.find_all("tr", attrs={"class": "border_new"})[
                               5].select(".disp_inline_block")
    for t, salary_tag in enumerate(salary_tags):
        job_salary = salary_tag.text
        job_description = job.find(
            string='仕事の内容').parent.find_next_sibling().text.replace('\n', '')
        job_location = job.find(
            string='就業場所').parent.find_next_sibling().text.replace('\n', '')

        message = message + \
            "■{0} （ {1} ）{2} \n□{3}\n".format(
                job_name, job_salary, job_description, job_location)
# 検索結果の出力
print(message)
browser.close()
