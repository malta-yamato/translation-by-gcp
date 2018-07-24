
## 概要

GCP(Google Cloud Platform) の Cloud Translation API を利用して翻訳を行います。
コマンドで翻訳したいテキストファイルを指定すると、出力フォルダに翻訳結果が格納されます。
翻訳したい言語は同時に複数を指定できます。
またAndroid開発用の追加機能として、リソースファイル res/values の strings.xml と arrays.xml の内容を翻訳し、ローカライズされたリソースを自動生成することも可能です。
GCPの翻訳APIを利用するので、コマンド実行で料金が発生します。料金体系については Cloud Translation API の説明ページでご確認ください。
翻訳が終了すると、API使用料金の見積額を表示します。私の経験上では一連の翻訳で＄1を超えることは稀です。
しかし過剰な利用を防ぐために、スクリプトで翻訳文字数の制限（デフォルト 100万文字）を設定しています。
この制限値を変更したい場合は各自ソースコードをご変更ください。ソースコードはMITライセンスで配布しております。
今後GCPの料金体系に変更があった場合、算出した見積額が誤ってしまう可能性がありますが、こちらについて直ぐに対応できるかどうか分かりません。見積額はあくまで参考値となります。

__免責事項__  
このスクリプトの使用で生じたあらゆる損害について作者は何ら責任を負うものではありません。

私は以下の条件でスクリプトを実行しました。
pythonのバージョンは3系であれば問題ないと思いますが、なるべく最新のものをご使用ください。

Python 3.6.5  
pip 10.0.1  
google-cloud-translate 1.3.1

## 事前準備

このスクリプトを使うにあたり、あらかじめ GCP のアカウントを作成し、Cloud Translation API を_有効_にしてください。
また以下の URL を参考に、python上で Cloud Translation API を使用できるように設定してください。

https://cloud.google.com/translate/docs/reference/libraries#client-libraries-install-python


## インストール方法

virtualenv 等の仮想環境でインストールすることをおすすめいたします。

pip install git+https://github.com/malta-yamato/translation-by-gcp.git

同時に google-cloud-translate もインストールされます。


## コマンド

### 通常のコマンド
translate 入力ファイル（現在、文字コードは utf-8 のみに対応しています）
例）translate sample.txt

### 翻訳先の指定（言語コード）
--langs 言語コード１ 言語コード2 …  
例）translate sample.txt --langs ja en

### 出力先フォルダの指定（省略可、デフォルトでは output-translation というフォルダが作成されて、そこに翻訳結果が格納される）
--output 出力先フォルダ  
例）translate sample.txt --langs ja en --output hoge

### 翻訳チェック（翻訳した結果をさらに指定した言語で翻訳し直します。結果は出力先フォルダの check フォルダに格納されます）
--check 言語コード  
例）translate sample.txt --langs en --check ja

### Android用
transand リソースフォルダ  
例）transand values --lang en --check ja
