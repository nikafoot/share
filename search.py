
### 検索ツールサンプル
### これをベースに課題の内容を追記してください

import csv

csv_path = 'program1.csv'

# 検索ソース
source=["ねずこ","たんじろう","きょうじゅろう","ぎゆう","げんや","かなお","ぜんいつ"]

with open(csv_path,'w') as csv_file:
    csv_file.write(','.join(source))

with open(csv_path,'r') as f:
    l=f.readlines()
    print(l)


def search():
    word =input("鬼滅の登場人物の名前を入力してください >>> ")
    
    ### ここに検索ロジックを書く
    if word in l:
        print("{}が見つかりました".format(word))
    
    else:
        print("{}が見つかりませんでした".format(word))
        l.append(word)
        print(l)

if __name__ == "__main__":
    search()

with open(csv_path,'w') as csv_file:
    csv_file.write(','.join(l))
