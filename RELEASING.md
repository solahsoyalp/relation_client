# リリース手順

このプロジェクトは **PyPI Trusted Publisher（GitHub Actions OIDC）** により、
`v*` タグを push すると **自動で PyPI へ公開**されます。API トークンの手動管理・
`twine upload` の手動実行は不要です。

公開ワークフロー: [`.github/workflows/publish.yml`](.github/workflows/publish.yml)

---

## 一度だけ必要な設定（PyPI Trusted Publisher）

PyPI 側で、この GitHub リポジトリを「信頼できる発行元」として登録します。**初回のみ**実施します。

1. https://pypi.org/manage/project/relation-client/settings/publishing/ を開く
2. **Add a new publisher**（GitHub） に以下を入力:
   | 項目 | 値 |
   | --- | --- |
   | Owner | `solahsoyalp` |
   | Repository name | `relation_client` |
   | Workflow name | `publish.yml` |
   | Environment name | `pypi` |
3. 保存する。

> 補足: GitHub 側の Environment `pypi` は、`publish.yml` の初回実行時に自動作成されます。
> 必要に応じて GitHub の **Settings → Environments → pypi** で承認者やブランチ保護などの
> 保護ルールを追加できます（任意・推奨）。

これにより、API トークンを一切保存せずに公開できます。既存の API トークンが残っている
場合は、設定後に失効（revoke）して構いません。

---

## リリースを切る手順

1. **バージョンを更新**: `relation_client/__init__.py` の `__version__` を上げる（SemVer）。
2. **CHANGELOG を更新**: `CHANGELOG.md` の `[Unreleased]` を新バージョン節（例 `[0.4.0] - YYYY-MM-DD`）に確定する。
3. **PR を作成してマージ**: 変更を `main` にマージし、CI が green であることを確認する。
4. **タグを付けて push**:
   ```bash
   git checkout main && git pull
   git tag -a v0.4.0 -m "Release 0.4.0"
   git push origin v0.4.0
   ```
5. `publish.yml` が起動し、ビルド → `twine check` → **PyPI へ自動公開**される。
   進捗は GitHub の **Actions** タブで確認できる。
6. **GitHub Release を作成**（任意・推奨）:
   ```bash
   gh release create v0.4.0 --title "v0.4.0" --notes-file <(...)  # CHANGELOG の該当節を本文に
   ```

> バージョン番号とタグ名は一致させること（`__version__= "0.4.0"` ⇔ タグ `v0.4.0`）。
> PyPI は同一バージョンの再アップロード不可。修正が必要な場合はパッチを上げて再リリースする。

---

## ローカルでの手動公開（フォールバック）

Trusted Publisher が未設定の場合や緊急時は、従来どおり手動公開も可能です。

```bash
python -m pip install --upgrade build twine
python -m build
python -m twine check dist/*
python -m twine upload dist/*   # 要 PyPI API トークン
```

API トークンは `~/.pypirc` か環境変数（`TWINE_USERNAME=__token__` / `TWINE_PASSWORD=pypi-...`）で
渡す。**トークンをコミットやチャットに残さないこと。**
