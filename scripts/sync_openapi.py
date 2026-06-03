#!/usr/bin/env python3
"""
OpenAPI仕様同期スクリプト

このスクリプトは、Re:lation APIの「単一の信頼できる情報源（single source of truth）」
である OpenAPI 3.0 仕様を、ドキュメントリポジトリ
`solahsoyalp/Re_lation_API_Docs_Unofficial` から必要なときにオンデマンドで取得します。

巨大なJSONをこのリポジトリにベンダリング（同梱）してしまうとGit履歴が肥大化するため、
仕様ファイルはGit管理対象外（spec/.gitignore で *.json を無視）とし、本スクリプトで
ローカルの `spec/` ディレクトリへダウンロードして利用します。

依存ライブラリは標準ライブラリ（urllib.request）のみです。

使い方:
    python3 scripts/sync_openapi.py

取得した仕様は `relation_client/tests/test_openapi_consistency.py` により、
クライアント実装との整合性チェック（スモークテスト）に使用されます。
"""

import os
import sys
import urllib.request
import urllib.error

# ドキュメントリポジトリの raw URL ベース
RAW_BASE = (
    'https://raw.githubusercontent.com/'
    'solahsoyalp/Re_lation_API_Docs_Unofficial/main/spec'
)

# ドキュメントリポジトリの spec/ ディレクトリに含まれる OpenAPI 3.0 JSON ファイル群。
# （リソースごとに分割されたOpenAPIドキュメント）
SPEC_FILES = [
    'attachment.json',
    'badge.json',
    'case_category.json',
    'chat.json',
    'comment.json',
    'contact.json',
    'customer_group.json',
    'label.json',
    'mail.json',
    'mail_account.json',
    'message_box.json',
    'pending_reason.json',
    'template.json',
    'ticket.json',
    'user.json',
]

# このスクリプトから見た spec/ ディレクトリ（リポジトリ直下）
SPEC_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'spec'
)


def download(filename, dest_dir):
    """指定したOpenAPI JSONファイルを raw URL から dest_dir へダウンロードする。"""
    url = f'{RAW_BASE}/{filename}'
    dest = os.path.join(dest_dir, filename)
    req = urllib.request.Request(url, headers={'User-Agent': 'relation-client-sync'})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read()
    with open(dest, 'wb') as f:
        f.write(data)
    return len(data)


def main():
    os.makedirs(SPEC_DIR, exist_ok=True)
    print(f'OpenAPI仕様を {RAW_BASE} から取得します')
    print(f'保存先: {SPEC_DIR}')

    failures = []
    for filename in SPEC_FILES:
        try:
            size = download(filename, SPEC_DIR)
            print(f'  OK   {filename} ({size} bytes)')
        except urllib.error.URLError as exc:
            failures.append(filename)
            print(f'  FAIL {filename}: {exc}', file=sys.stderr)

    if failures:
        print(
            f'{len(failures)} 件のファイル取得に失敗しました: {failures}',
            file=sys.stderr,
        )
        return 1

    print(f'完了: {len(SPEC_FILES)} ファイルを同期しました')
    return 0


if __name__ == '__main__':
    sys.exit(main())
