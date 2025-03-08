"""
アドレス帳 (customer_group) リソースモジュール

このモジュールは、Re:lation APIのアドレス帳 (customer_group) リソースに対応するクラスを提供します。
"""

from typing import Dict, Any, List, Optional, Union

from ..models import CustomerGroup


class CustomerGroupResource:
    """アドレス帳 (customer_group) リソースクラス

    このクラスは、アドレス帳 (customer_group) リソースに関連するすべてのAPIメソッドを提供します。
    """

    def __init__(self, client):
        """CustomerGroupResourceを初期化します

        Args:
            client: RelationClientインスタンス
        """
        self.client = client

    def list(self) -> List[CustomerGroup]:
        """アドレス帳の一覧を取得します

        Returns:
            CustomerGroup オブジェクトのリスト
        """
        # APIリクエスト実行
        response = self.client.get('customer_groups')
        
        # レスポンスからCustomerGroupオブジェクトのリストを作成
        customer_groups = []
        for customer_group_data in response:
            customer_groups.append(CustomerGroup.from_dict(customer_group_data))
            
        return customer_groups 