# エラーハンドリング

Re:lation API Pythonクライアントは、API通信中に発生する可能性のあるさまざまなエラーを処理するための例外クラスを提供しています。適切なエラーハンドリングを実装することで、より堅牢なアプリケーションを構築できます。

## 例外の階層

ライブラリの例外は以下の階層構造になっています：

- `Exception`
  - `APIError` - すべてのAPIエラーの基底クラス
    - `AuthenticationError` - 認証エラー
    - `PermissionError` - 権限エラー
    - `ResourceNotFoundError` - リソースが見つからないエラー
    - `InvalidRequestError` - 無効なリクエストエラー
    - `RateLimitError` - レート制限エラー
    - `ServiceUnavailableError` - サービス利用不可エラー

## 基本的なエラーハンドリング

例外をキャッチして適切に処理するための基本的なパターンは以下の通りです：

```python
from relation_client import RelationClient
from relation_client.exceptions import (
    AuthenticationError, PermissionError, ResourceNotFoundError,
    RateLimitError, InvalidRequestError, APIError, ServiceUnavailableError
)

client = RelationClient(
    access_token='あなたのアクセストークン',
    subdomain='あなたのサブドメイン'
)

try:
    # APIを呼び出す処理
    customers = client.customers.search(customer_group_id=1)
except AuthenticationError:
    # アクセストークンが無効な場合の処理
    print("認証エラー：アクセストークンが無効です")
except PermissionError:
    # リソースへのアクセス権限がない場合の処理
    print("権限エラー：リソースへのアクセス権限がありません")
except ResourceNotFoundError:
    # リソースが存在しない場合の処理
    print("リソースが見つかりません")
except RateLimitError:
    # レート制限を超えた場合の処理
    print("レート制限を超えました。しばらく待ってから再試行してください")
except InvalidRequestError as e:
    # リクエスト内容に問題がある場合の処理
    print(f"リクエストが無効です：{e}")
except APIError as e:
    # その他のAPIエラーの処理
    print(f"API内部エラー：{e}")
except ServiceUnavailableError:
    # サービスが一時的に利用できない場合の処理
    print("サービスが一時的に利用できません")
except Exception as e:
    # 予期しないエラーの処理
    print(f"予期しないエラーが発生しました：{e}")
```

## レート制限の処理

Re:lation APIにはリクエスト頻度の制限があります。`RateLimitError`が発生した場合、一定時間待機してから再試行することが推奨されます。

```python
import time
from relation_client.exceptions import RateLimitError

def with_retry(func, max_retries=3, initial_delay=1):
    """レート制限エラーが発生した場合にリトライするデコレータ関数"""
    def wrapper(*args, **kwargs):
        retries = 0
        delay = initial_delay
        
        while retries <= max_retries:
            try:
                return func(*args, **kwargs)
            except RateLimitError:
                if retries == max_retries:
                    raise
                    
                print(f"レート制限エラー。{delay}秒待機してリトライします...")
                time.sleep(delay)
                retries += 1
                delay *= 2  # 指数バックオフ
    
    return wrapper

# 使用例
@with_retry
def search_customers(client, customer_group_id):
    return client.customers.search(customer_group_id=customer_group_id)

# 関数を呼び出し
customers = search_customers(client, 1)
```

## エラー情報の取得

`APIError`とそのサブクラスは、エラーに関する追加情報を提供します：

```python
try:
    # APIを呼び出す処理
    customers = client.customers.search(customer_group_id=1)
except InvalidRequestError as e:
    print(f"エラーコード: {e.status_code}")
    print(f"エラーメッセージ: {e}")
    print(f"詳細情報: {e.error_info}")
```

## ベストプラクティス

1. **具体的な例外をキャッチする**：できるだけ具体的な例外をキャッチして、それぞれに適した処理を行いましょう。

2. **リトライメカニズムを実装する**：一時的なエラー（`RateLimitError`や`ServiceUnavailableError`など）に対しては、適切なバックオフ戦略を用いたリトライメカニズムを実装しましょう。

3. **エラーをログに記録する**：エラー情報を適切にログに記録することで、問題の診断と解決が容易になります。

4. **ユーザーフレンドリーなエラーメッセージ**：エンドユーザーに表示するエラーメッセージは、技術的な詳細ではなく、解決策や次のステップを示す内容にしましょう。

## 関連リソース

- [例外モジュールのソースコード](https://github.com/yourusername/relation-client/blob/main/relation_client/exceptions.py)
- [APIドキュメント](https://docs.example.com/relation-api/errors)（日本語） 