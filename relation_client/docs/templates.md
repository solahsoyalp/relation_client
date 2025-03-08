# テンプレート管理

Re:lation API Pythonクライアントを使用すると、Re:lationの返信テンプレートを効率的に管理できます。このドキュメントでは、テンプレートの取得、検索、使用方法などについて説明します。

## テンプレートとは

テンプレートは、よく使用する定型文や回答をあらかじめ登録しておき、チケット対応時に簡単に呼び出して利用するための機能です。テンプレートを使用することで、以下のメリットがあります：

- 返信の品質と一貫性の確保
- 対応時間の短縮
- 新しいスタッフのトレーニング支援

## テンプレート一覧の取得

特定の受信箱に登録されているテンプレートの一覧を取得するには：

```python
# テンプレート一覧を取得
templates = client.templates.list(message_box_id=123)

for template in templates:
    print(f"ID: {template.template_id}, 名前: {template.template_name}")
    print(f"カテゴリ: {template.template_category_name}")
    print(f"作成者: {template.created_user}")
    print(f"作成日時: {template.created_at}")
    print(f"更新日時: {template.updated_at}")
    print("---")
```

### ページネーション

結果が多い場合は、ページネーションを使用して取得できます：

```python
# ページネーションを使用してテンプレート一覧を取得
templates = client.templates.list(
    message_box_id=123,
    per_page=20,  # 1ページあたりの件数
    page=1        # ページ番号
)
```

## テンプレートの検索

### カテゴリによる検索

特定のカテゴリに属するテンプレートを検索するには：

```python
# テンプレートカテゴリで検索
category_templates = client.templates.search(
    message_box_id=123, 
    template_category_name="お問い合わせ返信"
)

for template in category_templates:
    print(f"ID: {template.template_id}, 名前: {template.template_name}")
    print(f"件名: {template.title}")
    print(f"本文: {template.text_body}")
    print("---")
```

### キーワードによる検索

テンプレート名や本文に特定のキーワードを含むテンプレートを検索するには：

```python
# キーワードで検索
keyword_templates = client.templates.search(
    message_box_id=123, 
    keyword="返品"
)

for template in keyword_templates:
    print(f"ID: {template.template_id}, 名前: {template.template_name}")
    print(f"件名: {template.title}")
    print(f"本文: {template.text_body}")
    print("---")
```

### 複合条件による検索

カテゴリとキーワードを組み合わせて検索することもできます：

```python
# カテゴリとキーワードで検索
templates = client.templates.search(
    message_box_id=123, 
    template_category_name="お問い合わせ返信",
    keyword="返品"
)
```

### すべてのテンプレートを検索

カテゴリを指定せずにすべてのテンプレートを検索できます：

```python
# すべてのテンプレートを検索（カテゴリ指定なし）
all_templates = client.templates.search(message_box_id=123)
```

## テンプレートの詳細取得

特定のテンプレートIDを使用して、テンプレートの詳細情報を取得するには：

```python
# テンプレートの詳細を取得
template = client.templates.get(
    message_box_id=123,
    template_id=456
)

print(f"テンプレート名: {template.template_name}")
print(f"カテゴリ: {template.template_category_name}")
print(f"送信元: {template.from_}")  # 'from' はPythonの予約語のため 'from_' として参照
print(f"宛先: {template.to}")
print(f"CC: {template.cc}")
print(f"BCC: {template.bcc}")
print(f"件名: {template.title}")
print(f"HTML本文: {template.html_body}")
print(f"テキスト本文: {template.text_body}")
```

## テンプレートを使用したメール送信

テンプレートを使用してメールを送信するには、テンプレートから情報を取得し、メール送信APIに渡します：

```python
# テンプレートを取得
template = client.templates.get(
    message_box_id=123,
    template_id=456
)

# テンプレートを使用してメール送信
result = client.mails.send(
    message_box_id=123,
    mail_account_id=1,
    to="customer@example.com",
    subject=template.title,
    body=template.text_body,
    cc=template.cc,
    bcc=template.bcc,
    is_html=False,
    status_cd="ongoing"  # ステータス（対応中）
)

print(f"テンプレートを使用したメール送信完了: メッセージID={result['message_id']}")
```

### HTML形式のメール送信

テンプレートにHTML本文が含まれている場合、HTML形式のメールを送信できます：

