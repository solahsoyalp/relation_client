# チケット管理

Re:lation API Pythonクライアントを使用すると、Re:lationのチケット（問い合わせ）を効率的に管理できます。このドキュメントでは、チケットの検索、取得、更新、応対メモの作成など、チケット関連の操作方法について説明します。

## チケットの検索

### 基本的な検索

特定の受信箱内のチケットを検索するには、以下のように`search`メソッドを使用します：

```python
tickets = client.tickets.search(
    message_box_id=123,  # 受信箱ID
    per_page=20,         # 1ページあたりの件数
    page=1               # ページ番号
)

for ticket in tickets:
    print(f"ID: {ticket.ticket_id}, タイトル: {ticket.title}, ステータス: {ticket.status_cd}")
```

### 検索条件の指定

様々な条件でチケットを検索することができます：

```python
from relation_client import STATUS_OPEN, STATUS_ONGOING, METHOD_MAIL, METHOD_LINE

# ステータスで検索（未対応のチケット）
tickets = client.tickets.search(
    message_box_id=123,
    status_cds=[STATUS_OPEN]
)

# 複数のステータスで検索（未対応または対応中のチケット）
tickets = client.tickets.search(
    message_box_id=123,
    status_cds=[STATUS_OPEN, STATUS_ONGOING]
)

# チャネルで検索（メールによる問い合わせ）
tickets = client.tickets.search(
    message_box_id=123,
    method_cds=[METHOD_MAIL]
)

# 複数のチャネルで検索（メールまたはLINEによる問い合わせ）
tickets = client.tickets.search(
    message_box_id=123,
    method_cds=[METHOD_MAIL, METHOD_LINE]
)

# タイトルや本文に特定のキーワードを含むチケットを検索
tickets = client.tickets.search(
    message_box_id=123,
    keyword='返品'
)

# 担当者で検索
tickets = client.tickets.search(
    message_box_id=123,
    assignee='yamada'  # 担当者のメンション名
)

# 複数の条件を組み合わせて検索
tickets = client.tickets.search(
    message_box_id=123,
    status_cds=[STATUS_OPEN, STATUS_ONGOING],
    method_cds=[METHOD_MAIL],
    keyword='返品',
    assignee='yamada'
)
```

### 詳細な検索パラメータ

`search`メソッドでは、以下のパラメータを使用できます：

| パラメータ | 型 | 説明 |
|------------|------|-----------|
| `message_box_id` | int | **必須** 受信箱ID |
| `status_cds` | list | ステータスコードのリスト |
| `method_cds` | list | チャネルコードのリスト |
| `keyword` | str | タイトルや本文に含まれるキーワード |
| `assignee` | str | 担当者のメンション名 |
| `customer_id` | int | 顧客ID |
| `customer_group_id` | int | アドレス帳ID |
| `system_id1` | str | 顧客コード |
| `case_category_ids` | list | チケット分類IDのリスト |
| `label_ids` | list | ラベルIDのリスト |
| `color_cd` | str | 色コード |
| `created_at_from` | str | 作成日時の開始日（ISO 8601形式） |
| `created_at_to` | str | 作成日時の終了日（ISO 8601形式） |
| `updated_at_from` | str | 更新日時の開始日（ISO 8601形式） |
| `updated_at_to` | str | 更新日時の終了日（ISO 8601形式） |
| `per_page` | int | 1ページあたりの件数（デフォルト: 20） |
| `page` | int | ページ番号（デフォルト: 1） |

## チケットの取得

特定のチケットを取得するには：

