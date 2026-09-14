# Detailed design

## Build
scripts/build.py --out _site --base /C-study/。URL baseを一元化しHTMLをエスケープ。lesson.example/deep.walk/deep.bug.after/exercise.solution/deep.drillsから192サンプルを生成し本文との乖離を防ぐ。

## Content
course: version,updated,target,chapters[8],lessons[32],sources,glossaryDetails。
lesson: id,chapter,title,summary,minutes,goals,sections,foundation,syntax,example,output,trace,pitfall,exercise,questions[5],refs,tags,sdk,deep。
deep: intro,concepts,reference(単独3列),walk,bug,base_explanation,drills[2],checkpoints。重複deep.questionsはquestionsへ統合。

## State
schemaVersion付きJSON。completed/bookmarksは既知ID、quizは既知問題IDと0..3の選択、draftsは既知演習IDと長さ制限付き文字列、lastLessonは既知ID、themeはsystem/light/dark。未知キーや不正型は不採用。import確認後に置換し、失敗なら旧状態を維持。

## Interaction
全文索引から検索結果リンク。dialogはshowModal/close、Escapeとfocus復帰。pre内部スクロール、copy結果aria-live。問題はfieldset/legend/radioで選び、採点後に正答と全理由。演習はlabel付きtextarea、ヒント/解答はdetails。

## Validation
全HTMLのh1/見出しID/リンク/前後ナビ/問題/演習/禁止内容を検査。実ブラウザーで明暗×3サイズ、保存復元、JSON境界、問題、検索、drawer、focusを確認。C#の実行は別テストで記録し、SDK不在を合格扱いしない。
