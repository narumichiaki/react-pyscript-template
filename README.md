# Web Application Template with React and PyScript

Reactをフロントエンド、PyScriptをバックエンドとして動作するWebアプリケーションのテンプレートです。

サーバを用意することなく、Sharepoint上にフロントエンドつきのPythonツールを展開するために開発しました。


## QuickStart
手元のPCで本テンプレートを使用したWebサービスを作成する場合は、`python -m http.server 8000`等でサーバを立ててご利用ください。
Sharepoint環境に設置することもできます(後述)。

- フロントエンドは`renderer.tsx`に記述します。
    - React + TypeScriptで書くことができます。
    - 必ず`window.api_endpoint(url: str, json_param: str) -> str`を定義する必要があります。
- バックエンドは`backend.py`に記述します。
    - Pythonで書くことができます。
    - 必ず`window.render(call_api: CallApiFunction) -> void`を定義する必要があります。
    - 標準外のモジュールをインポートする場合は、`pyscript.toml`に記載する必要があります。詳しくは、[PyScript公式ドキュメント](https://docs.pyscript.net/2024.10.1/user-guide/configuration/)を参照してください。


## 本テンプレートのメリット・デメリット
### メリット
- データ分析ライブラリが豊富なPythonをバックエンドとして使える。
- プログラミング環境・スキルがない人にもPython製ツールを提供できる。
- バージョンをツール作成側でコントロールできる。旧バージョンが各使用者の手元に残らない。
- ユーザによる意図しない改変を避けられる。
- Sharepoint環境のみ： Sharepoint上に設置して動作させられる(後述)。

### デメリット
- サーバが存在しないため、サーバ側でのデータ保持はできない。
- ユーザ側のPCに計算負荷がかかる。


## Sharepoint上への設置
本テンプレートは、[カスタムスクリプトが有効化されている](https://learn.microsoft.com/ja-jp/sharepoint/allow-or-prevent-custom-script)Sharepoint上に設置することができます。
`index.html`の拡張子を`.aspx`に変更してアップロードしてください。
