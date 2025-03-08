"""
MailResourceクラスのテスト

このモジュールは、MailResourceクラスの各メソッドをテストします。
"""
import json
import pytest
from unittest import mock

from relation_client.resources.mails import MailResource


class TestMailResource:
    """MailResourceクラスのテスト"""

    @pytest.fixture
    def client_mock(self):
        """APIクライアントのモック"""
        client = mock.Mock()
        # メール送信・返信・下書きメソッドのレスポンスを設定
        client.post.return_value = {
            "message_id": 111,
            "ticket_id": 222
        }
        
        return client

    @pytest.fixture
    def mail_resource(self, client_mock):
        """MailResourceインスタンス"""
        return MailResource(client_mock)

    def test_send(self, mail_resource, client_mock):
        """send()メソッドのテスト"""
        # 実行
        result = mail_resource.send(
            message_box_id=123,
            mail_account_id=1,
            to="test@example.com",
            subject="テストメール",
            body="これはテストメールです。",
            status_cd="open",
            cc="cc@example.com",
            bcc="bcc@example.com",
            is_html=False,
            pending_reason_id=10
        )

        # 検証
        client_mock.post.assert_called_once_with('123/mails', data={
            "status_cd": "open",
            "mail_account_id": 1,
            "to": "test@example.com",
            "subject": "テストメール",
            "body": "これはテストメールです。",
            "is_html": False,
            "cc": "cc@example.com",
            "bcc": "bcc@example.com",
            "pending_reason_id": 10
        })
        
        assert result == {
            "message_id": 111,
            "ticket_id": 222
        }

    def test_send_minimal(self, mail_resource, client_mock):
        """send()メソッドの最小パラメータでのテスト"""
        # 実行
        result = mail_resource.send(
            message_box_id=123,
            mail_account_id=1,
            to="test@example.com",
            subject="テストメール",
            body="これはテストメールです。"
        )

        # 検証
        client_mock.post.assert_called_once_with('123/mails', data={
            "status_cd": "open",
            "mail_account_id": 1,
            "to": "test@example.com",
            "subject": "テストメール",
            "body": "これはテストメールです。",
            "is_html": False
        })
        
        assert result == {
            "message_id": 111,
            "ticket_id": 222
        }

    def test_reply(self, mail_resource, client_mock):
        """reply()メソッドのテスト"""
        # 実行
        result = mail_resource.reply(
            message_box_id=123,
            message_id=456,
            mail_account_id=1,
            to="test@example.com",
            subject="Re: テストメール",
            body="返信します。",
            status_cd="open",
            cc="cc@example.com",
            bcc="bcc@example.com",
            is_html=False,
            pending_reason_id=10
        )

        # 検証
        client_mock.post.assert_called_once_with('123/mails/reply', data={
            "message_id": 456,
            "status_cd": "open",
            "mail_account_id": 1,
            "to": "test@example.com",
            "subject": "Re: テストメール",
            "body": "返信します。",
            "is_html": False,
            "cc": "cc@example.com",
            "bcc": "bcc@example.com",
            "pending_reason_id": 10
        })
        
        assert result == {
            "message_id": 111,
            "ticket_id": 222
        }

    def test_draft(self, mail_resource, client_mock):
        """draft()メソッドのテスト"""
        # 実行
        result = mail_resource.draft(
            message_box_id=123,
            mail_account_id=1,
            to="test@example.com",
            subject="下書きメール",
            body="これは下書きメールです。",
            message_id=789,
            status_cd="open",
            cc="cc@example.com",
            bcc="bcc@example.com",
            is_html=True,
            pending_reason_id=10
        )

        # 検証
        client_mock.post.assert_called_once_with('123/mails/draft', data={
            "status_cd": "open",
            "mail_account_id": 1,
            "to": "test@example.com",
            "subject": "下書きメール",
            "body": "これは下書きメールです。",
            "is_html": True,
            "message_id": 789,
            "cc": "cc@example.com",
            "bcc": "bcc@example.com",
            "pending_reason_id": 10
        })
        
        assert result == {
            "message_id": 111,
            "ticket_id": 222
        }

    def test_draft_new(self, mail_resource, client_mock):
        """draft()メソッドの新規下書きテスト"""
        # 実行
        result = mail_resource.draft(
            message_box_id=123,
            mail_account_id=1,
            to="test@example.com",
            subject="新規下書き",
            body="これは新規下書きです。"
        )

        # 検証
        client_mock.post.assert_called_once_with('123/mails/draft', data={
            "status_cd": "open",
            "mail_account_id": 1,
            "to": "test@example.com",
            "subject": "新規下書き",
            "body": "これは新規下書きです。",
            "is_html": False
        })
        
        assert result == {
            "message_id": 111,
            "ticket_id": 222
        } 