```python
ticket = client.tickets.get(
    message_box_id=123,  # 受信箱ID
    ticket_id=456        # チケットID
)

print(f"チケット情報: ID={ticket.ticket_id}, タイトル={ticket.title}")
print(f"ステータス: {ticket.status_cd}, 担当者: {ticket.assignee}")
print(f"作成日時: {ticket.created_at}, 更新日時: {ticket.updated_at}")

# チケット内のメッセージを表示
for message in ticket.messages:
    print(f"メッセージID: {message.message_id}")
    print(f"送信者: {message.from_}")  # 'from' はPythonの予約語のため 'from_' として参照
    print(f"宛先: {message.to}")
    print(f"件名: {message.title}")
    print(f"本文: {message.body}")
    print(f"送信日時: {message.sent_at}")
    print(f"チャネル: {message.method_cd}")
    
    # 添付ファイルがある場合
    if message.attachments:
        print("添付ファイル:")
        for attachment in message.attachments:
            print(f"  - {attachment.file_name} ({attachment.content_type})")
    
    print("---")
```

## チケットの更新

### 基本的な更新

チケットを更新するには：

```python
from relation_client import STATUS_CLOSED, COLOR_RED

client.tickets.update(
    message_box_id=123,  # 受信箱ID
    ticket_id=456,       # チケットID
    status_cd=STATUS_CLOSED,  # ステータス（対応完了）
    color_cd=COLOR_RED,       # 色（赤）
    assignee="yamada"         # 担当者のメンション名
)

print("チケット更新完了")
```

### チケット分類やラベルの設定

チケットに分類やラベルを設定するには：

```python
client.tickets.update(
    message_box_id=123,
    ticket_id=456,
    case_category_ids=[1, 2],  # チケット分類IDのリスト（複数指定可能）
    label_ids=[3, 4]           # ラベルIDのリスト（複数指定可能）
)

print("チケットの分類とラベルを更新しました")
```

### メモの更新

チケットのメモを更新するには：

```python
client.tickets.update(
    message_box_id=123,
    ticket_id=456,
    memo="お客様は急ぎの対応を希望しています。明日までに回答が必要です。"
)

print("チケットのメモを更新しました")
```

## 応対メモの作成

### 新規チケットとして応対メモを作成

```python
from relation_client import STATUS_OPEN, ICON_MEETING
from datetime import datetime
import pytz

# 現在時刻（日本時間）
jst = pytz.timezone('Asia/Tokyo')
now = datetime.now(jst).isoformat()

# 応対メモを作成（新規チケット）
result = client.tickets.create_record(
    message_box_id=123,       # 受信箱ID
    subject="お問い合わせ対応",  # 件名
    operated_at=now,          # 応対日時
    duration=30,              # 応対時間（分）
    body="お客様からの問い合わせに対応しました。次回は来週フォローアップの連絡をします。",  # 本文
    status_cd=STATUS_OPEN,    # ステータス（未対応）
    icon_cd=ICON_MEETING,     # 応対種別（会議）
    customer_email="customer@example.com",  # 顧客メールアドレス
    operator="tanaka"         # 応対者のメンション名
)

print(f"応対メモ作成完了: メッセージID={result['message_id']}, チケットID={result['ticket_id']}")
```

### 既存チケットに応対メモを追加

```python
from relation_client import ICON_CALLED_PHONE

# 既存チケットに応対メモを追加
result = client.tickets.create_record(
    message_box_id=123,        # 受信箱ID
    subject="フォローアップ対応",  # 件名
    operated_at=now,           # 応対日時
    duration=15,               # 応対時間（分）
    body="お客様にフォローアップの連絡をしました。",  # 本文
    ticket_id=456,             # 既存チケットID
    icon_cd=ICON_CALLED_PHONE  # 応対種別（架電）
)

print(f"応対メモ追加完了: メッセージID={result['message_id']}")
```

## メールの送信

### 新規メール送信

```python
from relation_client import STATUS_OPEN

# 新規メール送信
result = client.mails.send(
    message_box_id=123,      # 受信箱ID
    mail_account_id=1,       # 送信メールアカウントID
    to="customer@example.com",  # 宛先
    subject="お問い合わせありがとうございます",  # 件名
    body="いつもご利用ありがとうございます。\n...",  # 本文
    status_cd=STATUS_OPEN,   # ステータス
    cc="team@example.com",   # CC
    bcc="archive@example.com",  # BCC
    is_html=False,           # HTMLメールかどうか
    pending_reason_id=None   # 保留理由ID
)

print(f"メール送信完了: メッセージID={result['message_id']}, チケットID={result['ticket_id']}")
```

