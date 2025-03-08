# Re:lation API Python クライアントドキュメント

Re:lation APIを簡単に利用するためのPythonライブラリのドキュメントへようこそ。このドキュメントでは、ライブラリの使い方や機能について詳しく説明しています。

## 目次

1. [はじめに](./getting_started.md)
2. [クライアント設定](./client_configuration.md)
3. [顧客管理](./customers.md)
4. [チケット管理](./tickets.md)
5. [チャット機能](./chats.md)
6. [テンプレート](./templates.md)
7. [添付ファイル](./attachments.md)
8. [エラーハンドリング](./error_handling.md)
9. [高度な使い方](./advanced_usage.md)
10. [リファレンス](./reference.md)

## クイックスタート

```python
from relation_client import RelationClient

# クライアントを初期化
client = RelationClient(
    access_token='あなたのアクセストークン',
    subdomain='あなたのサブドメイン'
)

# アドレス帳一覧の取得
customer_groups = client.customer_groups.list()
for group in customer_groups:
    print(f"ID: {group.customer_group_id}, 名前: {group.name}")

# 顧客の検索
customers = client.customers.search(
    customer_group_id=1,  # アドレス帳ID
    emails=['example@email.com']  # メールアドレスで検索
)
```

詳しい使い方は[はじめに](./getting_started.md)を参照してください。 