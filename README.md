GCP(Google Cloud Platform) の Cloud Translation API を利用して翻訳を行います。
翻訳のターゲットとなる言語を複数指定した一括翻訳が行えます。
Android のリソースファイル res/values の strings.xml と arrays.xml の内容を翻訳し、ローカライズされたリソースを自動で作成します。
料金が過大となるような過剰なリクエストを防ぐために翻訳文字数の制限を行っています。この制限値は引数で設定可能です。
翻訳が終了すると、使用料金の見積額を表示します。

このツールを使うにあたり、あらかじめ GCP のアカウントを作成し、Cloud Translation API を有効にしてください。
以下の URL をご参考ください。
TODO: Google Cloud URL

インストール方法


使用方法