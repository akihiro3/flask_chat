from elasticsearch import Elasticsearch
import MeCab
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

"""
@misc{Pythonでつくる対話システム,
      title = {Pythonでつくる対話システム},
      author = {東中 竜一郎 and 稲葉 通将 and 水上 雅博},
      year = {2020},
      publisher = {オーム社}
      書籍コードを一部改変して使用
      } 
"""


class EbdmSystem:
    def __init__(self):
        # MeCabの初期化
        self.tagger = MeCab.Tagger('-Owakati')
        self.tagger.parse("")
        # Elasticsearchと接続
        self.es = Elasticsearch("es")

    def initial_message(self):
        # 最初の発話を返す
        text = {"utt": 'こんにちは。対話を始めましょう。'}
        return text

    def reply(self, user_input):
        # scoreとresultの初期値
        max_score = -float('inf')
        result = ''

        # cos類似度でscoreが高い返答を選択
        for r in self.__reply(user_input['utt']):
            score = self.evaluate(user_input['utt'], r)
            if score >= max_score:
                max_score = score
                result = r[1]
        return {"utt": result}

    def __reply(self, utt):
        # Elasticsearchの機能で100件の用例を抽出
        results = self.es.search(index='dialogue_pair',
                                 query={'match': {'query': utt}}, size=10,)
        return [(result['_source']['query'], result['_source']['response'], result["_score"]) for result in results['hits']['hits']]

    def evaluate(self, utt, pair):
        # cos類似度を算出
        return self.cosine(utt, pair[0]) * self.cosine(utt, pair[1])

    def cosine(self, a, b):
        # sklearnのvectorizerを使って単語頻度ベクトルを作る
        a, b = CountVectorizer(token_pattern=u'(?u)\\b\\w+\\b').fit_transform(
            [self.tagger.parse(a), self.tagger.parse(b)])
        # cosine_similarityでコサイン類似度を計算する
        return cosine_similarity(a, b)[0]
