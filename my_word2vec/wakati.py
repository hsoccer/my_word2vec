import MeCab

class Wakati(object):

    """
    ==========================================================
    ファイルに存在する文章を指定の辞書を用いてMeCabによって形態素に分ける
    ==========================================================
    【関数説明】
    __init__ : コンストラクタ
    wakati : 文章を分かち書きする
    output : 結果をファイルに出力する
    """

    def __init__(self, file_dir, dic_dir=None, user_dir=None, hinshis=["動詞", "形容詞", "形容動詞", "助動詞"]):
        """
        ==========================================================
        コンストラクタ
        ==========================================================
        【変数説明】
        file_dir : 入力となる文章のディレクトリ
        dic_dir : システム辞書のディレクトリ(/usr/local/lib/mecab/dic/mecab-ipadic-neologd)
        user_dir : ユーザー辞書のディレクトリ(/Users/ユーザ名/Desktop/word2vec/user.dic)
        hinshis : 活用する語
        tagger : MeCab用のtagger(詳細はMeCab自体のドキュメント参照)
        f : 入力ファイル
        splited_text : 各行を分かち書きしたもの(splited_line)をリストで格納する(Noneで初期化)
        out_dir : 出力ファイルのディレクトリ(Noneで初期化)
        """
        if dic_dir is not None and user_dir is not None:
            self.tagger = MeCab.Tagger("mecabrc -d {} -u {}".format(dic_dir, user_dir))
        elif dic_dir is not None:
            self.tagger = MeCab.Tagger("mecabrc -d {}".format(dic_dir))
        else:
            self.tagger = MeCab.Tagger("mecabrc")
        self.f = open(file_dir, 'r')
        self.hinshis = hinshis
        self.splited_text = None
        self.out_dir = None

    def wakati(self):
        """
        ==========================================================
        文章全体を分かち書きし、self.splited_textに格納する
        その際、活用された語については原形に直す
        ==========================================================
        【変数説明】
        line : 入力文章の一行(更新されていく)
        splited_line : 各行の文章を分かち書きしたもののリスト
        node : 各単語のノード
        word : 単語
        feature : 単語の情報
        hinshi : 品詞
        kata : 活用形
        genkei : 原形
        """
        line = self.f.readline()
        splited_text = []
        while line:
            node = self.tagger.parseToNode(line).next
            splited_line = []
            while node.surface:
                word = node.surface
                feature = node.feature.split(',')
                hinshi = feature[0]
                kata = feature[5]
                genkei = feature[6]
                if hinshi in self.hinshis:
                    if kata != "基本形":
                        word = genkei
                splited_line.append(word)
                node = node.next
            splited_text.append(splited_line)
            line = self.f.readline()
        self.splited_text = splited_text
        self.f.close()

    def output(self, out_dir):
        """
        ==========================================================
        self.splited_textをファイルに出力する
        ==========================================================
        【変数説明】
        out_dir : 出力ファイルのディレクトリ
        fout : 出力ファイル
        """
        assert self.splited_text is not None
        if self.out_dir is None:
            self.out_dir = out_dir
        self.fout = open(self.out_dir, 'w')
        for line in self.splited_text:
            self.fout.write(" ".join(line) + " ")
        self.fout.close()
