# AI_WORK_STATE

- Project: C# Learning Lab
- Version: 5.0.0 / 図解・実例版
- Input: C-study_detailed_release(1).zip
- Delivery: 公開用ZIP + 編集用ZIP
- Repository operations: none
- Current work: サイト改修済み。最終配布ファイルの状態は validation/visual/release-manifest.json を参照。

## 完了

80ページ、8章32レッスン、詳細解説32ページ。32SVGを64箇所へ配置し、64実例を追加。96演習・160問・180語は維持。目次は左の階層、用語は右。不要文言を整理し、強調・コード装飾・.cs保存を追加。

構造検査: PASS、6,442ローカル参照、エラー0。
DOM表示・操作と図版・コードの静的検査: 213/213 PASS。Chromiumのインメモリ読み込み、保存領域はテスト専用の代替。

## 未実装・未検証

ブラウザー内C#ランナーは未実装。.NET SDK不足と外部取得制約によりビルド・実行未検証。実オリジン永続保存、実機Safari/iPhone/iPad、実公開も未検証。無料枠で不可能と判断したわけではない。

## 正本

content/visual/lessons.json、content/visual/copy-edits.json、content/deep/、content/guides/、content/templates/、scripts/build_visual.py、scripts/visual_components.py、assets/css/visual.css、assets/js/expanded.js、assets/js/visual.js。

## 再開

NEXT_WORK.md → docs/VALIDATION.md → docs/MAINTENANCE.md の順に読み、実SDK検証から進めます。過去版の docs/archive/v4/ を現在版の証拠として使わないでください。
