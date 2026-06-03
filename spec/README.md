# spec/ ディレクトリ

このディレクトリは、Re:lation API の **OpenAPI 3.0 仕様**（単一の信頼できる情報源 /
single source of truth）をローカルに配置するための場所です。

仕様の正本（canonical source）は、別リポジトリ
[`solahsoyalp/Re_lation_API_Docs_Unofficial`](https://github.com/solahsoyalp/Re_lation_API_Docs_Unofficial)
の `spec/` ディレクトリで配布されている OpenAPI 3.0 JSON 群です。

## ローカルへの取得方法

巨大なJSONをこのクライアントリポジトリに同梱（ベンダリング）しないため、
仕様ファイル（`*.json`）は `.gitignore` でGit管理対象外にしています。
必要なときに、以下のコマンドで正本をローカルへ取得してください。

```sh
python3 scripts/sync_openapi.py
```

実行すると、リソースごとに分割された OpenAPI 3.0 JSON がこのディレクトリへ
ダウンロードされます。

## 整合性テスト

仕様をローカルに同期した状態で整合性テストを実行すると、クライアント実装
（エンドポイントパスやAPIバージョン）が OpenAPI 仕様と矛盾していないかを
スモークチェックします。

```sh
python3 -m pytest relation_client/tests/test_openapi_consistency.py -q
```

仕様がローカルに同期されていない場合、テストは**スキップ**されます
（CIではデフォルトでネットワークアクセスを行いません）。
