# flask_chat
flaskを用いて作成した対話システムと会話が行えるアプリです。

## 使用方法
1. Dockerを使用しているので、cloneした後に`docker-compose up`を入力してください。  
1. imageのダウンロードが終わると、実行されるので`http://localhost:4231/`にアクセスしてください。
1. 表示されたwebページにあるloginボタンを押してください。
1. 初回の場合は、loginページにある`create new account`のリンクからアカウントを作成してください。
2. 対話システムとのチャットページが開くので、チャットを楽しんでください。

## 説明
- 研究のために作成した対話システムと会話できるチャットアプリです。
- 開発目的は以下になります。  
1. 対話システムを用いた実験を行う際に、別途ユーザ登録などが必要なサービスを使わず、簡単に対話ができるアプリケーションが必要であったこと。
2. 開発側でログデータなどを取得できるチャットアプリが必要であったこと。
3. 別のアプリケーションで利用するための対話システムAPIが必要であったため。
  
- 対話システムは用例ベースとなっており、700対程度のデータから、cos類似度を用いてユーザが入力した発話と近い内容のデータの返答を返します。  
- 対話システムのプログラムのみ書籍を参考に改変して作成しています。(code内に引用をのせております。)  
  
- webサイトの部分ではログイン処理を行い、ユーザに応じてチャットルームの作成と対話ログの保持を行っています。ユーザごとにそれぞれが会話を行うことが可能です。将来的には、対話ログの情報から会話内容の遷移やユーザ支援を行いたいと考えています。  
- 簡易的なAPIとしてjson形式でのリクエストを受け付け、対話システムの返答を別のアプリケーションに送信することが可能です。この機能を使い、研究では、VRアプリケーションやAIスピーカーへwebアプリケーションと同一の対話システムの実装を行っております。

## ソースコードの解説
- 

## 仕様
使用言語：python,javascript,HTML,css  
フレームワーク：flask  
インフラ：Docker,nginx 
