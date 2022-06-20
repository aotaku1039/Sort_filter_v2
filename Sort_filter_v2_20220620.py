import os
import re
from unittest import result

os.system("cls") #コンソール画面消去


g_input_tetfus = ["", ""] #入力テト譜 0...filterURL 1...uniqueURL
output_type = 0 #出力形式



def inputTetfu():
    while True:
        input_tetfu = input()
        if input_tetfu.find("115@") != -1: #「115@」が含まれていたときだけ通す
            return input_tetfu

def inputType(): #出力形式
    while True:
        input_text = input()
        if input_text.isdecimal():
            input_num = int(input_text)
            if 0 <= input_num <= 8: #0以上8以下の数値が打ち込まれていたときだけ通す
                return input_num
            

print("※ウィンドウサイズによって出力の挙動が変わる場合があります、ウィンドウを最大化してから進めてください")
print("*Output behavior may change depending on window size, please maximize the window before proceeding.")
print("")

print("path-filterのURLを貼り付けて、Enterキーを押してください")
print("Paste the path-filter URL and press Enter.")
print("")
g_input_tetfus[0] = inputTetfu()

print("")
print("")
print("path-uniqueのURLを貼り付けて、Enterキーを押してください")
print("Paste the path-unique URL and press Enter.")
print("")
g_input_tetfus[1] = inputTetfu()

print("")
print("")
print("出力形式を0~8の数値で入力し、Enterキーを押してください")
print("Enter the output format as a number from 0 to 8 and press the Enter key.")
print("")
print("0...RAW DATA(v115@スタート)")
print("1...日本版のEdit形式(https://fumen.zui.jp/?v115@スタート)")
print("2...日本版のFullList形式(https://fumen.zui.jp/?d115@スタート)")
print("3...日本版のMiniList形式(https://fumen.zui.jp/?D115@スタート)")
print("4...日本版のView形式(https://fumen.zui.jp/?m115@スタート)")
print("5...モバイル版(https://knewjade.github.io/fumen-for-mobile/#?d=v115@スタート)")
print("6...HardDrop版のEdit形式(https://harddrop.com/fumen/?v115@スタート)")
print("7...HardDrop版のList形式(https://harddrop.com/fumen/?d115@スタート)")
print("8...HardDrop版のView形式(https://harddrop.com/fumen/?m115@スタート)")
print("")
output_type = inputType()


