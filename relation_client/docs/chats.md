# チャット機能

Re:lation API Pythonクライアントを使用すると、様々なチャットサービスとの連携機能を活用できます。このドキュメントでは、ChatPlus、LINE、Yahoo!ショッピング、楽天R-Messeなどのチャットサービス関連の操作方法について説明します。

## 対応しているチャットサービス

Re:lation APIは以下のチャットサービスに対応しています：

- **ChatPlus** - ウェブサイト上のチャットツール
- **LINE** - LINEの公式アカウントとの連携
- **Yahoo!ショッピング** - Yahoo!ショッピングのお問い合わせ連携
- **楽天R-Messe** - 楽天市場のお問い合わせ連携
- **ウェブチャット** - Re:lationウェブチャット機能

## ChatPlusの情報取得

ChatPlusで受信したチャットの詳細情報を取得するには：

```python
# ChatPlus情報の取得
chatplus = client.chats.get_chatplus(
    message_box_id=123,  # 受信箱ID
    ticket_id=456,       # チケットID
    message_id=789       # メッセージID
)

print(f"ChatPlusアカウント: {chatplus.account}")
print(f"顧客メールアドレス: {chatplus.email}")
print(f"顧客名: {chatplus.name}")

# 会話履歴の表示
for conv in chatplus.conversations:
    print(f"発言者: {conv.speaker_name}")
    print(f"会話種別: {conv.conversation_type}")
    print(f"内容: {conv.note}")
    print(f"送信日時: {conv.sent_at}")
    print("---")

# お客様情報
if chatplus.customer_info:
    print(f"お客様情報:")
    for key, value in chatplus.customer_info.items():
        print(f"  {key}: {value}")
```

### ChatPlus会話履歴の種別

ChatPlusの会話履歴には以下の種別があります：

| 種別 | 説明 |
|------|------|
| `chatplus` | ChatPlusでの会話 |
| `memo` | オペレータによるメモ |
| `transfer` | 別のオペレータへの転送 |
| `automation` | 自動応答 |

## LINEの情報取得

LINEで受信したメッセージの詳細情報を取得するには：

```python
# LINE情報の取得
line = client.chats.get_line(
    message_box_id=123,  # 受信箱ID
    ticket_id=456,       # チケットID
    message_id=789       # メッセージID
)

print(f"LINEアカウント: {line.account}")
print(f"チャネルID: {line.channel_id}")

# グループやトークルーム情報
if line.group_id:
    print(f"グループID: {line.group_id}")
    print(f"グループ名: {line.group_name}")
elif line.room_id:
    print(f"トークルームID: {line.room_id}")

# 会話履歴の表示
for conv in line.conversations:
    print(f"発言者: {conv.speaker_name}")
    print(f"発言者ID: {conv.speaker_id}")
    print(f"メッセージ種別: {conv.message_type}")
    print(f"内容: {conv.note}")
    print(f"送信日時: {conv.sent_at}")
    
    # スタンプの場合
    if conv.message_type == 'sticker':
        print(f"  パッケージID: {conv.package_id}")
        print(f"  スタンプID: {conv.sticker_id}")
    
    # 画像や動画の場合
    if conv.media_url:
        print(f"  メディアURL: {conv.media_url}")
    
    print("---")
```

### LINEメッセージの種別

LINEメッセージには以下の種別があります：

| 種別 | 説明 |
|------|------|
| `text` | テキストメッセージ |
| `sticker` | スタンプ |
| `image` | 画像 |
| `video` | 動画 |
| `audio` | 音声 |
| `location` | 位置情報 |
| `template` | テンプレートメッセージ |
| `flex` | Flexメッセージ |

## Yahoo!ショッピングの情報取得

Yahoo!ショッピングのお問い合わせ情報を取得するには：

