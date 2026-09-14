# 教材の正本と再生成

## 編集するファイル

追加の詳細解説は `content/deep/01.md`〜`32.md`、補助教材は `content/guides/*.md`、用語は `content/glossary-expanded.json` が正本です。全選択肢の追加説明は `content/quiz_enrichment_*.json`、三段階演習の補強は `content/exercise-coaching-*.json` に保存しています。

`content/templates/*.html.template` と `course-original.json` は入力版の生成開始点です。HTMLテンプレートは教材を減らさずに引き継ぐための元データで、公開ページではありません。通常は追加Markdown・JSONを編集し、生成スクリプトで統合します。

生成後の `content/course.json` では、表示する問題の正本は `lessons[].questions` です。`deep.questions` は入力版の履歴データとして残しているため、再度連結して問題を増やさないでください。

表示用のローカル保存キーは `cstudy.learning.v2`、スキーマはversion 2を維持しています。32レッスンのIDと96演習の下書きキーを変える場合は、既存データの移行設計が必要です。

## 再生成

生成・監査用の依存は `scripts/requirements.txt` に記載しています。閲覧だけなら不要です。

```powershell
python scripts/build_expanded.py
python scripts/audit_csharp_code.py
python scripts/audit_expanded.py
python scripts/verify_dotnet.py --build
```

生成スクリプトは元テンプレートから公開HTMLを組み立て直し、検索用データとC#サンプルを生成します。出力HTMLを直接編集すると再生成で失われるため、正本または生成処理へ変更を戻してください。

`audit_expanded.py` は静的リンク検査、ローカルHTTP配信検査、HTML直接読み込みによるDOM表示検査を行います。この制作環境のURL制限のため、DOM方式を採用しています。新しい環境では別途、本当のHTTP URLまたはfile URLをブラウザーで開くE2E検査を追加してください。

大きな監査を画面幅単位で分ける場合は環境変数 `AUDIT_MODE=desktop` / `tablet` / `mobile` を使えます。`AUDIT_RESUME=1` は同じ成果物の中断再開専用です。教材・CSS・スクリプトを変更した後に過去のPASSを再利用しないでください。

## コードフェンス

`csharp` は独立コンソール例、`csharp-web` はWeb SDK用、`csharp-input` は入力あり、`csharp-file` はファイル操作、`csharp-error` は意図的失敗、`csharp-fragment` は部分例、`csharp-test` はテストプロジェクト用です。

`flow` / `memory` は「見出し | 説明」を一行ずつ書くとネイティブHTMLの図になります。図中のAやBは実体を区別する教材上のラベルであり、物理アドレスではありません。

図・本文・コード・想定出力を変更したときは、状態表と演習の説明にも変更が伝わっているか確認します。想定出力を実測結果へ変更するのは、本当にSDKで検証した後だけです。
