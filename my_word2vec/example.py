from vectorizer import Vectorizer

"""
==========================================================
自作のWord2Vecを使って、夏目漱石の『こころ』を解析する。
(『こころ』は青空文庫(http://www.aozora.gr.jp/cards/000148/card773.html)から
ダウンロードして同じディレクトリに入れておく)
==========================================================
【関数説明】
kokoro : 『こころ』のモデルを作成
"""

def kokoro():
    """
    ==========================================================
    『こころ』から作成されたモデルを返す
    ==========================================================
    【変数説明】
    dic_dir : システム辞書のディレクトリ(このPCでは"/usr/local/lib/mecab/dic/mecab-ipadic-neologd")
    user_dir : ユーザー辞書のディレクトリ(このPCでは"/Users/ユーザ名/Desktop/word2vec/user.dic")
    """

    #Vectorizerインスタンスを作成
    #__init__で文章が分かち書きされたファイル(out.txt)が同じディレクトリ内に作られる。
    #dic_dir、user_dirは変更が必要
    v = Vectorizer(file_dir="kokoro.txt",\
     dic_dir="/usr/local/lib/mecab/dic/mecab-ipadic-neologd",\
     user_dir="/Users/ユーザ名/Desktop/word2vec/user.dic")

    #単語の分散表現のモデル作成
    v.vectorize()

    #できたモデルを返す
    return v.model

if __name__ == "__main__":

    #『こころ』から作成されたモデル
    model = kokoro()

    #「人間」という単語に最も近い１０単語を表示する
    #resultは(単語, コサイン距離)からなるリスト
    result = model.most_similar(positive="人間")
    for pair in result:
        word = pair[0]
        distance = pair[1]
        print(word, distance)

    #完成したモデルを保存したければ以下のコードのコメントアウトを外す
    #v.save_model("kokoro.model")