```python
# Yahoo!ショッピング情報の取得
yahoo = client.chats.get_yahoo(
    message_box_id=123,  # 受信箱ID
    ticket_id=456,       # チケットID
    message_id=789       # メッセージID
)

print(f"Yahoo!ショッピングアカウント: {yahoo.account}")
print(f"問い合わせID: {yahoo.inquiry_id}")
print(f"問い合わせステータス: {yahoo.inquiry_status}")
print(f"問い合わせ種別: {yahoo.inquiry_kind}")

# 商品情報
if yahoo.item:
    print(f"商品情報:")
    print(f"  商品ID: {yahoo.item.item_id}")
    print(f"  商品名: {yahoo.item.item_name}")
    print(f"  商品URL: {yahoo.item.item_url}")
    if yahoo.item.item_image_url:
        print(f"  商品画像URL: {yahoo.item.item_image_url}")

# 注文情報
if yahoo.order:
    print(f"注文情報:")
    print(f"  注文ID: {yahoo.order.order_id}")
    print(f"  注文日時: {yahoo.order.order_time}")
    print(f"  金額: {yahoo.order.price}")

# 会話履歴の表示
for conv in yahoo.conversations:
    print(f"発言者: {conv.speaker_name}")
    print(f"内容: {conv.note}")
    print(f"送信日時: {conv.sent_at}")
    print("---")
```

## 楽天R-Messeの情報取得

楽天R-Messeのお問い合わせ情報を取得するには：

```python
# R-Messe情報の取得
rmesse = client.chats.get_r_messe(
    message_box_id=123,  # 受信箱ID
    ticket_id=456,       # チケットID
    message_id=789       # メッセージID
)

print(f"R-Messeアカウント: {rmesse.account}")
print(f"問い合わせID: {rmesse.inquiry_id}")
print(f"問い合わせステータス: {rmesse.inquiry_status}")
print(f"問い合わせカテゴリ: {rmesse.inquiry_category}")

# 商品情報
if rmesse.item:
    print(f"商品情報:")
    print(f"  商品ID: {rmesse.item.item_id}")
    print(f"  商品名: {rmesse.item.item_name}")
    print(f"  商品URL: {rmesse.item.item_url}")
    if rmesse.item.item_image_url:
        print(f"  商品画像URL: {rmesse.item.item_image_url}")

# 注文情報
if rmesse.order:
    print(f"注文情報:")
    print(f"  注文ID: {rmesse.order.order_id}")
    print(f"  注文日時: {rmesse.order.order_time}")
    print(f"  金額: {rmesse.order.price}")

# 会話履歴の表示
for conv in rmesse.conversations:
    print(f"発言者: {conv.speaker_name}")
    print(f"内容: {conv.note}")
    print(f"送信日時: {conv.sent_at}")
    print("---")
```

## チャットメッセージの返信

各チャットサービスへの返信は、通常のメッセージ送信APIを使用します。

### LINEへの返信

```python
# LINEメッセージへの返信
result = client.line.reply(
    message_box_id=123,    # 受信箱ID
    message_id=789,        # 返信元メッセージID
    body="ありがとうございます。承りました。",  # 本文
    status_cd="ongoing"    # ステータス（対応中）
)

print(f"LINE返信完了: メッセージID={result['message_id']}")
```

### テキスト以外のメッセージ送信

テキスト以外のメッセージ（画像、スタンプなど）を送信する場合は、各チャットサービスの専用APIを使用します：

```python
# LINEでスタンプを送信
result = client.line.send_sticker(
    message_box_id=123,    # 受信箱ID
    ticket_id=456,         # チケットID
    package_id=1,          # パッケージID
    sticker_id=1,          # スタンプID
    status_cd="ongoing"    # ステータス（対応中）
)

print(f"LINEスタンプ送信完了: メッセージID={result['message_id']}")

# LINE画像を送信
result = client.line.send_image(
    message_box_id=123,    # 受信箱ID
    ticket_id=456,         # チケットID
    image_url="https://example.com/image.jpg",  # 画像URL
    status_cd="ongoing"    # ステータス（対応中）
)

print(f"LINE画像送信完了: メッセージID={result['message_id']}")
```

## ウェブチャットの管理

Re:lationのウェブチャット機能を利用する場合：

```python
# ウェブチャットセッションの取得
webchat = client.chats.get_web_chat(
    message_box_id=123,  # 受信箱ID
    ticket_id=456,       # チケットID
    message_id=789       # メッセージID
)

print(f"チャットID: {webchat.chat_id}")
print(f"顧客名: {webchat.customer_name}")
print(f"顧客メールアドレス: {webchat.customer_email}")

# 会話履歴の表示
for conv in webchat.conversations:
    print(f"発言者: {conv.speaker_name}")
    print(f"内容: {conv.note}")
    print(f"送信日時: {conv.sent_at}")
    print("---")

# ウェブチャットへの返信
result = client.web_chat.reply(
    message_box_id=123,    # 受信箱ID
    message_id=789,        # 返信元メッセージID
    body="ありがとうございます。承りました。",  # 本文
    status_cd="ongoing"    # ステータス（対応中）
)

print(f"ウェブチャット返信完了: メッセージID={result['message_id']}")

# ウェブチャットセッションの終了
client.web_chat.end_session(
    message_box_id=123,  # 受信箱ID
    ticket_id=456        # チケットID
)

print("ウェブチャットセッションを終了しました")
```

