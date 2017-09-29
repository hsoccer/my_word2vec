import MeCab
from gensim.models import word2vec
import logging

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

    def __init__(self, file_dir, dic_dir, user_dir=None, hinshis=["動詞", "形容詞", "形容動詞", "助動詞"]):
        """
        ==========================================================
        コンストラクタ
        ==========================================================
        【変数説明】
        file_dir : 入力となる文章のディレクトリ
        dic_dir : システム辞書のディレクトリ(/usr/local/lib/mecab/dic/mecab-ipadic-neologd)
        user_dir : ユーザー辞書のディレクトリ(/Users/konoharuki/Desktop/word2vec/user.dic)
        hinshis : 活用する語
        tagger : MeCab用のtagger(詳細はMeCab自体のドキュメント参照)
        f : 入力ファイル
        splited_text : 各行を分かち書きしたもの(splited_line)をリストで格納する(Noneで初期化)
        """
        if user_dir is not None:
            self.tagger = MeCab.Tagger("mecabrc -d {} -u {}".format(dic_dir, user_dir))
        else:
            self.tagger = MeCab.Tagger("mecabrc -d {}".format(dic_dir))
        self.f = open(file_dir, 'r')
        self.hinshis = hinshis
        self.splited_text = None

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
        self.fout = open(self.out_dir, 'w')
        for line in self.splited_text:
            self.fout.write(" ".join(line) + " ")
        self.fout.close()

class Vectorizer(Wakati):

    """
    ==========================================================
    Wakatiをベースとして、分かち書きしたものを学習して分散表現する
    ==========================================================
    【関数説明】
    __init__ : コンストラクタ
    vectorize : 分散表現を作る
    _train : gensimを使ってword2vecする
    save_model : 作ったモデルを保存する
    """

    def __init__(self, file_dir, dic_dir, user_dir=None, out_dir="out.txt", hinshis=["動詞", "形容詞", "形容動詞", "助動詞"]):
        """
        ==========================================================
        コンストラクタ
        Wakatiを使って文章を分かち書きしておく
        ==========================================================
        【変数説明】
        file_dir : 入力となる文章のディレクトリ
        dic_dir : システム辞書のディレクトリ(/usr/local/lib/mecab/dic/mecab-ipadic-neologd)
        user_dir : ユーザー辞書のディレクトリ(/Users/konoharuki/Desktop/word2vec/user.dic)
        out_dir : 分かち書きされた文章のファイルのディレクトリ
        hinshis : 活用する語
        model : モデル(Noneで初期化)
        """
        Wakati.__init__(self, file_dir, dic_dir, user_dir, hinshis)
        self.out_dir = out_dir
        self.model = None
        self.wakati()
        self.output(self.out_dir)

    def vectorize(self, other_file_dir=None, sg=1, size=300, min_count=10, window=5, hs=0, negative=15, iter=15):
        """
        ==========================================================
        単語の分散表現を作成
        ==========================================================
        【変数説明】
        out_dir : 分かち書きされた文章のファイル
        other_file_dir : out_dirを使わない場合のファイル名(Noneで初期化)
        sentences : 分かち書きされ、空白区切の文章全文
        """
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        if other_file_dir is None:
            sentences = word2vec.Text8Corpus(self.out_dir)
        else:
            sentences = word2vec.Text8Corpus(other_file_dir)
        self._train(sentences, sg, size, min_count, window, hs, negative, iter)

    def _train(self, sentences, sg=1, size=300, min_count=10, window=5, hs=0, negative=15, iter=15):
        """
        ==========================================================
        gensimによる学習
        ==========================================================
        【変数説明】
        sentences : 分かち書きされ、空白区切の文章全文
        word2vecの引数 : 詳細はgensimのドキュメント参照
        """
        self.model = word2vec.Word2Vec(sentences, sg=sg, size=size, min_count=min_count, window=window, hs=hs, negative=negative, iter=iter)

    def save_model(self, model_dir):
        """
        ==========================================================
        モデルを保存する
        ==========================================================
        【変数説明】
        model_dir : モデルを保存するディレクトリ
        """
        assert self.model is not None
        self.model.save(model_dir)
