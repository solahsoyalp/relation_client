# 顧客管理

Re:lation API Pythonクライアントを使用すると、Re:lationの顧客情報を簡単に管理できます。このドキュメントでは、顧客情報の検索、作成、更新、削除などの操作方法について説明します。

## 顧客の検索

### 基本的な検索

特定のアドレス帳（顧客グループ）内の顧客を検索するには、以下のように`search`メソッドを使用します：

```python
customers = client.customers.search(
    customer_group_id=1,  # アドレス帳ID
    per_page=20,          # 1ページあたりの件数
    page=1                # ページ番号
)

for customer in customers:
    print(f"ID: {customer.customer_id}, 名前: {customer.last_name} {customer.first_name}")
```

### 検索条件の指定

様々な条件で顧客を検索することができます：

```python
# メールアドレスで検索
customers = client.customers.search(
    customer_group_id=1,
    emails=['example@email.com']
)

# 電話番号で検索
customers = client.customers.search(
    customer_group_id=1,
    tels=['09012345678']
)

# 顧客コード（system_id1）で検索
customers = client.customers.search(
    customer_group_id=1,
    system_id1=['CUS001', 'CUS002']
)

# 名前で検索
customers = client.customers.search(
    customer_group_id=1,
    name='山田'  # 姓名どちらでも検索可能
)

# 複数の条件を組み合わせて検索
customers = client.customers.search(
    customer_group_id=1,
    name='山田',
    gender_cd=1  # 1: 男性, 2: 女性, 9: 不明
)
```

### 詳細な検索パラメータ

`search`メソッドでは、以下のパラメータを使用できます：

| パラメータ | 型 | 説明 |
|------------|------|-----------|
| `customer_group_id` | int | **必須** アドレス帳ID |
| `emails` | list | メールアドレスのリスト |
| `tels` | list | 電話番号のリスト |
| `system_id1` | list | 顧客コードのリスト |
| `name` | str | 検索する名前（姓名どちらでも検索可能） |
| `gender_cd` | int | 性別コード（1: 男性, 2: 女性, 9: 不明） |
| `is_valid` | bool | 有効な顧客のみ検索するかどうか |
| `per_page` | int | 1ページあたりの件数（デフォルト: 20） |
| `page` | int | ページ番号（デフォルト: 1） |

## 顧客の取得

### 顧客IDによる取得

特定の顧客IDを使用して顧客情報を取得するには：

```python
customer = client.customers.get(
    customer_group_id=1,  # アドレス帳ID
    customer_id=123       # 顧客ID
)

print(f"顧客情報: {customer.last_name} {customer.first_name}")
```

### system_id1による取得

顧客コード（system_id1）を使用して顧客情報を取得するには：

```python
customer = client.customers.get_by_system_id1(
    customer_group_id=1,  # アドレス帳ID
    system_id1='CUS001'   # 顧客コード
)

print(f"顧客情報: {customer.last_name} {customer.first_name}")
```

### メールアドレスによる取得

メールアドレスを使用して顧客情報を取得するには：

```python
customer = client.customers.get_by_email(
    customer_group_id=1,           # アドレス帳ID
    email='example@email.com'      # メールアドレス
)

print(f"顧客情報: {customer.last_name} {customer.first_name}")
```

### 電話番号による取得

電話番号を使用して顧客情報を取得するには：

```python
customer = client.customers.get_by_tel(
    customer_group_id=1,    # アドレス帳ID
    tel='09012345678'       # 電話番号
)

print(f"顧客情報: {customer.last_name} {customer.first_name}")
```

## 顧客の作成

新しい顧客を作成するには、以下のように`create`メソッドを使用します：

```python
customer = client.customers.create(
    customer_group_id=1,       # アドレス帳ID
    last_name='山田',           # 姓
    first_name='太郎',          # 名
    gender_cd=1,               # 性別（1: 男性, 2: 女性, 9: 不明）
    emails=[{'email': 'yamada@example.com'}],  # メールアドレス
    tels=[{'tel': '09012345678'}],             # 電話番号
    system_id1='EMP0001'       # 顧客コード
)

print(f"登録完了: ID={customer.customer_id}")
```

### 詳細な顧客情報の登録

より詳細な顧客情報を登録することもできます：

