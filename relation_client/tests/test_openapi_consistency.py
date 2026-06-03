"""
OpenAPI整合性テスト

Re:lation API の OpenAPI 3.0 仕様（単一の信頼できる情報源）と、このクライアント
実装との整合性をスモークチェックします。

仕様はリポジトリに同梱せず、`scripts/sync_openapi.py` で `spec/` ディレクトリへ
オンデマンドに取得する運用です。そのため、仕様がローカルに同期されていない場合、
本テストは **スキップ** され、CIではデフォルトでネットワークアクセスを行いません。

仕様が存在する場合のみ、以下のような高価値な整合性を検証します:
  - 仕様の servers URL に含まれるAPIバージョンが
    `relation_client.constants.API_VERSION` と一致すること
  - 各リソースが利用する代表的なエンドポイントパス（例:
    `/{message_box_id}/mails`, `/{message_box_id}/tickets/search`,
    `/{message_box_id}/records`）が、仕様の paths に存在すること

軽微な表記揺れに耐えられるよう、パスはサフィックス一致で照合します。
"""

import glob
import json
import os
import re

import pytest

from relation_client import constants

# spec/ ディレクトリ（リポジトリ直下）
SPEC_DIR = os.path.join(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ),
    'spec',
)

# 各リソースが利用する代表的なエンドポイントのパスサフィックス。
# 仕様側は /{message_box_id}/... のように先頭が異なる場合があるため、
# 末尾（サフィックス）一致で照合する。
SAMPLE_PATH_SUFFIXES = [
    '/mails',
    '/tickets/search',
    '/records',
]


def _spec_files():
    """ローカルに同期されたOpenAPI JSONファイルの一覧を返す。"""
    return sorted(glob.glob(os.path.join(SPEC_DIR, '*.json')))


def _load_specs():
    """同期済みのOpenAPI仕様を読み込んで (ファイル名, dict) のリストで返す。"""
    specs = []
    for path in _spec_files():
        with open(path, encoding='utf-8') as f:
            specs.append((os.path.basename(path), json.load(f)))
    return specs


def _all_paths(specs):
    """全仕様の paths キー（エンドポイントパス文字列）を集合で返す。"""
    paths = set()
    for _name, spec in specs:
        for path in (spec.get('paths') or {}):
            paths.add(path)
    return paths


# 仕様が同期されていなければモジュール全体をスキップする
pytestmark = pytest.mark.skipif(
    not _spec_files(),
    reason='OpenAPI spec not synced; run scripts/sync_openapi.py',
)


def test_api_version_matches_spec_servers():
    """仕様の servers URL に含まれるAPIバージョンが定数と一致すること。"""
    specs = _load_specs()
    assert specs, 'OpenAPI spec not synced; run scripts/sync_openapi.py'

    checked = False
    for name, spec in specs:
        for server in (spec.get('servers') or []):
            url = server.get('url', '')
            # 例: https://{subdomain}.relationapp.jp/api/v2
            match = re.search(r'/api/(v\d+)', url)
            if match:
                checked = True
                assert match.group(1) == constants.API_VERSION, (
                    f'{name}: servers URL のAPIバージョン {match.group(1)!r} が '
                    f'constants.API_VERSION {constants.API_VERSION!r} と一致しません'
                )

    assert checked, (
        '仕様の servers URL からAPIバージョンを判定できませんでした'
    )


@pytest.mark.parametrize('suffix', SAMPLE_PATH_SUFFIXES)
def test_sample_endpoint_paths_present_in_spec(suffix):
    """代表的なエンドポイントパスが仕様の paths に存在すること（サフィックス一致）。"""
    specs = _load_specs()
    paths = _all_paths(specs)
    assert paths, '仕様に paths が見つかりませんでした'

    matched = [p for p in paths if p.endswith(suffix)]
    assert matched, (
        f'サフィックス {suffix!r} に一致するパスが仕様に見つかりませんでした。'
        f' 既知のパス例: {sorted(paths)[:10]}'
    )