```python
# HTML形式のメール送信
result = client.mails.send(
    message_box_id=123,
    mail_account_id=1,
    to="customer@example.com",
    subject=template.title,
    body=template.html_body,
    cc=template.cc,
    bcc=template.bcc,
    is_html=True,  # HTML形式のメール
    status_cd="ongoing"
)

print(f"HTML形式のメール送信完了: メッセージID={result['message_id']}")
```

## プレースホルダーの置換

テンプレートにはプレースホルダー（変数）を含めることができます。送信前にこれらの変数を実際の値に置換します：

```python
# テンプレート本文からプレースホルダーを置換
template_body = template.text_body
personalized_body = template_body.replace("{customer_name}", "山田様")
personalized_body = personalized_body.replace("{order_id}", "ORD-12345")
personalized_body = personalized_body.replace("{delivery_date}", "5月10日")

# 置換後の本文でメール送信
result = client.mails.send(
    message_box_id=123,
    mail_account_id=1,
    to="customer@example.com",
    subject=template.title.replace("{order_id}", "ORD-12345"),
    body=personalized_body,
    status_cd="ongoing"
)
```

### 顧客情報を使用した置換

顧客情報を使用してプレースホルダーを置換する例：

```python
# 顧客情報の取得
customer = client.customers.get_by_email(
    customer_group_id=1,
    email="customer@example.com"
)

# テンプレート本文からプレースホルダーを置換
template_body = template.text_body
personalized_body = template_body.replace("{customer_name}", f"{customer.last_name}{customer.first_name}様")
personalized_body = personalized_body.replace("{company_name}", customer.company_name or "")

# 置換後の本文でメール送信
result = client.mails.send(
    message_box_id=123,
    mail_account_id=1,
    to="customer@example.com",
    subject=template.title,
    body=personalized_body,
    status_cd="ongoing"
)
```

## テンプレートカテゴリの取得

テンプレートカテゴリの一覧を取得するには：

```python
# テンプレートカテゴリ一覧を取得
categories = client.template_categories.list(message_box_id=123)

for category in categories:
    print(f"ID: {category.template_category_id}, 名前: {category.name}")
    print(f"作成日時: {category.created_at}")
    print(f"更新日時: {category.updated_at}")
    print("---")
```

## テンプレート情報の属性

テンプレートオブジェクトには以下の属性があります：

| 属性 | 型 | 説明 |
|------|------|-----------|
| `template_id` | int | テンプレートID |
| `template_name` | str | テンプレート名 |
| `template_category_id` | int | テンプレートカテゴリID |
| `template_category_name` | str | テンプレートカテゴリ名 |
| `from_` | str | 送信元 |
| `to` | str | 宛先 |
| `cc` | str | CC |
| `bcc` | str | BCC |
| `title` | str | 件名 |
| `text_body` | str | テキスト形式の本文 |
| `html_body` | str | HTML形式の本文 |
| `created_user` | str | 作成者 |
| `created_at` | str | 作成日時 |
| `updated_at` | str | 更新日時 |

## テンプレートの作成と更新

APIを通じてテンプレートを作成・更新する機能は、現在のバージョンでは提供されていません。テンプレートの作成や更新は、Re:lationの管理画面から行う必要があります。

## エラーハンドリング

テンプレート操作中に発生する可能性のあるエラーを適切に処理するには：

```python
from relation_client.exceptions import (
    ResourceNotFoundError, InvalidRequestError, APIError
)

try:
    # テンプレートの取得
    template = client.templates.get(
        message_box_id=123,
        template_id=999999  # 存在しないテンプレートID
    )
except ResourceNotFoundError:
    print("指定されたテンプレートが見つかりません")
except InvalidRequestError as e:
    print(f"リクエストが無効です: {e}")
except APIError as e:
    print(f"APIエラーが発生しました: {e}")
```

## テンプレート活用のベストプラクティス

1. **適切なカテゴリ分類**: テンプレートは目的や用途ごとに適切なカテゴリに分類し、検索しやすくしましょう。

2. **プレースホルダーの活用**: プレースホルダーを使用して、カスタマイズ可能なテンプレートを作成しましょう。

3. **定期的な見直し**: 情報が古くなっていないか、表現が適切かなど、定期的にテンプレートの内容を見直しましょう。

4. **シンプルな設計**: 複雑なHTMLや多すぎるプレースホルダーは避け、シンプルで使いやすいテンプレートを心がけましょう。

## 関連情報

- [チケット管理](./tickets.md)
- [メール操作](./mails.md)
- [顧客管理](./customers.md) 