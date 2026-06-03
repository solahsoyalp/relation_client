# セキュリティポリシー

## 脆弱性の報告

セキュリティ上の問題を発見した場合は、公開 Issue ではなく、リポジトリオーナー宛に
非公開で連絡してください。

## 依存パッケージの方針

### requests と Python サポートの関係

`requests` は既知脆弱性の修正に伴い、サポートする Python バージョンを引き上げています。

| requests バージョン | requires-python | 関連する既知脆弱性 |
| --- | --- | --- |
| `< 2.32.0` | — | CVE-2023-32681 / CVE-2024-35195 |
| `2.32.4` | `>=3.8` | CVE-2024-35195 を修正済み |
| `2.32.5` | `>=3.9` | 〃 |
| `>= 2.33.0` | `>=3.10` | CVE-2026-25645 を修正済み |

本プロジェクトは Python 3.8〜3.12 をサポートするため、依存宣言で
環境マーカーを用いて、各 Python が導入可能な範囲で最も安全な `requests` を要求します。

```
requests>=2.33.0; python_version >= "3.10"
requests>=2.32.4; python_version < "3.10"
```

#### 残存リスク（重要）

`requests` の `CVE-2026-25645` 修正版（`2.33.0`）以降は **Python 3.10 以上が必須**です。
そのため **Python 3.8 / 3.9 環境では `2.33.0` を導入できず、当該脆弱性の修正を受け取れません**。
最大限のセキュリティを求める場合は、**Python 3.10 以上**の利用を推奨します。

将来 Python 3.8 / 3.9 のサポートを終了する際は、依存宣言を
`requests>=2.33.0`（マーカーなし）へ統一し、`requires-python` も `>=3.10` に
引き上げる予定です。

## 依存監査

CI で [`pip-audit`](https://github.com/pypa/pip-audit) を実行し、依存パッケージの
既知脆弱性を継続的に確認しています（`.github/workflows/ci.yml` の `audit` ジョブ）。
ローカルでも以下で実行できます。

```bash
python -m pip install pip-audit
pip-audit -r relation_client/requirements.txt
```
