## 1 変数の使い方
name1 = "ねずこ"
#name2 = "ぜんいつ"
name2 = "むざん"

#print(name1+'と'+ name2 + "は仲間です")

## 2　if文の使い方
"""
if name2=="むざん":
    print("仲間ではありません")
else:
    pass
"""

## 3 配列の使い方
names1=["たんじろう","ぎゆう","ねずこ"]
names2=["むざん","るい","あかざ"]
names1.append("ぜんいつ")

## for文の使い方
"""
for name in names:
    print(name)
"""


## 関数の使い方
def kimetu(words):
    for word in words:
        if word=="ねずこ":
            print("ねずこは含まれます")
        elif word == "むざん":
            print("むざんが含まれています")
        

kimetu(names1)