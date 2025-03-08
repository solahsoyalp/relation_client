# はじめに

このドキュメントでは、Re:lation API Python クライアントの基本的な使い方を説明します。

## インストール

`relation-client`パッケージをインストールするには、以下のコマンドを実行します：

```bash
pip install relation-client
```

より新しい開発版を使用したい場合は、GitHubリポジトリから直接インストールすることも可能です：

```bash
pip install git+https://github.com/yourusername/relation-client.git
```

## 前提条件

Re:lation API クライアントを使用するには、以下が必要です：

- Python 3.6以上
- Re:lation APIのアクセストークン
- Re:lation APIのサブドメイン

アクセストークンとサブドメインは、Re:lation管理画面から取得することができます。

## クライアントの初期化

まず最初に、APIクライアントを初期化します：

```python
from relation_client import RelationClient

client = RelationClient(
    access_token='あなたのアクセストークン',
    subdomain='あなたのサブドメイン'
)
```

## 基本的な使い方

### アドレス帳（顧客グループ）の操作

アドレス帳の一覧を取得します：

```python
customer_groups = client.customer_groups.list()

for group in customer_groups:
    print(f"ID: {group.customer_group_id}, 名前: {group.name}")
```

### 顧客情報の操作

顧客を検索します：

```python
customers = client.customers.search(
    customer_group_id=1,  # アドレス帳ID
    emails=['example@email.com'],  # メールアドレスで検索
    per_page=20,  # 1ページあたりの件数
    page=1  # ページ番号
)

for customer in customers:
    print(f"ID: {customer.customer_id}, 名前: {customer.last_name} {customer.first_name}")
```

顧客を登録します：

```python
customer = client.customers.create(
    customer_group_id=1,  # アドレス帳ID
    last_name='山田',
    first_name='太郎',
    gender_cd=1,  # 1: 男性, 2: 女性, 9: 不明
    emails=[{'email': 'yamada@example.com'}],
    tels=[{'tel': '09012345678'}],
    system_id1='EMP0001'  # 顧客コード
)

print(f"登録完了: ID={customer.customer_id}")
```

### チケット（問い合わせ）の操作

チケットを検索します：

```python
from relation_client import STATUS_OPEN, METHOD_MAIL

tickets = client.tickets.search(
    message_box_id=123,  # 受信箱ID
    status_cds=[STATUS_OPEN],  # ステータス（未対応）
    method_cds=[METHOD_MAIL],  # チャネル（メール）
    per_page=20,  # 1ページあたりの件数
    page=1  # ページ番号
)

for ticket in tickets:
    print(f"ID: {ticket.ticket_id}, タイトル: {ticket.title}, ステータス: {ticket.status_cd}")
```

## エラーハンドリング

API呼び出し時のエラーは適切に処理することが重要です：

```python
from relation_client.exceptions import (
    AuthenticationError, PermissionError, ResourceNotFoundError,
    RateLimitError, InvalidRequestError, APIError, ServiceUnavailableError
)

try:
    # APIを呼び出す処理
    customers = client.customers.search(customer_group_id=1)
except AuthenticationError:
    print("認証エラー：アクセストークンが無効です")
except PermissionError:
    print("権限エラー：リソースへのアクセス権限がありません")
except ResourceNotFoundError:
    print("リソースが見つかりません")
except RateLimitError:
    print("レート制限を超えました。しばらく待ってから再試行してください")
except InvalidRequestError as e:
    print(f"リクエストが無効です：{e}")
except APIError as e:
    print(f"API内部エラー：{e}")
except ServiceUnavailableError:
    print("サービスが一時的に利用できません")
```

## 次のステップ

より詳細な情報については、以下のドキュメントを参照してください：

- [クライアント設定](./client_configuration.md) - クライアントの詳細な設定方法
- [顧客管理](./customers.md) - 顧客情報に関する操作
- [チケット管理](./tickets.md) - チケットに関する操作
- [エラーハンドリング](./error_handling.md) - 詳細なエラー処理 