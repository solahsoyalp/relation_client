#!/usr/bin/env python
"""
Re:lation API クライアントライブラリの基本的な使用例
"""

import os
import sys
from pprint import pprint

# パッケージのインポートパスを追加
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from relation_client import RelationClient
from relation_client.exceptions import (
    AuthenticationError, PermissionError, ResourceNotFoundError, APIError
)


def main():
    """基本的な使用例のメイン関数"""
    # 環境変数から認証情報を取得（実際の使用時は環境変数を設定してください）
    access_token = os.getenv('RELATION_ACCESS_TOKEN')
    subdomain = os.getenv('RELATION_SUBDOMAIN')

    if not access_token or not subdomain:
        print('環境変数 RELATION_ACCESS_TOKEN と RELATION_SUBDOMAIN を設定してください')
        sys.exit(1)

    # クライアントの初期化
    client = RelationClient(
        access_token=access_token,
        subdomain=subdomain
    )

    try:
        # アドレス帳の一覧取得
        print('\n--- アドレス帳一覧 ---')
        customer_groups = client.customer_groups.list()
        for group in customer_groups:
            print(f'ID: {group.customer_group_id}, 名前: {group.name}')

        if not customer_groups:
            print('アドレス帳が見つかりませんでした')
            sys.exit(1)

        # 最初のアドレス帳IDを使用
        customer_group_id = customer_groups[0].customer_group_id
        print(f'\n--- 選択したアドレス帳 ID: {customer_group_id} ---')

        # 顧客の検索
        print('\n--- 顧客検索 ---')
        customers = client.customers.search(
            customer_group_id=customer_group_id,
            per_page=5
        )
        for customer in customers:
            print(f'ID: {customer.customer_id}, 名前: {customer.last_name or ""} {customer.first_name or ""}')
            if customer.emails:
                print(f'  メール: {", ".join(e.email for e in customer.emails)}')

        # 新しい顧客の作成
        print('\n--- 顧客作成 ---')
        
        # 実際に作成する場合はコメントを外してください
        """
        new_customer = client.customers.create(
            customer_group_id=customer_group_id,
            last_name='テスト',
            first_name='太郎',
            gender_cd=1,
            emails=[{'email': 'test_taro@example.com'}],
            system_id1='TEST001'
        )
        print(f'作成された顧客: ID={new_customer.customer_id}, 名前={new_customer.last_name} {new_customer.first_name}')
        
        # 作成した顧客の取得
        retrieved_customer = client.customers.get_by_system_id1(
            customer_group_id=customer_group_id,
            system_id1='TEST001'
        )
        print(f'取得した顧客: ID={retrieved_customer.customer_id}, 名前={retrieved_customer.last_name} {retrieved_customer.first_name}')
        
        # 顧客の更新
        updated_customer = client.customers.update_by_system_id1(
            customer_group_id=customer_group_id,
            system_id1='TEST001',
            company_name='株式会社テスト'
        )
        print(f'更新された顧客: ID={updated_customer.customer_id}, 会社名={updated_customer.company_name}')
        
        # 顧客の削除
        client.customers.delete_by_system_id1(
            customer_group_id=customer_group_id,
            system_id1='TEST001'
        )
        print('顧客が削除されました')
        """

    except AuthenticationError:
        print('認証エラー: アクセストークンが無効です')
    except PermissionError:
        print('権限エラー: この操作を行う権限がありません')
    except ResourceNotFoundError:
        print('リソースが見つかりません')
    except APIError as e:
        print(f'APIエラー: {e.message}')
    except Exception as e:
        print(f'予期しないエラー: {str(e)}')


if __name__ == '__main__':
    main() 