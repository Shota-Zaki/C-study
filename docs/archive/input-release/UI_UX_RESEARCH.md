# UI/UX調査・情報設計

- 調査日: 2026-09-14
- 対象: 技術ドキュメントと学習サービスの中間に位置するWeb教材
- 目的: 長い教材でも現在位置を失わず、本文を継続して読み、演習・確認・復習へ自然に進めるUIを定義する

## 1. 調査対象

1. Microsoft Learn / Microsoft Learn Training
2. MDN Web Docs
3. React 公式 Learn
4. The Odin Project
5. Codecademy
6. freeCodeCamp
7. Zenn
8. Qiita

公開中のページと公式ヘルプ・執筆ガイド・リリースノートを優先して確認した。

## 2. ナビゲーション・情報設計の比較

| サイト | グローバルナビ | 左サイドバー / 章一覧 | ページ内目次 | 前後移動 | 検索 | C-studyで採用する要素 |
|---|---|---|---|---|---|---|
| Microsoft Learn | 製品・Training・資格などを横断する上位ナビ | ドキュメント階層を辿るナビを持つ。TrainingはPath → Module → Unitの階層 | 長い記事では記事内項目を補助表示 | 学習Unitでは連続した順路を持つ | サイト全体検索を強く提供 | コース階層と本文を分離し、現在レッスンを左ナビで強調。公式参照先を本文末に集約 |
| MDN | Web技術・Learn等の上位領域へ移動 | 文書ツリーを階層化し、現在セクションを展開、現在ページを強調 | `In this article` で長文の現在位置を補助 | 同一ツリーをサイドバーで辿れる | ドキュメント検索 | 左ナビの current 表示、右TOC、見出しアンカー、本文中心の3カラム |
| React Learn | Learn / Reference等の主要領域を分離 | Learn内の概念を段階的に辿れる | 長いページを見出しで分割 | Previous / Next を明示 | ドキュメント検索 | 本文末の前後レッスン移動と、冒頭の「このレッスンで学ぶこと」 |
| The Odin Project | Curriculumを中心に上位導線を持つ | Course → Section → Lessonの順で進む | Lesson本文内は見出し中心 | Lesson末にNext導線 | カリキュラム内探索 | 章→レッスンの順路を崩さず、本文末で次へ進める構造 |
| Codecademy | コース・Pathを中心とした学習ナビ | SyllabusでModule / Lesson / Exerciseを把握 | 演習画面では作業領域が中心 | 学習フローに沿って次Exerciseへ進む | コース探索 | 進捗と学習データを独立状態として保存し、復元可能にする |
| freeCodeCamp | Curriculumを上位に置く | Certification → Module → Lesson / Workshop / Lab等の階層 | コンテンツ種別ごとに段階表示 | ステップ型課題は次へ継続 | Curriculum探索 | 理論・演習・Review・Quizを一連の学習線として配置 |
| Zenn | 記事 / Bookなどのコンテンツ種別へ移動 | Bookではチャプター一覧を保持 | 2026年6月更新でPC/モバイル共通のフローティング目次、現在位置を連動表示 | Bookはチャプター単位で移動 | サイト検索 | PCは常設TOC、狭い画面では補助UIを本文から退避させる考え方を採用 |
| Qiita | 記事・質問等の主要導線 | 記事単体は本文を主役にし、周辺導線を抑える | 見出し構造を使って長文を把握 | 関連記事等はあるが教材順路は主目的ではない | 記事検索 | 本文の可読性を最優先し、教材固有の順路だけを追加 |

## 3. 本文・コード・補助情報の比較

| サイト | 本文幅 / 読みやすさ | 見出し階層 | コードブロック | Callout | モバイル | ダークモード | C-studyへの反映 |
|---|---|---|---|---|---|---|---|
| Microsoft Learn | 長文を中央カラムに制限し周辺ナビと分離 | H1から節へ順序化 | 言語・用途を意識したコード例。公式執筆ガイドでは検証可能な例を重視 | Note / Important等 | 補助ナビを圧縮 | 対応 | 本文最大幅を抑え、コードに言語名とCopyを付与。Note / Importantを視覚・テキストの両方で区別 |
| MDN | 執筆ガイドではデスクトップ本文を約700pxの前提でコード例の表示を検討 | 例ごとに見出し→説明→コード→結果説明を推奨 | Static / Live等を使い分け。コピーして利用される前提で品質を重視 | Note等 | コード例もレスポンシブを考慮 | 対応 | コード前に目的、後に処理・結果説明を置く。横スクロールはコード内部へ限定 |
| React | 短い段落とコードを交互に置き、概念を段階化 | `You will learn`→各概念→Recap / Challenge | Sandboxを本文に統合 | Note等 | 本文・演習を縦に再配置 | 対応 | 到達目標→説明→例→演習の順番を採用。ブラウザー内C#実行は行わず下書き欄のみ提供 |
| The Odin Project | Lesson本文は通常の文書幅でAssignmentを明確に分ける | Overview / Assignment / Knowledge check等 | 学習課題と外部教材を組み合わせる | Note相当の補足 | 1カラム中心へ縮退 | 対応 | 演習と確認問題を本文から視覚的に区切り、教材の終点を明確化 |
| Codecademy | エディター・指示・プレビューを学習操作中心に構成 | Exercise単位 | 編集状態を保持 | ヒント・エラー等 | 学習画面を端末幅に適応 | 対応 | 下書き保存と進捗保存を実装。ただし「実行」「自動採点」を装わない |
| freeCodeCamp | 理論ページ・Workshop・Labで画面目的を切り替える | Module内で教材種別を分ける | ステップ課題で編集内容を検証する仕組みを持つ | 指示・テスト結果を明確化 | 段階UIを縦方向へ適応 | 対応 | C-studyでは一ページに理論・3演習・確認問題をまとめつつ、節の境界を強くする |
| Zenn | 記事 / Book本文を読み続けやすい中央領域 | Markdown見出し | 言語名やファイル名をコードフェンスに付与可能 | メッセージ記法 | 目次をポップオーバーへ退避 | 対応 | コード言語ラベル、本文優先、モバイルdrawer/dialog |
| Qiita | 記事本文を主領域に置く | 2026年の改善でも見出し・mainランドマーク等の意味構造を重視 | 技術記事のコード表示を重視 | note / warning系表現 | 記事本文優先 | 対応 | semantic HTML、正しい見出し順、visible focus、カード過多を避ける |

