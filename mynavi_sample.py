import os
from selenium.webdriver import Chrome, ChromeOptions
#210609
from selenium.webdriver.support.ui import WebDriverWait
#
import time
import pandas as pd


#後日追記した部分Beautifulsoup４をインストールしてimport
from bs4 import BeautifulSoup
import urllib.request as req

from selenium.webdriver.chrome.webdriver import WebDriver


# Chromeを起動する関数


def set_driver(driver_path, headless_flg):
    # Chromeドライバーの読み込み
    options = ChromeOptions()
    #seleniumを安定化させるための関数（onenoteを参照)
    # ヘッドレスモード（画面非表示モード）の設定
    if headless_flg == True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    # options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    # シークレットモードの設定を付与
    options.add_argument('--incognito')
    # ChromeのWebDriverオブジェクトを作成する。
    return Chrome(executable_path=os.getcwd() + "/" + driver_path, options=options)

def find_table_target_word(th_elms, td_elms, target:str):
    #tableのthからtargetの文字列を探し一致する行のtdを返す
    for th_elm, td_elm in zip(th_elms,td_elms):
        if th_elm.text == target:
            return td_elm.text
# main処理


def main():
    search_keyword = "高収入"
    # driverを起動
    if os.name == 'nt': #Windows
        driver = set_driver("chromedriver.exe", False)
    elif os.name == 'posix': #Mac
        driver = set_driver("chromedriver", False)
    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)

    # 検索窓に入力
    driver.find_element_by_class_name(
        "topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()
    
    while True:
        time.sleep(5)
        try:
        # ポップアップを閉じる
            driver.execute_script('document.querySelector(".karte-close").click()')
            time.sleep(5)
        # ポップアップを閉じる
            driver.execute_script('document.querySelector(".karte-close").click()')
        except:
            pass
        #現在のURLを取得
        url = driver.current_url
        #Beautifulsoupを利用して、htmlの解析を行う
        html =req.urlopen(url)
        soup = BeautifulSoup(html,'html.parser')

        # ページ終了まで繰り返し取得
        exp_name_list           = []
        exp_first_year_fee_list = []
        exp_locate_list         = []
        # 検索結果の１ページ目の会社名と初年度年収を取得
        name_list = soup.find_all('h3', attrs={'class': "cassetteRecruit__name"})
        table_list = soup.find_all('div', attrs={'class': "cassetteRecruit__main"})
    
    
        # 1ページ分繰り返し
        for name, table in zip(name_list, table_list):   
            #｜を探して、位置をｓに保存
            name = name.text
            s = name.find("|")
        
            #初年度の年収をtableから探す
            first_year_fee = find_table_target_word(table.find_all("th"), table.find_all("td"), "初年度年収")
        
            #勤務地をtableから探す
            locate = find_table_target_word(table.find_all("th"), table.find_all("td"), "勤務地")

            #取得した項目をリストに格納する
            exp_name_list.append(name[:s])
            exp_first_year_fee_list.append(first_year_fee)
            exp_locate_list.append(locate)

        print(exp_name_list, exp_first_year_fee_list, exp_locate_list)
        #print(exp_first_year_fee_list)

        #次のページへ移動
        time.sleep(10)
        next_page = driver.find_element_by_class_name("iconFont--arrowLeft")
        if bool(next_page) == True:
            next_page.click()
            continue
        else :
            break

# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()