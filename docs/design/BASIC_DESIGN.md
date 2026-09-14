# Basic design

content/course.jsonとcontent/projects.jsonを正本に、Python標準ライブラリで静的HTMLを生成。本文は事前描画し、ブラウザーのスクリプトは検索・進捗・演習下書き・問題・JSON入出力・テーマに限定する。

ページ: ロードマップ、環境構築、32レッスン、制作一覧と3詳細、用語集、学習データ、404。読む→試す→解く→次へ。PCは左章ナビ/中央本文/右目次、中幅は本文内目次、狭幅は左ナビをdialogへ。

データ: 教材→ビルダー→HTML/検索索引/サンプルZIP。操作→状態検証→localStorage→画面反映。JSON→検証→確認→保存。破損や容量不足は通知し元データを保護。

公開: GitHub PagesのActionsビルドへ対応。mainはcontent/site/必要なscripts/README/公開workflow等のallowlist。設計・証跡・移行スクリプトはworkのみ。

調査: Microsoft Learn、MDN、React公式、The Odin Project、Codecademy、Qiita公式、Zenn公式を2026-09-14に確認。Learn/MDNの現在位置と見出し、Reactの例題と演習、Odinのロードマップ、Qiita/Zennの本文とCalloutを抽出。15観点と未確認事項をUI_UX_RESEARCH.mdに記録する。
