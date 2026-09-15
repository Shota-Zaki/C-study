# AI_WORK_STATE

- Project: C# Learning Lab
- Version: 5.1.0 / 本文図解・単元別構成版
- Input: C-study_visual_release(1).zip
- Delivery: GitHub `work` / `main` + 公開用ZIP + 編集用ZIP
- Repository operations: `work` に正本・生成物、`main` に公開物を反映済み
- Current work: 単元別の説明順と本文途中の図解を追加し、GitHub Actionsのビルド・監査・`main` 公開・GitHub Pagesデプロイまで完了。

## 完了

80ページ、8章32レッスン、詳細解説32ページ。既存の32 SVG / 64配置と64実例、96演習・160問・180語を維持したまま、説明途中へ文脈依存の図解を212箇所追加しました。新規図解は74ページに配置し、単元ごとの説明順は24種類の構成を使用しています。

条件分岐は判定・経路・境界、配列と反復は添字・反復・更新、値型と参照型は参照関係、LINQは件数・要素型・処理段階、非同期は開始・待機・再開・合流、HTTP/Web APIは要求・検証・状態変更・応答というように、単元に合わせて図と説明順を変更しています。

ローカル検査: `scripts/build_visual.py`、`scripts/audit_visual.py`、`scripts/audit_pedagogy.py` がPASS。構造監査は80ページ、6,511ローカル参照、エラー0。教材監査は既存コード717ブロック・既存説明3,476段落を保持し、新規図解212配置を確認。

GitHub Actions `Build and publish visual release` は復元・依存導入・ビルド/監査・公開用パッケージ・`work`生成コミット・`main`公開の全ステップがsuccess。`work` の生成コミットは `60bf3ea417e91171104ef40d9f9ec44327e5007f`、`main` の公開コミットは `9e2ba2fea70e4748aa1991efb326555322b1d8c7`。GitHub Pages deploymentもsuccess。

## 未実装・未検証

ブラウザー内C#ランナーは未実装。.NET SDK不足と外部取得制約によりC#サンプルの実ビルド・実行は未検証。GitHub Pagesへのデプロイ自体は成功済みですが、公開URLの通常ナビゲーション・実オリジン永続保存、実機Safari/iPhone/iPadは未検証です。無料枠で不可能と判断したわけではありません。

## 正本

教材・生成の主要正本は `content/visual/lessons.json`、`content/visual/copy-edits.json`、`content/pedagogy/lessons.json`、`content/pedagogy/supplements.json`、`content/deep/`、`content/guides/`、`content/templates/`、`scripts/build_visual.py`、`scripts/visual_components.py`、`scripts/pedagogy.py`、`assets/css/visual.css`、`assets/css/pedagogy.css`、`assets/js/expanded.js`、`assets/js/visual.js`。

`main` のLesson 18で `data-teaching-edition="5.1"`、`assets/css/pedagogy.css` の読込、本文途中の `teaching-figure` が公開物へ入っていることを確認済みです。

## 再開

`NEXT_WORK.md` → `docs/VALIDATION.md` → `docs/MAINTENANCE.md` の順に読み、実SDK検証から進めます。過去版の `docs/archive/v4/` を現在版の証拠として使わないでください。
