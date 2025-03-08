"""
AttachmentResourceクラスのテスト

このモジュールは、AttachmentResourceクラスのメソッドをテストします。
"""
import pytest
from unittest import mock

from relation_client.resources.attachments import AttachmentResource


class TestAttachmentResource:
    """AttachmentResourceのテストクラス"""

    @pytest.fixture
    def client_mock(self):
        """APIクライアントのモック"""
        client = mock.Mock()
        client.get.return_value = {
            "url": "https://example.com/download/abc123",
            "file_name": "test_document.pdf",
            "expires_in_sec": 30
        }
        return client

    @pytest.fixture
    def attachment_resource(self, client_mock):
        """AttachmentResourceインスタンス"""
        return AttachmentResource(client_mock)

    def test_get_download_url(self, attachment_resource, client_mock):
        """get_download_url()メソッドのテスト"""
        # 実行
        result = attachment_resource.get_download_url(message_box_id=123, attachment_id=456)

        # 検証
        client_mock.get.assert_called_once_with('123/messages/attachments/456')
        assert isinstance(result, dict)
        assert "url" in result
        assert "file_name" in result
        assert "expires_in_sec" in result
        assert result["url"] == "https://example.com/download/abc123"
        assert result["file_name"] == "test_document.pdf"
        assert result["expires_in_sec"] == 30

    def test_get_download_url_error(self, attachment_resource, client_mock):
        """エラーレスポンスの場合のget_download_url()メソッドのテスト"""
        # モックの設定
        client_mock.get.return_value = {"error": "リソースが見つかりません"}
        
        # 実行
        result = attachment_resource.get_download_url(message_box_id=123, attachment_id=999)
        
        # 検証
        client_mock.get.assert_called_once_with('123/messages/attachments/999')
        assert isinstance(result, dict)
        assert "error" in result 