### メール返信

```python
# メール返信
result = client.mails.reply(
    message_box_id=123,      # 受信箱ID
    message_id=456,          # 返信元メッセージID
    mail_account_id=1,       # 送信メールアカウントID
    to="customer@example.com",  # 宛先
    subject="Re: お問い合わせについて",  # 件名
    body="お問い合わせいただきありがとうございます。\n...",  # 本文
    status_cd=STATUS_OPEN,   # ステータス
    cc="team@example.com",   # CC
    is_html=False            # HTMLメールかどうか
)

print(f"メール返信完了: メッセージID={result['message_id']}")
```

### メール下書き作成

```python
# メール下書き作成（新規）
result = client.mails.draft(
    message_box_id=123,      # 受信箱ID
    mail_account_id=1,       # 送信メールアカウントID
    to="customer@example.com",  # 宛先
    subject="お問い合わせありがとうございます",  # 件名
    body="いつもご利用ありがとうございます。\n下書き段階のメールです。",  # 本文
    is_html=False            # HTMLメールかどうか
)

print(f"メール下書き作成完了: メッセージID={result['message_id']}, チケットID={result['ticket_id']}")

# メール下書き作成（返信）
result = client.mails.draft(
    message_box_id=123,      # 受信箱ID
    message_id=456,          # 返信元メッセージID
    mail_account_id=1,       # 送信メールアカウントID
    to="customer@example.com",  # 宛先
    subject="Re: お問い合わせについて",  # 件名
    body="お問い合わせいただきありがとうございます。\n下書きの返信です。",  # 本文
    is_html=True             # HTMLメールにする場合
)

print(f"返信メール下書き作成完了: メッセージID={result['message_id']}")
```

## チケットの保留/スヌーズ

チケットを保留状態にし、特定の日時に再表示（スヌーズ）させるには：

```python
from relation_client import SNOOZE_TODAY, SNOOZE_TOMORROW, SNOOZE_NEXT_WEEK

# 今日の終業時間にスヌーズ
client.tickets.update(
    message_box_id=123,
    ticket_id=456,
    status_cd="ongoing",      # 保留
    pending_reason_id=1,      # スヌーズ設定のある保留理由ID
    snooze_term=SNOOZE_TODAY  # 今日の終業時間
)

# 明日の午前中にスヌーズ
client.tickets.update(
    message_box_id=123,
    ticket_id=456,
    status_cd="ongoing",        # 保留
    pending_reason_id=1,        # スヌーズ設定のある保留理由ID
    snooze_term=SNOOZE_TOMORROW # 明日の午前中
)

# 来週の月曜日にスヌーズ
client.tickets.update(
    message_box_id=123,
    ticket_id=456,
    status_cd="ongoing",          # 保留
    pending_reason_id=1,          # スヌーズ設定のある保留理由ID
    snooze_term=SNOOZE_NEXT_WEEK  # 来週の月曜日
)

# 特定の日時にスヌーズ
client.tickets.update(
    message_box_id=123,
    ticket_id=456,
    status_cd="ongoing",           # 保留
    pending_reason_id=1,           # スヌーズ設定のある保留理由ID
    snooze_term="2023-12-25T09:00:00+09:00"  # 指定した日時（ISO 8601形式）
)

print("チケットを保留状態に更新しました")
```

## チケット情報の属性

チケットオブジェクトには以下の属性があります：

| 属性 | 型 | 説明 |
|------|------|-----------|
| `ticket_id` | int | チケットID |
| `title` | str | チケットのタイトル |
| `status_cd` | str | ステータスコード |
| `color_cd` | str | 色コード |
| `assignee` | str | 担当者のメンション名 |
| `case_category_ids` | list | チケット分類IDのリスト |
| `label_ids` | list | ラベルIDのリスト |
| `customer_id` | int | 顧客ID |
| `customer_group_id` | int | アドレス帳ID |
| `system_id1` | str | 顧客コード |
| `messages` | list | メッセージのリスト |
| `memo` | str | メモ |
| `created_at` | str | 作成日時 |
| `updated_at` | str | 更新日時 |
| `deleted_at` | str | 削除日時 |

