"""
チャットリソースのテスト

このモジュールは、ChatResourceクラスのテストを提供します。
"""
import json
import pytest
from unittest import mock

from relation_client.models import ChatPlus, Yahoo, RMesse, Line
from relation_client.resources.chats import ChatResource


class TestChatResource:
    """ChatResourceクラスのテスト"""

    @pytest.fixture
    def client_mock(self):
        """APIクライアントのモック"""
        client = mock.Mock()
        return client

    @pytest.fixture
    def chat_resource(self, client_mock):
        """ChatResourceインスタンス"""
        return ChatResource(client_mock)

    def test_get_chatplus(self, chat_resource, client_mock):
        """get_chatplus()メソッドのテスト"""
        # 準備
        message_box_id = 123
        ticket_id = 456
        message_id = 789
        client_mock.get.return_value = {
            "account": "ChatPlusアカウント",
            "account_key": "account_key_123",
            "email": "test@example.com",
            "company_name": "サンプル株式会社",
            "site": "https://example.com",
            "conversations": [
                {
                    "chatplus_conversation_id": 1,
                    "action_cd": "received",
                    "speaker_name": "顧客",
                    "sent_by": "customer",
                    "sent_at": "2021-01-05T13:31:56Z",
                    "conversation_type": "text",
                    "note": "こんにちは"
                },
                {
                    "chatplus_conversation_id": 2,
                    "action_cd": "sent",
                    "speaker_name": "担当者",
                    "sent_by": "operator",
                    "sent_at": "2021-01-05T13:32:10Z",
                    "conversation_type": "text",
                    "note": "いらっしゃいませ"
                }
            ]
        }

        # 実行
        result = chat_resource.get_chatplus(message_box_id, ticket_id, message_id)

        # 検証
        client_mock.get.assert_called_once_with(f"{message_box_id}/tickets/{ticket_id}/messages/{message_id}/chatplus")
        assert isinstance(result, ChatPlus)
        assert result.account == "ChatPlusアカウント"
        assert result.account_key == "account_key_123"
        assert result.email == "test@example.com"
        assert result.company_name == "サンプル株式会社"
        assert result.site == "https://example.com"
        assert len(result.conversations) == 2
        assert result.conversations[0].chatplus_conversation_id == 1
        assert result.conversations[0].speaker_name == "顧客"
        assert result.conversations[0].conversation_type == "text"
        assert result.conversations[0].note == "こんにちは"
        assert result.conversations[1].chatplus_conversation_id == 2
        assert result.conversations[1].speaker_name == "担当者"
        assert result.conversations[1].note == "いらっしゃいませ"

    def test_get_yahoo(self, chat_resource, client_mock):
        """get_yahoo()メソッドのテスト"""
        # 準備
        message_box_id = 123
        ticket_id = 456
        message_id = 789
        client_mock.get.return_value = {
            "account": "Yahooアカウント",
            "store_account": "store_123",
            "email": "test@example.com",
            "inquiry_status": "対応中",
            "inquiry_kind": "商品について",
            "inquiry_category": "発送について",
            "order_id": "order_123",
            "order_url": "https://example.com/order/123",
            "item_number": "item_123",
            "item_url": "https://example.com/item/123",
            "conversations": [
                {
                    "yahoo_conversation_id": 1,
                    "action_cd": "received",
                    "speaker_name": "顧客",
                    "sent_by": "customer",
                    "sent_at": "2021-01-05T13:31:56Z",
                    "conversation_type": "text",
                    "note": "商品はまだ発送されていますか？"
                }
            ]
        }

        # 実行
        result = chat_resource.get_yahoo(message_box_id, ticket_id, message_id)

        # 検証
        client_mock.get.assert_called_once_with(f"{message_box_id}/tickets/{ticket_id}/messages/{message_id}/yahoo")
        assert isinstance(result, Yahoo)
        assert result.account == "Yahooアカウント"
        assert result.store_account == "store_123"
        assert result.email == "test@example.com"
        assert result.inquiry_status == "対応中"
        assert result.inquiry_kind == "商品について"
        assert result.inquiry_category == "発送について"
        assert result.order_id == "order_123"
        assert len(result.conversations) == 1
        assert result.conversations[0].yahoo_conversation_id == 1
        assert result.conversations[0].note == "商品はまだ発送されていますか？"

    def test_get_r_messe(self, chat_resource, client_mock):
        """get_r_messe()メソッドのテスト"""
        # 準備
        message_box_id = 123
        ticket_id = 456
        message_id = 789
        client_mock.get.return_value = {
            "account": "R-Messeアカウント",
            "email": "test@example.com",
            "inquiry_status": "対応中",
            "inquiry_category": "商品について",
            "inquiry_type": "返品について",
            "inquiry_number": "inquiry_123",
            "inquiry_url": "https://example.com/inquiry/123",
            "order_number": "order_123",
            "item_number": "item_123",
            "item_name": "サンプル商品",
            "item_url": "https://example.com/item/123",
            "conversations": [
                {
                    "r_messe_conversation_id": 1,
                    "action_cd": "received",
                    "speaker_name": "顧客",
                    "sent_by": "customer",
                    "sent_at": "2021-01-05T13:31:56Z",
                    "conversation_type": "text",
                    "note": "返品手続きを教えてください"
                }
            ]
        }

        # 実行
        result = chat_resource.get_r_messe(message_box_id, ticket_id, message_id)

        # 検証
        client_mock.get.assert_called_once_with(f"{message_box_id}/tickets/{ticket_id}/messages/{message_id}/r_messe")
        assert isinstance(result, RMesse)
        assert result.account == "R-Messeアカウント"
        assert result.email == "test@example.com"
        assert result.inquiry_status == "対応中"
        assert result.inquiry_category == "商品について"
        assert result.inquiry_type == "返品について"
        assert result.inquiry_number == "inquiry_123"
        assert result.item_name == "サンプル商品"
        assert len(result.conversations) == 1
        assert result.conversations[0].r_messe_conversation_id == 1
        assert result.conversations[0].note == "返品手続きを教えてください"

    def test_get_line(self, chat_resource, client_mock):
        """get_line()メソッドのテスト"""
        # 準備
        message_box_id = 123
        ticket_id = 456
        message_id = 789
        client_mock.get.return_value = {
            "account": "LINEアカウント",
            "channel_id": "channel_123",
            "group_name": "サンプルグループ",
            "conversations": [
                {
                    "line_conversation_id": 1,
                    "action_cd": "received",
                    "speaker_name": "顧客",
                    "sent_by": "customer",
                    "sent_at": "2021-01-05T13:31:56Z",
                    "conversation_type": "text",
                    "note": "こんにちは"
                },
                {
                    "line_conversation_id": 2,
                    "action_cd": "sent",
                    "speaker_name": "担当者",
                    "sent_by": "operator",
                    "sent_at": "2021-01-05T13:32:10Z",
                    "conversation_type": "sticker",
                    "note": "スタンプを送信しました"
                }
            ]
        }

        # 実行
        result = chat_resource.get_line(message_box_id, ticket_id, message_id)

        # 検証
        client_mock.get.assert_called_once_with(f"{message_box_id}/tickets/{ticket_id}/messages/{message_id}/line")
        assert isinstance(result, Line)
        assert result.account == "LINEアカウント"
        assert result.channel_id == "channel_123"
        assert result.group_name == "サンプルグループ"
        assert len(result.conversations) == 2
        assert result.conversations[0].line_conversation_id == 1
        assert result.conversations[0].speaker_name == "顧客"
        assert result.conversations[0].note == "こんにちは"
        assert result.conversations[1].line_conversation_id == 2
        assert result.conversations[1].conversation_type == "sticker"
        assert result.conversations[1].note == "スタンプを送信しました" 