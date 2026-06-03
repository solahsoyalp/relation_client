"""
テスト共通のフィクスチャ

このモジュールは、複数のテストで共有する pytest フィクスチャを定義します。
リソース固有のデフォルト応答を持つ ``client_mock`` を各テストファイルで個別に
定義している箇所はそのまま維持し、ここでは「素のモック」と「実クライアント」の
共通フィクスチャのみを提供します。
"""
from unittest import mock

import pytest

from relation_client import RelationClient


@pytest.fixture
def client_mock():
    """リソースへ注入する素の API クライアントモック。

    既定の戻り値を持たないため、各テストで ``client_mock.get.return_value`` 等を
    設定して利用します。リソース固有のデフォルト応答が必要なテストファイルでは、
    同名のローカルフィクスチャで上書きできます。
    """
    return mock.Mock()


@pytest.fixture
def client():
    """テスト用の実 ``RelationClient`` インスタンス。

    HTTP 層（``requests.Session.request``）はテスト側で patch して利用します。
    """
    return RelationClient(access_token='test_token', subdomain='test')