## メッセージ情報の属性

メッセージオブジェクトには以下の属性があります：

| 属性 | 型 | 説明 |
|------|------|-----------|
| `message_id` | int | メッセージID |
| `from_` | str | 送信者 |
| `to` | str | 宛先 |
| `cc` | str | CC |
| `bcc` | str | BCC |
| `title` | str | 件名 |
| `body` | str | 本文 |
| `html_body` | str | HTML形式の本文 |
| `method_cd` | str | チャネルコード |
| `sent_at` | str | 送信日時 |
| `is_outbound` | bool | 送信メッセージかどうか |
| `attachments` | list | 添付ファイルのリスト |

## 定数

ライブラリには、チケット操作に使用できる便利な定数が定義されています：

### ステータスコード

```python
from relation_client import (
    STATUS_OPEN,       # 未対応
    STATUS_ONGOING,    # 対応中
    STATUS_PENDING,    # 保留
    STATUS_RESOLVED,   # 解決済み
    STATUS_CLOSED      # 完了
)
```

### チャネルコード

```python
from relation_client import (
    METHOD_MAIL,          # メール
    METHOD_CHAT_PLUS,     # ChatPlus
    METHOD_YAHOO,         # Yahoo!ショッピング
    METHOD_RECORD,        # 応対メモ
    METHOD_LINE,          # LINE
    METHOD_R_MESSE,       # 楽天R-Messe
    METHOD_WEB_CHAT       # ウェブチャット
)
```

### 色コード

```python
from relation_client import (
    COLOR_RED,      # 赤
    COLOR_YELLOW,   # 黄
    COLOR_GREEN,    # 緑
    COLOR_BLUE,     # 青
    COLOR_PURPLE,   # 紫
    COLOR_BLACK     # 黒
)
```

### 応対種別アイコン

```python
from relation_client import (
    ICON_RECEIVED_PHONE,   # 着信
    ICON_CALLED_PHONE,     # 発信
    ICON_VISIT,            # 来店
    ICON_MEETING,          # 会議
    ICON_FAX,              # FAX
    ICON_MEMO              # メモ
)
```

### スヌーズ設定

```python
from relation_client import (
    SNOOZE_TODAY,        # 今日の終業時間
    SNOOZE_TOMORROW,     # 明日の午前中
    SNOOZE_NEXT_WEEK     # 来週の月曜日
)
```

## エラーハンドリング

チケット操作中に発生する可能性のあるエラーを適切に処理するには：

```python
from relation_client.exceptions import (
    ResourceNotFoundError, InvalidRequestError, PermissionError
)

try:
    # 存在しないチケットIDで検索
    ticket = client.tickets.get(
        message_box_id=123,
        ticket_id=999999
    )
except ResourceNotFoundError:
    print("指定されたチケットが見つかりません")
except PermissionError:
    print("このチケットにアクセスする権限がありません")
except InvalidRequestError as e:
    print(f"リクエストが無効です: {e}")
```

## バッチ処理

多数のチケットを処理する場合は、ページネーションを活用します：

```python
from relation_client import STATUS_OPEN

page = 1
per_page = 50
total_processed = 0

# すべての未対応チケットを処理
while True:
    tickets = client.tickets.search(
        message_box_id=123,
        status_cds=[STATUS_OPEN],
        per_page=per_page,
        page=page
    )
    
    # 結果が空ならループを終了
    if not tickets:
        break
        
    for ticket in tickets:
        # チケット情報の処理
        process_ticket(ticket)
        total_processed += 1
    
    print(f"{total_processed}件処理しました")
    page += 1
```

## 関連情報

- [顧客管理](./customers.md)
- [チャット機能](./chats.md)
- [テンプレート](./templates.md)
- [添付ファイル](./attachments.md)
- [エラーハンドリング](./error_handling.md) 