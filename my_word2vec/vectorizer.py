from gensim.models import word2vec
import logging
from wakati import Wakati

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

    def __init__(self, file_dir, dic_dir=None, user_dir=None, out_dir="out.txt", hinshis=["動詞", "形容詞", "形容動詞", "助動詞"]):
        """
        ==========================================================
        コンストラクタ
        Wakatiを使って文章を分かち書きしておく
        ==========================================================
        【変数説明】
        file_dir : 入力となる文章のディレクトリ
        dic_dir : システム辞書のディレクトリ(/usr/local/lib/mecab/dic/mecab-ipadic-neologd)
        user_dir : ユーザー辞書のディレクトリ(/Users/ユーザ名/Desktop/word2vec/user.dic)
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
