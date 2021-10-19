from flask_app.models.ebdm_system import EbdmSystem

"""
@misc{Pythonでつくる対話システム,
      title = {Pythonでつくる対話システム},
      author = {東中 竜一郎 and 稲葉 通将 and 水上 雅博},
      year = {2020},
      publisher = {オーム社}
      } 
      書籍コードを一部改変して使用
"""


class Bot:
    def __init__(self):
        self.edbm = EbdmSystem()

    def start(self):
        # 最初の発話を生成するとき
        text = self.edbm.initial_message()
        return text["utt"]

    def message(self, update):
        # 辞書型 inputにユーザからの発話
        # replyメソッドで発話を生成
        inp = {"utt": update}
        text = self.edbm.reply(inp)
        return text["utt"]