## チャット関連の定数

ライブラリには、チャット操作に使用できる便利な定数が定義されています：

```python
from relation_client import (
    # チャネルコード
    METHOD_CHAT_PLUS,      # ChatPlus
    METHOD_LINE,           # LINE
    METHOD_YAHOO,          # Yahoo!ショッピング
    METHOD_R_MESSE,        # 楽天R-Messe
    METHOD_WEB_CHAT,       # ウェブチャット
    
    # LINEメッセージ種別
    LINE_MESSAGE_TEXT,     # テキスト
    LINE_MESSAGE_STICKER,  # スタンプ
    LINE_MESSAGE_IMAGE,    # 画像
    LINE_MESSAGE_VIDEO,    # 動画
    LINE_MESSAGE_AUDIO,    # 音声
    LINE_MESSAGE_LOCATION, # 位置情報
    
    # Yahoo!ショッピング問い合わせ種別
    YAHOO_INQUIRY_BEFORE_ORDER,  # 注文前
    YAHOO_INQUIRY_AFTER_ORDER,   # 注文後
    
    # 問い合わせステータス
    INQUIRY_STATUS_OPEN,    # 未対応
    INQUIRY_STATUS_ONGOING, # 対応中
    INQUIRY_STATUS_CLOSED   # 完了
)
```

## チャットオブジェクトの属性

各チャットサービスのオブジェクトには、以下のような属性があります：

### ChatPlusオブジェクト

| 属性 | 型 | 説明 |
|------|------|-----------|
| `account` | str | ChatPlusアカウント名 |
| `email` | str | 顧客メールアドレス |
| `name` | str | 顧客名 |
| `conversations` | list | 会話履歴のリスト |
| `customer_info` | dict | お客様情報 |

### LINEオブジェクト

| 属性 | 型 | 説明 |
|------|------|-----------|
| `account` | str | LINEアカウント名 |
| `channel_id` | str | チャネルID |
| `user_id` | str | ユーザーID |
| `group_id` | str | グループID（グループの場合） |
| `group_name` | str | グループ名（グループの場合） |
| `room_id` | str | トークルームID（トークルームの場合） |
| `conversations` | list | 会話履歴のリスト |

### Yahoo!ショッピングオブジェクト

| 属性 | 型 | 説明 |
|------|------|-----------|
| `account` | str | Yahoo!ショッピングアカウント名 |
| `inquiry_id` | str | 問い合わせID |
| `inquiry_status` | str | 問い合わせステータス |
| `inquiry_kind` | str | 問い合わせ種別 |
| `item` | object | 商品情報 |
| `order` | object | 注文情報 |
| `conversations` | list | 会話履歴のリスト |

### 楽天R-Messeオブジェクト

| 属性 | 型 | 説明 |
|------|------|-----------|
| `account` | str | 楽天R-Messeアカウント名 |
| `inquiry_id` | str | 問い合わせID |
| `inquiry_status` | str | 問い合わせステータス |
| `inquiry_category` | str | 問い合わせカテゴリ |
| `item` | object | 商品情報 |
| `order` | object | 注文情報 |
| `conversations` | list | 会話履歴のリスト |

## エラーハンドリング

チャット操作中に発生する可能性のあるエラーを適切に処理するには：

```python
from relation_client.exceptions import (
    ResourceNotFoundError, InvalidRequestError, APIError
)

try:
    # チャット情報の取得
    chatplus = client.chats.get_chatplus(
        message_box_id=123,
        ticket_id=456,
        message_id=789
    )
except ResourceNotFoundError:
    print("指定されたチャットメッセージが見つかりません")
except InvalidRequestError as e:
    print(f"リクエストが無効です: {e}")
except APIError as e:
    print(f"APIエラーが発生しました: {e}")
```

## 関連情報

- [チケット管理](./tickets.md)
- [メッセージ管理](./messages.md)
- [エラーハンドリング](./error_handling.md) 