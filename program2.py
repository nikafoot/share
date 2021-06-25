import os
from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import datetime
from bs4 import BeautifulSoup
import urllib.request as req

LOG_FILE_PATH = "./log/log_{datetime}.log"
log_file_path=LOG_FILE_PATH.format(datetime=datetime.datetime.now().strftime('%Y-%m-%d-%H'))
EXP_CSV_PATH="./exp_list_{search_keyword}_{datetime}.csv"


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
    driver_path = ChromeDriverManager().install()
    return Chrome(driver_path, options=options)

#tableから指定の文字列を探し、返す関数
def find_table_target_word(th_elms, td_elms, target:str):
    #tableのthからtargetの文字列を探し一致する行のtdを返す
    for th_elm, td_elm in zip(th_elms,td_elms):
        if th_elm.text == target:
            return td_elm.text

#ログファイルおよびコンソール出力
def log(txt):
    now= datetime.datetime.now().strftime('%Y-%m-%d-%H')
    logStr = '[%s: %s] %s' % ('log',now , txt)
    #ログ出力
    with open(log_file_path, 'a', encoding='utf-8_sig') as f:
        f.write(logStr + '\n')
    print(logStr)

### main処理
def main():
    log("処理開始")
    search_keyword = input("検索したいキーワードを入力してください：")
    log("検索キーワード：".format(search_keyword))
    # driverを起動
    if os.name == 'nt': #Windows
        driver = set_driver("chromedriver.exe", False)
    elif os.name == 'posix': #Mac
        driver = set_driver("chromedriver", False)
    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)
    try:
        #ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(5)
        #ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
    except:
        pass

    # 検索窓に入力
    driver.find_element_by_class_name("topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()
    

    # ページをまたいで繰り返し取得
    exp_name_list           = []
    exp_first_year_fee_list = []
    exp_locate_list         = []
    count = 1
    success = 0
    fail = 0

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
        name_list = soup.select("h3.cassetteRecruit__name")
        table_list = soup.select("div.cassetteRecruit__main")
        
        # 1ページ分繰り返し
        for name, table in zip(name_list, table_list):   
            try:
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
                log(f"{count}件目成功 : {name[:s]}")   
                success += 1
            except Exception as e:
                log(f"{count}件目失敗 : {name[:s]}")
                log(e)
                fail+=1
            finally:
                count+=1

        #次のページへ移動
        time.sleep(5)
        try:
            driver.find_element_by_class_name("iconFont--arrowLeft").click()
        except:
            log("最終ページです。")
            break
    
    #csv出力
    dict = {'name': exp_name_list, 'payment':exp_first_year_fee_list, 'locate':exp_locate_list}
    df = pd.DataFrame(dict)
    df.to_csv(EXP_CSV_PATH, encoding='cp932')
    log(f"処理完了 成功件数: {success} 件 / 失敗件数: {fail} 件")

# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()