def getDivMod(x, y): #割り算して商と余りを返す
    return (x // y), (x % y)


def cutTetfuText(tetfu): #テト譜文字列から「?」や最初部分など、不要な部分を取り除く
    start = tetfu.find("@")
    tetfu = tetfu[start + 1 :]  #最初の不要部分を取り除く
    
    tetfu = tetfu.replace("?", "")  #「?」を取り除く
    tetfu = tetfu.replace(" ", "")  #空白を取り除く
    tetfu = re.sub("\n", "", tetfu) #改行を取り除く
    
    return tetfu




def formatText(text, tabletext): #文字を数字に変換
    cnt = 0 #足し算用
    before_cnt = 0 #足し算前の値調整
    
    for i in range(len(text)): #文字数の分だけループして足していく
        before_cnt = tabletext.find(text[i]) #単なる文字と数字の変換、64文字テーブル
        before_cnt *= (64 ** i)
        
        cnt += before_cnt
    
    return cnt


g_input_tetfus[0] = cutTetfuText(g_input_tetfus[0])
g_input_tetfus[1] = cutTetfuText(g_input_tetfus[1])


#https://knewjade.github.io/fumen-for-mobile/#?d=v115@bh5hJeAgWHAmuMeEF8lAA 例としてこのテト譜を使って、具体的に配列の1要素目の中に何が入るか説明

g_fields = [] #filterとuniqueのフィールド文字列を入れる配列　添字を2で割った商がページ数、あまりが0...filter 1...unique(1ページ単位で入る) 上の例だと「bh5hJe」までが入る
g_unique_pieceflag_comments = [] #uniqueのミノフラグとコメントデータをまとめて入れておく配列　添字そのままページ数 上の例だと「AgWHAmuMeEF8lAA」までが入る



def searchPieceflag(text): #探索範囲で最初にくるミノフラグ(AAA、AAP、AgH、AgWのどれか)の位置を取得
    i = 0
    
    while True:
        slicetext = text[i: i + 3]
        
        if  (slicetext == "AAA") or (slicetext == "AAP") or (slicetext == "AgH") or (slicetext == "AgW"):
            return i
        
        # if text[i: i+2] == "vh":
        #     print(f"{i}番目に重複あり")
        #     inputval = input()
            
        # print(i)
        
        if i > len(text):
            errormsg = input("エラーメッセージです、ミノフラグが見つかりませんでした  Error message, pieceflag not found.")
            os.exit()
        
        i += 1
    


def destructiveSlice(index, textcnt): #破壊的なslice関数
    slicetext = g_input_tetfus[index][:textcnt] #g_input_tetfus[index]からn文字取り出す
    g_input_tetfus[index] = g_input_tetfus[index][textcnt:] #取り出した分は消す
    
    return slicetext


def breakDownField(page): #フィールドを分解
    for i in range(2):
        g_fields.append("") #1ページの分解につき、2要素push(filter→unique)
    
    
    for filter0_unique1 in range(2):
        if g_input_tetfus[filter0_unique1] != "":
            pieceflag_index = searchPieceflag(g_input_tetfus[filter0_unique1]) #AAA、AAP、AgH、AgWのどれかを検索
            g_fields[page * 2 + filter0_unique1] = destructiveSlice(filter0_unique1, pieceflag_index) #そこまでを破壊的に取り出し、g_fields[]にそのまま入れる




def breakDownPieceFlagComment(page): #uniqueのミノフラグとコメントを分解
    g_unique_pieceflag_comments.append("") #1ページの分解につき、1要素push(unique)
    
    #記録するのはuniqueだけでいいが、filterも同じ手順を踏んで文字列を取り出しておかないといけない
    
    
    
    for filter0_unique1 in range(2):
        flag = destructiveSlice(filter0_unique1, 3) #まずはコメントフラグのオンオフ調べから　頭3文字を破壊的に取り出す
        
        if flag == "AAA": #AAAはAgHに、AAPはAgWにすることで　フラグ文字列を2種類だけに絞る
            flag = "AgH"
        elif flag == "AAP":
            flag = "AgW"
        
        if flag == "AgH": #コメントフラグがオフのとき
            totaltext = g_unique_pieceflag_comments[page - 1] #前のページのコメントをそのままもってくる
        else: #コメントフラグがオンのとき
            totaltext = flag #合計文字列にフラグ情報も含むので、あらかじめ入れておく
            
            textcnt_str = destructiveSlice(filter0_unique1, 2) #文字数情報の頭2文字を破壊的に取り出す
            totaltext += textcnt_str #合計文字列に入れる
            
            textcnt_int = formatText(textcnt_str, "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/") #取り出した2文字を数字変換
            textcntdiv4, textcntmod4 = getDivMod(textcnt_int, 4)#文字数を4で割って、商と余りを出す
            
            if textcntmod4 != 0: #あまりがあれば、切り上げて商に1を加える
                textcntdiv4 += 1
            
            for ii in range(textcntdiv4):
                comment_str = destructiveSlice(filter0_unique1, 5) #コメントデータ　頭5文字を破壊的に取り出す
                totaltext += comment_str #合計文字列に入れる
            
        
        g_unique_pieceflag_comments[page] = totaltext
    



page = 0

while True:
    # print(g_input_tetfus[1])
    
    if g_input_tetfus[1] == "":
        break
    
    breakDownField(page)
    breakDownPieceFlagComment(page)
    
    page += 1



def comparisonAndNewConstruction(): #比較と新構築
    
    sort_filter_v2 = "" #filter並び替えの結果を足し上げていく変数
    pagecnt = len(g_unique_pieceflag_comments) #uniqueのページ数
    
    repeat_cnt = 0 #被りパターン数カウント用
    
    element_histories = [] #足し上げるフィールドを入れていく パターンの重複確認用
    
    for i in range(pagecnt): #uniqueのページ数分だけforループを回す g_fields[奇数](unique)を見ていく用
        for ii in range(pagecnt): #こちらもuniqueのページ数分だけforループを回す g_fields[偶数](filter)を見ていく用
            if g_fields[i * 2 + 1] == g_fields[ii * 2 + 0]: #uniqueの調べているページが、filterの中にあったら
                
                if g_fields[i * 2 + 1] in element_histories: #もし、足し上げようとしたフィールドがすでに入れられているなら、何も足し上げない
                    repeat_cnt += 1 #被りパターン数カウント
                    
                else:
                    sort_filter_v2 += g_fields[i * 2 + 1] + g_unique_pieceflag_comments[i] #まだ入れられてないなら、フィールド情報、ミノフラグとコメント情報を足し上げる
                    element_histories.append(g_fields[i * 2 + 1]) #履歴として記録もしておく
                
    return sort_filter_v2, repeat_cnt


sort_filter_v2, repeat_cnt = comparisonAndNewConstruction()




def plusOutputType(type, text):
    
    if type == 1: #1...日本版のEdit形式
        plustext = "https://fumen.zui.jp/?v115@"
    elif type == 2: #2...日本版のFullList形式
        plustext = "https://fumen.zui.jp/?d115@"
    elif type == 3: #3...日本版のMiniList形式
        plustext = "https://fumen.zui.jp/?D115@"
    elif type == 4: #4...日本版のView形式
        plustext = "https://fumen.zui.jp/?m115@"
    elif type == 5: #5...モバイル版
        plustext = "https://knewjade.github.io/fumen-for-mobile/#?d=v115@"
    elif type == 6: #6...HardDrop版のEdit形式
        plustext = "https://harddrop.com/fumen/?v115@"
    elif type == 7: #7...HardDrop版のList形式
        plustext = "https://harddrop.com/fumen/?d115@"
    elif type == 8: #8...HardDrop版のView形式
        plustext = "https://harddrop.com/fumen/?m115@"
    else: #0...RAW DATA(v115@スタート)
        plustext = "v115@"
        
    return plustext + text


result_URL = plusOutputType(output_type, sort_filter_v2)


os.system("cls") #コンソール画面消去

print(f"結果URL  result URL   {repeat_cnt}パターン重複  {repeat_cnt} pattern duplicate")
print("")
print(result_URL)
print("")


print("URLをドラッグして選択し、Ctrl+Cキーでコピーしてください")
print("Drag the URL to select it and press Ctrl + C to copy it.")
print("")
print("コピーできたら、Enterキーを押してプログラムを終了させてください")
print("After copying, press Enter to exit the program.")

tmp = input()
