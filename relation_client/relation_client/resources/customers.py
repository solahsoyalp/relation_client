"""
コンタクト (customer) リソースモジュール

このモジュールは、Re:lation APIのコンタクト (customer) リソースに対応するクラスを提供します。
"""

from typing import Dict, Any, List, Optional, Union, cast

from ..models import Customer


class CustomerResource:
    """コンタクト (customer) リソースクラス

    このクラスは、コンタクト (customer) リソースに関連するすべてのAPIメソッドを提供します。
    """

    def __init__(self, client):
        """CustomerResourceを初期化します

        Args:
            client: RelationClientインスタンス
        """
        self.client = client

    def search(
        self,
        customer_group_id: int,
        customer_ids: Optional[List[int]] = None,
        gender_cds: Optional[List[int]] = None,
        system_id1s: Optional[List[str]] = None,
        default_assignees: Optional[List[str]] = None,
        emails: Optional[List[str]] = None,
        tels: Optional[List[str]] = None,
        badge_ids: Optional[List[int]] = None,
        per_page: int = 10,
        page: int = 1
    ) -> List[Customer]:
        """顧客を検索します

        Args:
            customer_group_id: アドレス帳ID
            customer_ids: 顧客IDの配列
            gender_cds: 性別コードの配列 (1: 男性, 2: 女性, 9: 不明)
            system_id1s: 顧客コードの配列
            default_assignees: 担当者のメンション名の配列
            emails: メールアドレスの配列（部分一致検索対応）
            tels: 電話番号の配列（部分一致検索対応）
            badge_ids: バッジIDの配列
            per_page: ページごとの件数 (1-50)
            page: ページ番号 (1以上)

        Returns:
            Customer オブジェクトのリスト
        """
        params: Dict[str, Any] = {
            'per_page': per_page,
            'page': page
        }

        # オプションパラメータの設定
        if customer_ids:
            params['customer_ids[]'] = customer_ids
        if gender_cds:
            params['gender_cds[]'] = gender_cds
        if system_id1s:
            params['system_id1s[]'] = system_id1s
        if default_assignees:
            params['default_assignees[]'] = default_assignees
        if emails:
            params['emails[]'] = emails
        if tels:
            params['tels[]'] = tels
        if badge_ids:
            params['badge_ids[]'] = badge_ids

        # APIリクエスト実行
        response = self.client.get(
            f'customer_groups/{customer_group_id}/customers/search',
            params=params
        )

        # レスポンスからCustomerオブジェクトのリストを作成
        customers = []
        for customer_data in response:
            customers.append(Customer.from_dict(customer_data))

        return customers

    def create(
        self,
        customer_group_id: int,
        last_name: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name_kana: Optional[str] = None,
        first_name_kana: Optional[str] = None,
        company_name: Optional[str] = None,
        title: Optional[str] = None,
        url: Optional[str] = None,
        gender_cd: Optional[int] = None,
        default_assignee: Optional[str] = None,
        emails: Optional[List[Dict[str, str]]] = None,
        archived_emails: Optional[List[Dict[str, str]]] = None,
        tels: Optional[List[Dict[str, str]]] = None,
        archived_tels: Optional[List[Dict[str, str]]] = None,
        badge_ids: Optional[List[int]] = None,
        system_id1: Optional[str] = None,
    ) -> Customer:
        """顧客を登録します

        Args:
            customer_group_id: アドレス帳ID
            last_name: 姓
            first_name: 名
            last_name_kana: 姓（カナ）
            first_name_kana: 名（カナ）
            company_name: 会社名
            title: 役職
            url: URL
            gender_cd: 性別コード (1: 男性, 2: 女性, 9: 不明)
            default_assignee: 担当者のメンション名
            emails: メールアドレスの配列 例: [{"email": "test@example.com"}]
            archived_emails: アーカイブメールアドレスの配列
            tels: 電話番号の配列 例: [{"tel": "09000000000"}]
            archived_tels: アーカイブ電話番号の配列
            badge_ids: バッジIDの配列
            system_id1: 顧客コード

        Returns:
            作成されたCustomerオブジェクト
        """
        # リクエストデータの準備
        data: Dict[str, Any] = {}

        # オプションパラメータの設定
        if last_name is not None:
            data['last_name'] = last_name
        if first_name is not None:
            data['first_name'] = first_name
        if last_name_kana is not None:
            data['last_name_kana'] = last_name_kana
        if first_name_kana is not None:
            data['first_name_kana'] = first_name_kana
        if company_name is not None:
            data['company_name'] = company_name
        if title is not None:
            data['title'] = title
        if url is not None:
            data['url'] = url
        if gender_cd is not None:
            data['gender_cd'] = gender_cd
        if default_assignee is not None:
            data['default_assignee'] = default_assignee
        if emails is not None:
            data['emails'] = emails
        if archived_emails is not None:
            data['archived_emails'] = archived_emails
        if tels is not None:
            data['tels'] = tels
        if archived_tels is not None:
            data['archived_tels'] = archived_tels
        if badge_ids is not None:
            data['badge_ids'] = badge_ids
        if system_id1 is not None:
            data['system_id1'] = system_id1

        # APIリクエスト実行
        response = self.client.post(
            f'customer_groups/{customer_group_id}/customers/create',
            data=data
        )

        # レスポンスからCustomerオブジェクトを作成
        return Customer.from_dict(response)

    def get_by_system_id1(
        self,
        customer_group_id: int,
        system_id1: str
    ) -> Customer:
        """顧客を取得します (system_id1 をキーに)

        Args:
            customer_group_id: アドレス帳ID
            system_id1: 顧客コード

        Returns:
            Customerオブジェクト
        """
        # APIリクエスト実行
        response = self.client.get(
            f'customer_groups/{customer_group_id}/customers/system_id1/{system_id1}'
        )

        # レスポンスからCustomerオブジェクトを作成
        return Customer.from_dict(response)

    def get_by_email(
        self,
        customer_group_id: int,
        email: str
    ) -> Customer:
        """顧客を取得します (email をキーに)

        Args:
            customer_group_id: アドレス帳ID
            email: メールアドレス

        Returns:
            Customerオブジェクト
        """
        # APIリクエスト実行
        response = self.client.get(
            f'customer_groups/{customer_group_id}/customers/email/{email}'
        )

        # レスポンスからCustomerオブジェクトを作成
        return Customer.from_dict(response)

    def update_by_system_id1(
        self,
        customer_group_id: int,
        system_id1: str,
        last_name: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name_kana: Optional[str] = None,
        first_name_kana: Optional[str] = None,
        company_name: Optional[str] = None,
        title: Optional[str] = None,
        url: Optional[str] = None,
        gender_cd: Optional[int] = None,
        default_assignee: Optional[str] = None,
        emails: Optional[List[Dict[str, str]]] = None,
        archived_emails: Optional[List[Dict[str, str]]] = None,
        tels: Optional[List[Dict[str, str]]] = None,
        archived_tels: Optional[List[Dict[str, str]]] = None,
        badge_ids: Optional[List[int]] = None,
    ) -> Customer:
        """顧客を更新します (system_id1 をキーに)

        Args:
            customer_group_id: アドレス帳ID
            system_id1: 顧客コード
            last_name: 姓
            first_name: 名
            last_name_kana: 姓（カナ）
            first_name_kana: 名（カナ）
            company_name: 会社名
            title: 役職
            url: URL
            gender_cd: 性別コード (1: 男性, 2: 女性, 9: 不明)
            default_assignee: 担当者のメンション名
            emails: メールアドレスの配列
            archived_emails: アーカイブメールアドレスの配列
            tels: 電話番号の配列
            archived_tels: アーカイブ電話番号の配列
            badge_ids: バッジIDの配列

        Returns:
            更新されたCustomerオブジェクト
        """
        # リクエストデータの準備
        data: Dict[str, Any] = {}

        # オプションパラメータの設定
        if last_name is not None:
            data['last_name'] = last_name
        if first_name is not None:
            data['first_name'] = first_name
        if last_name_kana is not None:
            data['last_name_kana'] = last_name_kana
        if first_name_kana is not None:
            data['first_name_kana'] = first_name_kana
        if company_name is not None:
            data['company_name'] = company_name
        if title is not None:
            data['title'] = title
        if url is not None:
            data['url'] = url
        if gender_cd is not None:
            data['gender_cd'] = gender_cd
        if default_assignee is not None:
            data['default_assignee'] = default_assignee
        if emails is not None:
            data['emails'] = emails
        if archived_emails is not None:
            data['archived_emails'] = archived_emails
        if tels is not None:
            data['tels'] = tels
        if archived_tels is not None:
            data['archived_tels'] = archived_tels
        if badge_ids is not None:
            data['badge_ids'] = badge_ids

        # APIリクエスト実行
        response = self.client.put(
            f'customer_groups/{customer_group_id}/customers/system_id1/{system_id1}',
            data=data
        )

        # レスポンスからCustomerオブジェクトを作成
        return Customer.from_dict(response)

    def update_by_email(
        self,
        customer_group_id: int,
        email: str,
        last_name: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name_kana: Optional[str] = None,
        first_name_kana: Optional[str] = None,
        company_name: Optional[str] = None,
        title: Optional[str] = None,
        url: Optional[str] = None,
        gender_cd: Optional[int] = None,
        default_assignee: Optional[str] = None,
        emails: Optional[List[Dict[str, str]]] = None,
        archived_emails: Optional[List[Dict[str, str]]] = None,
        tels: Optional[List[Dict[str, str]]] = None,
        archived_tels: Optional[List[Dict[str, str]]] = None,
        badge_ids: Optional[List[int]] = None,
        system_id1: Optional[str] = None,
    ) -> Customer:
        """顧客を更新します (email をキーに)

        Args:
            customer_group_id: アドレス帳ID
            email: メールアドレス
            last_name: 姓
            first_name: 名
            last_name_kana: 姓（カナ）
            first_name_kana: 名（カナ）
            company_name: 会社名
            title: 役職
            url: URL
            gender_cd: 性別コード (1: 男性, 2: 女性, 9: 不明)
            default_assignee: 担当者のメンション名
            emails: メールアドレスの配列
            archived_emails: アーカイブメールアドレスの配列
            tels: 電話番号の配列
            archived_tels: アーカイブ電話番号の配列
            badge_ids: バッジIDの配列
            system_id1: 顧客コード

        Returns:
            更新されたCustomerオブジェクト
        """
        # リクエストデータの準備
        data: Dict[str, Any] = {}

        # オプションパラメータの設定
        if last_name is not None:
            data['last_name'] = last_name
        if first_name is not None:
            data['first_name'] = first_name
        if last_name_kana is not None:
            data['last_name_kana'] = last_name_kana
        if first_name_kana is not None:
            data['first_name_kana'] = first_name_kana
        if company_name is not None:
            data['company_name'] = company_name
        if title is not None:
            data['title'] = title
        if url is not None:
            data['url'] = url
        if gender_cd is not None:
            data['gender_cd'] = gender_cd
        if default_assignee is not None:
            data['default_assignee'] = default_assignee
        if emails is not None:
            data['emails'] = emails
        if archived_emails is not None:
            data['archived_emails'] = archived_emails
        if tels is not None:
            data['tels'] = tels
        if archived_tels is not None:
            data['archived_tels'] = archived_tels
        if badge_ids is not None:
            data['badge_ids'] = badge_ids
        if system_id1 is not None:
            data['system_id1'] = system_id1

        # APIリクエスト実行
        response = self.client.put(
            f'customer_groups/{customer_group_id}/customers/email/{email}',
            data=data
        )

        # レスポンスからCustomerオブジェクトを作成
        return Customer.from_dict(response)

    def delete_by_system_id1(
        self,
        customer_group_id: int,
        system_id1: str
    ) -> None:
        """顧客を削除します (system_id1 をキーに)

        Args:
            customer_group_id: アドレス帳ID
            system_id1: 顧客コード
        """
        # APIリクエスト実行
        self.client.delete(
            f'customer_groups/{customer_group_id}/customers/system_id1/{system_id1}'
        )

    def delete_by_email(
        self,
        customer_group_id: int,
        email: str
    ) -> None:
        """顧客を削除します (email をキーに)

        Args:
            customer_group_id: アドレス帳ID
            email: メールアドレス
        """
        # APIリクエスト実行
        self.client.delete(
            f'customer_groups/{customer_group_id}/customers/email/{email}'
        ) 