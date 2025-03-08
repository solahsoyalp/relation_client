# Re:lation API Python クライアント

[![Python Versions](https://img.shields.io/pypi/pyversions/relation-client.svg)](https://pypi.org/project/relation-client/)
[![PyPI Version](https://img.shields.io/pypi/v/relation-client.svg)](https://pypi.org/project/relation-client/)
[![License](https://img.shields.io/github/license/yourusername/relation-client.svg)](https://github.com/yourusername/relation-client/blob/main/LICENSE)

Re:lation APIを簡単に利用するためのPythonライブラリです。このクライアントライブラリを使用することで、Re:lation APIを簡単かつ効率的に操作することができます。

*Read this in other languages: [English](#english), [日本語](#japanese)*

<a id="japanese"></a>
## 機能

- Re:lation APIの認証と接続管理
- アドレス帳（顧客グループ）の操作
- 顧客情報の検索・作成・更新・削除
- チケット（問い合わせ）の検索・取得・更新
- メッセージの送受信
- チャット情報の取得
- チケット分類の管理
- ラベルの管理
- テンプレートの操作
- 添付ファイルの操作
- バッジの管理
- メールアカウントと送信の管理

## インストール

### pipを使用したインストール

```bash
pip install relation-client
```

### 開発版のインストール

最新の開発版を使用したい場合は、GitHubリポジトリから直接インストールできます：

```bash
pip install git+https://github.com/solahsoyalp/relation_client.git
```

## 前提条件

- Python 3.6以上
- Re:lation APIのアクセストークン
- Re:lation APIのサブドメイン

## 基本的な使い方

### クライアントの初期化

```python
from relation_client import RelationClient

# クライアントの初期化
client = RelationClient(
    access_token='あなたのアクセストークン',
    subdomain='あなたのサブドメイン'
)
```

### クライアントオプション

クライアントの初期化時に、以下のオプションを設定できます：

```python
client = RelationClient(
    access_token='あなたのアクセストークン',
    subdomain='あなたのサブドメイン',
    api_version='v2',  # APIバージョン (デフォルト: v2)
    timeout=30,        # リクエストタイムアウト秒数
    max_retries=3,     # リトライ最大回数
    retry_delay=1      # リトライ間の待機秒数
)
```

## 詳細な使用例

### アドレス帳の操作

#### アドレス帳一覧の取得

```python
# アドレス帳一覧の取得
customer_groups = client.customer_groups.list()

for group in customer_groups:
    print(f"ID: {group.customer_group_id}, 名前: {group.name}")
```

### 顧客情報の操作

#### 顧客の検索

```python
# 顧客の検索
customers = client.customers.search(
    customer_group_id=1,  # アドレス帳ID
    emails=['example@email.com'],  # メールアドレスで検索
    per_page=20,  # 1ページあたりの件数
    page=1  # ページ番号
)

for customer in customers:
    print(f"ID: {customer.customer_id}, 名前: {customer.last_name} {customer.first_name}")
```

### 顧客の登録

```python
# 顧客の登録
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

### 顧客の取得

```python
# system_id1 で顧客を取得
customer = client.customers.get_by_system_id1(
    customer_group_id=1,  # アドレス帳ID
    system_id1='EMP0001'  # 顧客コード
)

print(f"顧客情報: {customer.last_name} {customer.first_name}")

# メールアドレスで顧客を取得
customer = client.customers.get_by_email(
    customer_group_id=1,  # アドレス帳ID
    email='yamada@example.com'
)

print(f"顧客情報: {customer.last_name} {customer.first_name}")
```

### 顧客の更新

```python
# system_id1 で顧客を更新
updated_customer = client.customers.update_by_system_id1(
    customer_group_id=1,  # アドレス帳ID
    system_id1='EMP0001',  # 顧客コード
    company_name='株式会社サンプル',
    emails=[{'email': 'new_yamada@example.com'}]
)

print(f"更新完了: {updated_customer.company_name}")
```

### 顧客の削除

```python
# system_id1 で顧客を削除
client.customers.delete_by_system_id1(
    customer_group_id=1,  # アドレス帳ID
    system_id1='EMP0001'  # 顧客コード
)

print("削除完了")
```

### チケットの検索

```python
from relation_client import STATUS_OPEN, METHOD_MAIL

# 未対応のチケットを検索
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

### チケットの取得

```python
# チケットの取得
ticket = client.tickets.get(
    message_box_id=123,  # 受信箱ID
    ticket_id=456  # チケットID
)

print(f"チケット情報: ID={ticket.ticket_id}, タイトル={ticket.title}")

# チケット内のメッセージを表示
for message in ticket.messages:
    print(f"メッセージID: {message.message_id}")
    print(f"件名: {message.title}")
    print(f"本文: {message.body}")
    print(f"送信日時: {message.sent_at}")
    print(f"チャネル: {message.method_cd}")
    print("---")
```

### チケットの更新

```python
from relation_client import STATUS_CLOSED, COLOR_RED

# チケットを更新（完了にする）
client.tickets.update(
    message_box_id=123,  # 受信箱ID
    ticket_id=456,  # チケットID
    status_cd=STATUS_CLOSED,  # ステータス（対応完了）
    color_cd=COLOR_RED,  # 色（赤）
    assignee="yamada"  # 担当者のメンション名
)

print("チケット更新完了")
```

### チケット分類の操作

```python
# チケット分類一覧の取得
case_categories = client.case_categories.list(
    message_box_id=123,  # 受信箱ID
    per_page=50,  # 1ページあたりの件数
    page=1  # ページ番号
)

for category in case_categories:
    print(f"ID: {category.case_category_id}")
    print(f"名前: {category.name}")
    if category.parent_id:
        print(f"親カテゴリID: {category.parent_id}")
    print(f"アーカイブ: {'はい' if category.archived else 'いいえ'}")
    print("---")

# チケット分類の登録
result = client.case_categories.create(
    message_box_id=123,  # 受信箱ID
    name="新規カテゴリ",  # カテゴリ名
    parent_id=1  # 親カテゴリID（省略可能）
)

print(f"チケット分類登録完了: ID={result['case_category_id']}")

# チケット分類の更新
client.case_categories.update(
    message_box_id=123,  # 受信箱ID
    case_category_id=2,  # チケット分類ID
    name="カテゴリ名更新",  # カテゴリ名
    archived=True  # アーカイブするかどうか
)

print("チケット分類更新完了")

# 更新時の注意事項：
# - 更新するチケット分類に子チケット分類や孫チケット分類が存在する場合、それらもアーカイブされます。
# - 親チケット分類がアーカイブされている場合、その分類は復活できません。

# チケットをチケット分類で分類する
client.tickets.update(
    message_box_id=123,  # 受信箱ID
    ticket_id=456,  # チケットID
    case_category_ids=[1, 2]  # チケット分類IDのリスト（複数指定可能）
)

print("チケットを分類しました")
```

### ラベルの操作

```python
# ラベル一覧の取得
labels = client.labels.list(
    message_box_id=123,  # 受信箱ID
    per_page=50,  # 1ページあたりの件数
    page=1  # ページ番号
)

for label in labels:
    print(f"ID: {label.label_id}")
    print(f"名前: {label.name}")
    print(f"色: {label.color}")
    if label.parent_id:
        print(f"親ラベルID: {label.parent_id}")
    print("---")

# ラベルの登録
result = client.labels.create(
    message_box_id=123,  # 受信箱ID
    name="重要",  # ラベル名
    color="red_01",  # 色
    parent_id=1  # 親ラベルID（省略可能）
)

print(f"ラベル登録完了: ID={result['label_id']}")

# ラベルの更新
client.labels.update(
    message_box_id=123,  # 受信箱ID
    label_id=2,  # ラベルID
    name="最重要",  # ラベル名
    color="red_04",  # 色
    parent_id=None  # 親ラベルID（Noneで親ラベルに変更）
)

print("ラベル更新完了")

# チケットにラベルを設定する
client.tickets.update(
    message_box_id=123,  # 受信箱ID
    ticket_id=456,  # チケットID
    label_ids=[1, 2]  # ラベルIDのリスト（複数指定可能）
)

print("チケットにラベルを設定しました")
```

### チャット情報の取得

```python
# ChatPlus情報の取得
chatplus = client.chats.get_chatplus(
    message_box_id=123,  # 受信箱ID
    ticket_id=456,  # チケットID
    message_id=789  # メッセージID
)

print(f"ChatPlusアカウント: {chatplus.account}")
print(f"顧客メールアドレス: {chatplus.email}")

# 会話履歴の表示
for conv in chatplus.conversations:
    print(f"発言者: {conv.speaker_name}")
    print(f"会話種別: {conv.conversation_type}")
    print(f"内容: {conv.note}")
    print(f"送信日時: {conv.sent_at}")
    print("---")

# Yahoo!ショッピング情報の取得
yahoo = client.chats.get_yahoo(
    message_box_id=123,  # 受信箱ID
    ticket_id=456,  # チケットID
    message_id=789  # メッセージID
)

print(f"Yahoo!ショッピングアカウント: {yahoo.account}")
print(f"問い合わせステータス: {yahoo.inquiry_status}")
print(f"問い合わせ種別: {yahoo.inquiry_kind}")

# R-Messe情報の取得
rmesse = client.chats.get_r_messe(
    message_box_id=123,  # 受信箱ID
    ticket_id=456,  # チケットID
    message_id=789  # メッセージID
)

print(f"R-Messeアカウント: {rmesse.account}")
print(f"問い合わせステータス: {rmesse.inquiry_status}")
print(f"問い合わせカテゴリ: {rmesse.inquiry_category}")

# LINE情報の取得
line = client.chats.get_line(
    message_box_id=123,  # 受信箱ID
    ticket_id=456,  # チケットID
    message_id=789  # メッセージID
)

print(f"LINEアカウント: {line.account}")
print(f"チャネルID: {line.channel_id}")
print(f"グループ名: {line.group_name}")
```

### メールの操作

```python
from relation_client import STATUS_OPEN

# 新規メール送信
result = client.mails.send(
    message_box_id=123,  # 受信箱ID
    mail_account_id=1,  # 送信メールアカウントID
    to="customer@example.com",  # 宛先
    subject="お問い合わせありがとうございます",  # 件名
    body="いつもご利用ありがとうございます。\n...",  # 本文
    status_cd=STATUS_OPEN,  # ステータス
    cc="team@example.com",  # CC
    bcc="archive@example.com",  # BCC
    is_html=False,  # HTMLメールかどうか
    pending_reason_id=None  # 保留理由ID
)

print(f"メール送信完了: メッセージID={result['message_id']}, チケットID={result['ticket_id']}")

# メール返信
result = client.mails.reply(
    message_box_id=123,  # 受信箱ID
    message_id=456,  # 返信元メッセージID
    mail_account_id=1,  # 送信メールアカウントID
    to="customer@example.com",  # 宛先
    subject="Re: お問い合わせについて",  # 件名
    body="お問い合わせいただきありがとうございます。\n...",  # 本文
    status_cd=STATUS_OPEN,  # ステータス
    cc="team@example.com",  # CC
    is_html=False  # HTMLメールかどうか
)

print(f"メール返信完了: メッセージID={result['message_id']}")

# メール下書き作成（新規）
result = client.mails.draft(
    message_box_id=123,  # 受信箱ID
    mail_account_id=1,  # 送信メールアカウントID
    to="customer@example.com",  # 宛先
    subject="お問い合わせありがとうございます",  # 件名
    body="いつもご利用ありがとうございます。\n下書き段階のメールです。",  # 本文
    is_html=False  # HTMLメールかどうか
)

print(f"メール下書き作成完了: メッセージID={result['message_id']}, チケットID={result['ticket_id']}")

# メール下書き作成（返信）
result = client.mails.draft(
    message_box_id=123,  # 受信箱ID
    message_id=456,  # 返信元メッセージID
    mail_account_id=1,  # 送信メールアカウントID
    to="customer@example.com",  # 宛先
    subject="Re: お問い合わせについて",  # 件名
    body="お問い合わせいただきありがとうございます。\n下書きの返信です。",  # 本文
    is_html=True  # HTMLメールにする場合
)

print(f"返信メール下書き作成完了: メッセージID={result['message_id']}")
```

### 応対メモの作成

```python
from relation_client import STATUS_OPEN, ICON_MEETING
from datetime import datetime
import pytz

# 現在時刻（日本時間）
jst = pytz.timezone('Asia/Tokyo')
now = datetime.now(jst).isoformat()

# 応対メモを作成（新規チケット）
result = client.tickets.create_record(
    message_box_id=123,  # 受信箱ID
    subject="お問い合わせ対応",  # 件名
    operated_at=now,  # 応対日時
    duration=30,  # 応対時間（分）
    body="お客様からの問い合わせに対応しました。次回は来週フォローアップの連絡をします。",  # 本文
    status_cd=STATUS_OPEN,  # ステータス（未対応）
    icon_cd=ICON_MEETING,  # 応対種別（会議）
    customer_email="customer@example.com",  # 顧客メールアドレス
    operator="tanaka"  # 応対者のメンション名
)

print(f"応対メモ作成完了: メッセージID={result['message_id']}, チケットID={result['ticket_id']}")

# 既存チケットに応対メモを追加
result = client.tickets.create_record(
    message_box_id=123,  # 受信箱ID
    subject="フォローアップ対応",  # 件名
    operated_at=now,  # 応対日時
    duration=15,  # 応対時間（分）
    body="お客様にフォローアップの連絡をしました。",  # 本文
    ticket_id=456,  # 既存チケットID
    icon_cd=ICON_CALLED_PHONE  # 応対種別（架電）
)

print(f"応対メモ追加完了: メッセージID={result['message_id']}")
```

### 受信箱の一覧取得

```python
# 受信箱一覧の取得
message_boxes = client.message_boxes.list()

for box in message_boxes:
    print(f"ID: {box.message_box_id}, 名前: {box.name}, 色: {box.color}")
    print(f"アドレス帳ID: {box.customer_group_id}, 更新日時: {box.last_updated_at}")
    print("---")

# 受信箱の取得
message_box = client.message_boxes.get(message_box_id=123)

print(f"受信箱情報: ID={message_box.message_box_id}, 名前={message_box.name}")
```

### 保留理由の一覧取得

```python
from relation_client import SNOOZE_TODAY, SNOOZE_TOMORROW

# 保留理由一覧の取得
pending_reasons = client.pending_reasons.list(message_box_id=123)

for reason in pending_reasons:
    print(f"ID: {reason.pending_reason_id}, 名前: {reason.name}")
    print(f"スヌーズ設定: {'あり' if reason.is_snoozed else 'なし'}")
    if reason.snooze_term:
        print(f"スヌーズ期間: {reason.snooze_term}")
    print("---")

# スヌーズ期間の定数を利用したチケット更新
client.tickets.update(
    message_box_id=123,
    ticket_id=456,
    status_cd="ongoing",  # 保留
    pending_reason_id=1,  # スヌーズ設定のある保留理由ID
    assignee="yamada"
)

print("チケットを保留に更新しました")
```

### 送信メール設定の一覧取得

```python
# 送信メール設定一覧の取得
mail_accounts = client.mail_accounts.list(
    message_box_id=123,  # 受信箱ID
    per_page=50,  # 1ページあたりの件数
    page=1  # ページ番号
)

for account in mail_accounts:
    print(f"ID: {account.mail_account_id}, 名前: {account.name}")
    print(f"メールアドレス: {account.email}")
    print("---")

# メール送信時に送信元として指定する場合
client.tickets.send_mail(
    message_box_id=123,
    ticket_id=456,
    to="customer@example.com",
    subject="お問い合わせありがとうございます",
    body="いつもご利用ありがとうございます。\n...",
    mail_account_id=1  # 送信メール設定ID
)

print("メールを送信しました")
```

### ユーザー一覧の取得

```python
from relation_client import USER_STATUS_AVAILABLE

# ユーザー一覧の取得
users = client.users.list(per_page=50, page=1)

for user in users:
    print(f"メンション名: {user.mention_name}")
    print(f"氏名: {user.last_name} {user.first_name}")
    print(f"部署: {user.department_name}")
    print(f"メールアドレス: {user.email}")
    print(f"ステータス: {user.status_cd}")
    print(f"管理者権限: {'あり' if user.is_tenant_admin else 'なし'}")
    print(f"多要素認証: {'有効' if user.is_otp_required else '無効'}")
    
    if user.last_page_loaded_at:
        print(f"最終アクセス日時: {user.last_page_loaded_at}")
    print("---")

# 有効なユーザーのみを表示
available_users = [user for user in users if user.status_cd == USER_STATUS_AVAILABLE]
print(f"有効なユーザー数: {len(available_users)}")
```

### バッジの一覧取得

```python
# バッジ一覧を取得
badges = client.badges.list(message_box_id=1)

for badge in badges:
    print(f"ID: {badge.badge_id}, 名前: {badge.name}")
```

### テンプレートの操作

```python
# テンプレート一覧を取得
templates = client.templates.list(message_box_id=1)

for template in templates:
    print(f"ID: {template.template_id}, 名前: {template.template_name}, カテゴリ: {template.template_category_name}")
    
# テンプレートカテゴリで検索
category_templates = client.templates.search(
    message_box_id=1, 
    template_category_name="お問い合わせ返信"
)

for template in category_templates:
    print(f"件名: {template.title}")
    print(f"本文: {template.text_body}")
    
# すべてのテンプレートを検索（カテゴリ指定なし）
all_templates = client.templates.search(message_box_id=1)

# テンプレートの使用例
if templates:
    template = templates[0]
    print(f"From: {template.from_}")  # 'from' はPythonの予約語のため 'from_' として参照
    print(f"To: {template.to}")
    print(f"件名: {template.title}")
    print(f"HTML本文: {template.html_body}")
    print(f"テキスト本文: {template.text_body}")
```

### 添付ファイルのダウンロード

```python
# 添付ファイルのダウンロードURLを取得
download_info = client.attachments.get_download_url(
    message_box_id=123,  # 受信箱ID
    attachment_id=456  # 添付ファイルID
)

print(f"ファイル名: {download_info['file_name']}")
print(f"ダウンロードURL: {download_info['url']}")
print(f"URL有効期限: {download_info['expires_in_sec']}秒")

# 添付ファイルのダウンロード例（requests使用）
import requests
import os

response = requests.get(download_info['url'], stream=True)
if response.status_code == 200:
    # ファイルを保存
    with open(download_info['file_name'], 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"ファイルを保存しました: {os.path.abspath(download_info['file_name'])}")
```

## エラーハンドリング

このライブラリは、Re:lation APIから返されるエラーを適切に処理します。エラーは以下のように捕捉できます：

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

## レート制限

Re:lation APIにはレート制限があります。制限に達すると、`RateLimitError`例外が発生します。
このライブラリは自動的にリトライ処理を行いますが、大量のリクエストを短時間に行う場合は注意が必要です。

## 開発とテスト

### 開発環境のセットアップ

```bash
# リポジトリのクローン
git clone https://github.com/yourusername/relation-client.git
cd relation-client

# 開発用の依存関係をインストール
pip install -e ".[dev]"
```

### テストの実行

```bash
# すべてのテストを実行
pytest

# カバレッジレポートを生成
pytest --cov=relation_client tests/
```

## ライセンス

このプロジェクトはMITライセンスの下で提供されています。詳細は[LICENSE](LICENSE)ファイルを参照してください。

## 貢献

貢献は歓迎します！バグ報告、機能リクエスト、プルリクエストなど、あらゆる形での貢献をお待ちしています。詳細は[貢献ガイドライン](docs/contributing.md)を参照してください。

1. このリポジトリをフォークする
2. 機能ブランチを作成する：`git checkout -b my-new-feature`
3. 変更をコミットする：`git commit -am 'Add some feature'`
4. ブランチをプッシュする：`git push origin my-new-feature`
5. プルリクエストを作成する

## 問い合わせ

質問や問題がある場合は、[GitHub Issues](https://github.com/yourusername/relation-client/issues)で報告してください。

---

<a id="english"></a>
# Re:lation API Python Client

A Python library for easily using the Re:lation API. This client library allows you to interact with the Re:lation API in a simple and efficient way.

## Features

- Re:lation API authentication and connection management
- Address book (customer group) operations
- Customer information search, creation, updating, and deletion
- Ticket (inquiry) search, retrieval, and updating
- Message sending and receiving
- Chat information retrieval
- Ticket classification management
- Label management
- Template operations
- Attachment handling
- Badge management
- Mail account and sending management

## Installation

### Installation using pip

```bash
pip install relation-client
```

### Development version installation

If you want to use the latest development version, you can install directly from the GitHub repository:

```bash
pip install git+https://github.com/yourusername/relation-client.git
```

## Prerequisites

- Python 3.6 or higher
- Re:lation API access token
- Re:lation API subdomain

## Basic Usage

### Client Initialization

```python
from relation_client import RelationClient

# Initialize the client
client = RelationClient(
    access_token='your_access_token',
    subdomain='your_subdomain'
)
```

### Client Options

You can set the following options when initializing the client:

```python
client = RelationClient(
    access_token='your_access_token',
    subdomain='your_subdomain',
    api_version='v2',  # API version (default: v2)
    timeout=30,        # Request timeout in seconds
    max_retries=3,     # Maximum number of retries
    retry_delay=1      # Wait time between retries in seconds
)
```

## Error Handling

This library appropriately handles errors returned from the Re:lation API. Errors can be caught as follows:

```python
from relation_client.exceptions import (
    AuthenticationError, PermissionError, ResourceNotFoundError,
    RateLimitError, InvalidRequestError, APIError, ServiceUnavailableError
)

try:
    # API call process
    customers = client.customers.search(customer_group_id=1)
except AuthenticationError:
    print("Authentication error: Invalid access token")
except PermissionError:
    print("Permission error: No access rights to the resource")
except ResourceNotFoundError:
    print("Resource not found")
except RateLimitError:
    print("Rate limit exceeded. Please wait and try again later")
except InvalidRequestError as e:
    print(f"Invalid request: {e}")
except APIError as e:
    print(f"API internal error: {e}")
except ServiceUnavailableError:
    print("Service temporarily unavailable")
```

## License

This project is provided under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! We look forward to bug reports, feature requests, pull requests, and any other forms of contribution. For details, please refer to the [contribution guidelines](docs/contributing.md).

## Contact

If you have questions or issues, please report them on [GitHub Issues](https://github.com/yourusername/relation-client/issues).