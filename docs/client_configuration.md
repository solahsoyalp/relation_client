# クライアント設定

Re:lation API Pythonクライアントは、さまざまな設定オプションを提供し、APIとの通信方法をカスタマイズすることができます。このドキュメントでは、利用可能な設定オプションと、それらの使用方法について説明します。

## 基本的な初期化

クライアントを最もシンプルに初期化する方法は次のとおりです：

```python
from relation_client import RelationClient

client = RelationClient(
    access_token='あなたのアクセストークン',
    subdomain='あなたのサブドメイン'
)
```

## 利用可能な設定オプション

クライアントの初期化時には、以下のオプションを設定できます：

| オプション | 型 | デフォルト値 | 説明 |
|------------|------|---------|-----------|
| `access_token` | str | **必須** | Re:lation APIのアクセストークン |
| `subdomain` | str | **必須** | Re:lationのサブドメイン |
| `api_version` | str | `'v2'` | 利用するAPIのバージョン |
| `timeout` | int | `30` | リクエストのタイムアウト時間（秒） |
| `max_retries` | int | `3` | リクエスト失敗時の最大リトライ回数 |
| `retry_delay` | int | `1` | リトライ間の待機時間（秒） |
| `user_agent` | str | `None` | カスタムユーザーエージェント |
| `proxies` | dict | `None` | リクエスト時に使用するプロキシ設定 |

## 詳細な設定例

### APIバージョンの指定

特定のAPIバージョンを使用する場合：

```python
client = RelationClient(
    access_token='あなたのアクセストークン',
    subdomain='あなたのサブドメイン',
    api_version='v1'  # デフォルトはv2
)
```

### タイムアウトとリトライの設定

ネットワークの安定性に問題がある場合や、長時間実行されるリクエストを処理する場合：

```python
client = RelationClient(
    access_token='あなたのアクセストークン',
    subdomain='あなたのサブドメイン',
    timeout=60,        # リクエストのタイムアウトを60秒に延長
    max_retries=5,     # 最大5回のリトライを許可
    retry_delay=2      # リトライ間の待機時間を2秒に設定
)
```

### プロキシの設定

プロキシサーバーを経由してAPIにアクセスする場合：

```python
proxies = {
    'http': 'http://10.10.1.10:3128',
    'https': 'http://10.10.1.10:1080',
}

client = RelationClient(
    access_token='あなたのアクセストークン',
    subdomain='あなたのサブドメイン',
    proxies=proxies
)
```

### カスタムユーザーエージェントの設定

カスタムアプリケーションを識別するためのユーザーエージェントを設定する場合：

```python
client = RelationClient(
    access_token='あなたのアクセストークン',
    subdomain='あなたのサブドメイン',
    user_agent='MyCustomApp/1.0.0'
)
```

## 環境変数による設定

セキュリティを高めるために、アクセストークンを環境変数から読み込むパターンも推奨されています：

```python
import os
from relation_client import RelationClient

client = RelationClient(
    access_token=os.environ.get('RELATION_ACCESS_TOKEN'),
    subdomain=os.environ.get('RELATION_SUBDOMAIN')
)
```

## APIエンドポイントのURL生成

クライアントはAPIエンドポイントのURLを自動的に生成します。URLの構造は次のとおりです：

```
https://{subdomain}.relation-app.com/api/{api_version}/
```

たとえば、`subdomain`が`example`で`api_version`が`v2`の場合、ベースURLは次のようになります：

```
https://example.relation-app.com/api/v2/
```

## 設定変更

クライアントの初期化後に設定を変更する必要がある場合は、新しいクライアントインスタンスを作成してください。既存のクライアントインスタンスの設定を動的に変更することはできません。

## 設定のベストプラクティス

1. **環境変数の使用**: アクセストークンなどの秘密情報は環境変数として保存し、コードにハードコードしないでください。

2. **適切なタイムアウト値**: ネットワーク状況やAPIの応答時間を考慮して、適切なタイムアウト値を設定してください。

3. **リトライ戦略**: 一時的なネットワークエラーに対処するために、適切なリトライ回数と待機時間を設定してください。

4. **デバッグモード**: 開発中はログを詳細に設定し、問題のトラブルシューティングを容易にしてください。

## 関連情報

- [はじめに](./getting_started.md)
- [エラーハンドリング](./error_handling.md)
- [高度な使い方](./advanced_usage.md) 