```python
customer = client.customers.create(
    customer_group_id=1,
    last_name='山田',
    first_name='太郎',
    last_name_kana='ヤマダ',
    first_name_kana='タロウ',
    gender_cd=1,
    birthday='1980-01-01',    # 生年月日（YYYY-MM-DD形式）
    company_name='株式会社サンプル',
    department_name='営業部',
    position_name='課長',
    emails=[
        {'email': 'yamada@example.com', 'type_cd': 1},   # 1: 個人, 2: 会社
        {'email': 'taro@gmail.com', 'type_cd': 1}
    ],
    tels=[
        {'tel': '09012345678', 'type_cd': 1},   # 1: 携帯, 2: 自宅, 3: 会社, 9: その他
        {'tel': '0312345678', 'type_cd': 3}
    ],
    addresses=[
        {
            'postal_code': '1000001',
            'prefecture_cd': 13,   # 都道府県コード（13: 東京都）
            'address1': '千代田区千代田',
            'address2': '1-1',
            'address3': 'サンプルビル101',
            'type_cd': 1   # 1: 自宅, 2: 会社, 9: その他
        }
    ],
    memo='重要顧客',
    system_id1='EMP0001',
    system_id2='DEPT001'
)
```

## 顧客の更新

### 顧客IDによる更新

顧客IDを使用して顧客情報を更新するには：

```python
updated_customer = client.customers.update(
    customer_group_id=1,     # アドレス帳ID
    customer_id=123,         # 顧客ID
    company_name='株式会社サンプル更新',
    department_name='開発部',
    emails=[{'email': 'new_email@example.com'}]
)

print(f"更新完了: {updated_customer.company_name}")
```

### system_id1による更新

顧客コード（system_id1）を使用して顧客情報を更新するには：

```python
updated_customer = client.customers.update_by_system_id1(
    customer_group_id=1,       # アドレス帳ID
    system_id1='EMP0001',      # 顧客コード
    company_name='株式会社サンプル更新',
    position_name='部長',
    tels=[{'tel': '08012345678', 'type_cd': 1}]
)

print(f"更新完了: {updated_customer.company_name}")
```

## 顧客の削除

### 顧客IDによる削除

顧客IDを使用して顧客を削除するには：

```python
client.customers.delete(
    customer_group_id=1,  # アドレス帳ID
    customer_id=123       # 顧客ID
)

print("削除完了")
```

### system_id1による削除

顧客コード（system_id1）を使用して顧客を削除するには：

```python
client.customers.delete_by_system_id1(
    customer_group_id=1,    # アドレス帳ID
    system_id1='EMP0001'    # 顧客コード
)

print("削除完了")
```

## 顧客情報の属性

顧客オブジェクトには以下の属性があります：

| 属性 | 型 | 説明 |
|------|------|-----------|
| `customer_id` | int | 顧客ID |
| `last_name` | str | 姓 |
| `first_name` | str | 名 |
| `last_name_kana` | str | 姓（カナ） |
| `first_name_kana` | str | 名（カナ） |
| `gender_cd` | int | 性別コード（1: 男性, 2: 女性, 9: 不明） |
| `birthday` | str | 生年月日（YYYY-MM-DD形式） |
| `company_name` | str | 会社名 |
| `department_name` | str | 部署名 |
| `position_name` | str | 役職名 |
| `emails` | list | メールアドレスのリスト |
| `tels` | list | 電話番号のリスト |
| `addresses` | list | 住所のリスト |
| `memo` | str | メモ |
| `system_id1` | str | 顧客コード1 |
| `system_id2` | str | 顧客コード2 |
| `is_valid` | bool | 有効かどうか |
| `created_at` | str | 作成日時 |
| `updated_at` | str | 更新日時 |
| `deleted_at` | str | 削除日時 |

## エラーハンドリング

顧客情報の操作中に発生する可能性のあるエラーを適切に処理するには：

```python
from relation_client.exceptions import ResourceNotFoundError, InvalidRequestError

try:
    # 存在しない顧客コードで検索
    customer = client.customers.get_by_system_id1(
        customer_group_id=1,
        system_id1='INVALID_CODE'
    )
except ResourceNotFoundError:
    print("指定された顧客コードの顧客が見つかりません")
except InvalidRequestError as e:
    print(f"リクエストが無効です: {e}")
```

## バッチ処理

多数の顧客を処理する場合は、ページネーションを活用します：

```python
page = 1
per_page = 50
total_processed = 0

while True:
    customers = client.customers.search(
        customer_group_id=1,
        per_page=per_page,
        page=page
    )
    
    # 結果が空ならループを終了
    if not customers:
        break
        
    for customer in customers:
        # 顧客情報の処理
        process_customer(customer)
        total_processed += 1
    
    print(f"{total_processed}件処理しました")
    page += 1
```

## 関連情報

- [アドレス帳管理](./customer_groups.md)
- [チケット管理](./tickets.md)
- [エラーハンドリング](./error_handling.md) 