## 4. 学習機能の比較

| サイト | 学習進捗 | 確認問題 | 演習UI | 状態リセット / 復元 | C-studyへの反映 |
|---|---|---|---|---|---|
| Microsoft Learn Training | Path / Module / Unit単位の進行管理 | AssessmentやKnowledge checkを組み込む教材がある | Interactive module / sandbox等 | アカウント学習履歴 | 32レッスンの完了数を常時表示 |
| React Learn | アカウント進捗よりドキュメント順路を重視 | ページ末のChallenge | 編集可能SandboxとShow solution | Sandbox側の状態 | 各レッスンに基礎・標準・応用の3演習を固定配置 |
| The Odin Project | サインイン時に進捗追跡 | Lesson末のKnowledge check | Assignmentで実作業を要求 | Curriculum進捗 | 確認問題を「理解確認」、演習を「自分で書く領域」と分離 |
| Codecademy | Course / Pathの進捗率を強く表示 | 課題判定を含む | Workspaceでコード状態を保存 | Course / Module / Exercise単位でReset可能。リセットはコードと進捗を消すため注意を明示 | 進捗・問題回答・下書き・復習マークをlocalStorageへ保存し、JSON export/importを提供 |
| freeCodeCamp | Curriculumの進捗を保持 | ModuleにQuizを含む | Theory / Workshop / Lab / Projectを段階化 | アカウント状態 | 理論→3段階演習→5問確認という固定学習ループ |

## 5. 採用する情報設計

### Desktop（1180px以上）

`左ナビ + 本文 + 右ページ内目次` を基本とする。

- 左: 8章 / 32レッスン、現在位置、進捗、検索・設定への導線
- 中央: 最大幅を制限した本文
- 右: 現在ページのH2/H3目次
- 本文のカード化は演習・確認問題など「操作境界」に限定する

### Tablet（821px〜1179px）

本文を優先する。

- 右TOCを非表示
- 左ナビは維持できる幅では残す
- 本文幅とコード領域を優先
- 表・コードだけ内部スクロール可能

### Mobile（820px以下）

1カラム本文へ縮退する。

- 左ナビはdrawer
- ページ内目次は本文先頭の目次と見出しアンカーで代替
- 固定3カラムを維持しない
- 操作ボタンは十分なタップ領域を確保
- body全体の横スクロールは禁止

## 6. ページ内の学習順序

1. レッスン番号 / 章 / 所要時間
2. 到達目標
3. 概念と内部の仕組み
4. 文法・コード例
5. 処理順 / 値・状態の変化
6. よくある間違いと修正
7. 基礎演習
8. 標準演習
9. 応用演習
10. 確認問題5問 + 全選択肢の解説
11. 公式一次情報
12. 前後レッスン移動

## 7. 視覚・操作ルール

- Important / Note / Tip / Error はラベルと境界線を併用し、色だけで区別しない。
- コードブロックは言語ラベルとCopyボタンを持つ。
- `pre` と必要な表のみ `overflow-x:auto`。ページ全体へ横スクロールを発生させない。
- 大きな装飾カード、巨大な上下余白、連続アニメーションを避ける。
- `prefers-reduced-motion` を尊重する。
- Light / Darkで意味構造を変えない。
- visible focusを必須とし、キーボードだけで検索・drawer・確認問題・設定を操作できるようにする。
- 演習textareaは「コード下書き」であり、実行環境がない状態を明記する。

## 8. C-studyで採用しない要素

- ブラウザー内でC#を動かしていないのに「実行」「成功」「自動採点」と表示すること
- すべての節をカードで囲うこと
- モバイルでDesktopの3カラムを縮小表示すること
- 進捗データを検証せずImportで直接上書きすること
- 本文理解より演出を優先するアニメーション

## 9. 参照先

- Microsoft Learn Training: https://learn.microsoft.com/en-us/training/
- Microsoft Learn content types: https://learn.microsoft.com/en-us/training/support/learn-content-types
- Microsoft Learn C#: https://learn.microsoft.com/en-us/dotnet/csharp/
- MDN sidebars: https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Page_structures/Sidebars
- MDN code examples: https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Page_structures/Code_examples
- MDN code style: https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide
- React Learn: https://react.dev/learn
- React challenges: https://react.dev/learn/your-first-component
- The Odin Project: https://www.theodinproject.com/lessons/foundations-how-this-course-will-work
- Codecademy progress reset: https://help.codecademy.com/hc/en-us/articles/220444588-Reset-Progress-on-a-Course-Path-or-Exercise
- freeCodeCamp curriculum structure: https://contribute.freecodecamp.org/how-to-work-on-coding-challenges/
- Zenn Book viewer update: https://info.zenn.dev/2026-06-12-book-viewer-improvements
- Qiita release note / accessibility: https://qiita.com/release-notes/2026-02-26
