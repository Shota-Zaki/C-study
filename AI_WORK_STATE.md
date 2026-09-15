# AI_WORK_STATE

- Project: C# Learning Lab
- Version: 5.0.0 / 図解・実例版
- Input: C-study_detailed_release(1).zip
- Delivery: GitHub `work` / `main` + 公開用ZIP + 編集用ZIP
- Repository operations: `work` に正本・生成物、`main` に公開物を反映済み
- Current work: サイト改修・GitHub反映・GitHub Pagesデプロイ済み。最終配布ファイルの状態は validation/visual/release-manifest.json を参照。

## 完了

80ページ、8章32レッスン、詳細解説32ページ。32SVGを64箇所へ配置し、64実例を追加。96演習・160問・180語は維持。目次は左の階層、用語は右。不要文言を整理し、強調・コード装飾・.cs保存を追加。

構造検査: PASS、6,442ローカル参照、エラー0。
DOM表示・操作と図版・コードの静的検査: 213/213 PASS。Chromiumのインメモリ読み込み、保存領域はテスト専用の代替。
GitHub `main` の公開ツリーSHAは `f66b9934f32f224a59e2384c0023c9d4f18ab4dc` で、ローカル公開物379ファイルから算出したGit tree SHAと一致。GitHub Pages deploymentも成功。

## 未実装・未検証

ブラウザー内C#ランナーは未実装。.NET SDK不足と外部取得制約によりビルド・実行未検証。GitHub Pagesへのデプロイ自体は成功済みですが、公開URLの通常ナビゲーション・実オリジン永続保存、実機Safari/iPhone/iPadは未検証です。無料枠で不可能と判断したわけではありません。

## 正本

content/visual/lessons.json、content/visual/copy-edits.json、content/deep/、content/guides/、content/templates/、scripts/build_visual.py、scripts/visual_components.py、assets/css/visual.css、assets/js/expanded.js、assets/js/visual.js。

## 再開

NEXT_WORK.md → docs/VALIDATION.md → docs/MAINTENANCE.md の順に読み、実SDK検証から進めます。過去版の docs/archive/v4/ を現在版の証拠として使わないでください。
