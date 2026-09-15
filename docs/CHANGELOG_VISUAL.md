# 変更箇所 — 図解・実例版

## ① 目次と用語の配置

位置: `scripts/build_visual.py`、生成される全HTMLの左右サイドバー。

修正前:

```html
<aside class="right-toc">
  <h2>このページの目次</h2>
  <nav><!-- ページ内見出し --></nav>
</aside>
<article>
  <section class="local-terms"><!-- ページ固有の用語 --></section>
</article>
```

修正後（構造の要約）:

```html
<details class="chapter-group current-chapter" open>
  <summary>Chapter 02</summary>
  <div class="lesson-item current-lesson">
    <a class="lesson-link">05 条件分岐とパターン</a>
    <nav class="lesson-toc" aria-label="このページの目次">
      <!-- ページ内見出し -->
    </nav>
  </div>
</details>
<aside class="right-toc glossary-rail">
  <details class="glossary-panel" open><!-- ページ固有の用語 --></details>
</aside>
```

理由: 章・レッスン・ページ内見出しの位置関係を左側に集約し、本文を読みながら用語定義を参照できるようにしました。既存の用語IDを残し、本文内のリンクを維持しています。

## ② 不要な案内・文言

位置: `scripts/build_visual.py` の見出し・セクション変換、`content/visual/copy-edits.json`。

修正前: 「本編から詳細解説へ」「この教材の使い方」「仕組みを理解し、書いて確かめる」などの案内、スローガン。

修正後: 対象セクションを削除し、関連する見出しは「概念・構文」「プログラムの実行手順」「条件式の評価と分岐先」など具体的な内容名に統一しました。詳細解説へのアクセスはタイトル下のタブに集約しています。

理由: 読み方の宣伝ではなく、C#の説明・図・コード・演習を本文の中心にするためです。元の技術説明を一括削除する方法は取らず、対応する言い換えと不要な案内の除去を分けています。

## ③ 図解と実例

位置: `content/visual/lessons.json`、`scripts/visual_components.py`、`assets/diagrams/`、`samples/visual/`。

修正前: 既存の説明・コード・表を中心とした構成。

修正後: 32種類のSVGと64本の独立した実例を追加。本文・詳細解説の両方に図を掲載し、実例には想定出力、処理順、値の変化、入力変更の影響、プロジェクトZIPを付けました。

理由: コードと状態変化を対応づけるためです。実例は1ファイルの断片だけでなく、対応する `.csproj` を持つ単位で配布します。

## ④ 強調とコード表示

位置: `assets/css/visual.css`、`scripts/build_visual.py` のコード装飾。

修正前:

```html
<pre><code>int total = 4200;</code></pre>
```

修正後（構造の要約）:

```html
<pre><code><span class="kt">int</span> total = <span class="mi">4200</span>;</code></pre>
```

理由: コード本文を変えずに型・文字列・キーワード・数値を色分けし、重要点には色だけでなく太さ・大きさ・ラベルも併用しました。画像・コード・表は狭い画面でそれぞれスクロールできるようにしています。

## ⑤ 演習欄

位置: `scripts/build_visual.py`、`assets/js/visual.js`。

修正前: 自動保存する下書き欄。

修正後: 自動保存を維持し、`.cs` ダウンロードを追加。保存済みの内容がない場合だけ開始コードを表示します。

理由: 実例・演習をローカルSDKへ移せるようにするためです。ブラウザー内C#ランナーは未搭載で、確認問題の採点と混同させていません。

## ⑥ 生成コマンド

位置: `scripts/run_release_audits.sh`、README、保守文書。

修正前:

```sh
python scripts/build_expanded.py
```

修正後:

```sh
python scripts/build_visual.py
```

理由: 元の詳細本文を復元してから、今回のレイアウト・用語・図解・コード装飾を毎回同じ順に適用するためです。元の生成処理は補助処理として残しています。
