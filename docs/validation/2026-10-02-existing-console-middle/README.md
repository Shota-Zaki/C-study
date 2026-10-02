# Existing Console semantic verification — 2026-10-02-existing-console-middle

Fixed input `5aa116852eee28c046356eeb8e751796857db908`. 76 unique existing Console examples, pre-established full stdout/exitCode/stderr expectations from matching Program.cs and canonical teaching sections. expectations.json retains source/project/teaching hashes, precise excerpts and reasoning; intentional runnable mistakes preserve their demonstrated outputs. Error/nonstandalone examples are not silently run as successful Console cases.

Actual 76/76 builds/runs and semantic contracts PASS. Full stdout/stderr compared with only CRLF/LF normalization, except an explicitly described dynamic timing contract if present. results.json preserves commands/logs/lifecycle SDK/runtime and cleanup exit0. One existing pinned-image container, no network,2CPU/2GB, private copied fixtures, per-example CWD, sequential build120s/run15s. Any stdin is piped without terminal echo; any file is in disposable per-example space. No host mounts, installs, source changes, services, main or deploy. verify.py reproduces from this repository with unique container name and existing image.

| Example | Expected complete stdout (line separators shown as /) | Semantics |
| --- | --- | --- |
|deep-09-01|ノート: 200 / ペン: 100|Each constructor retains its independent supplied name/price.|
|deep-09-02|ノート|Valid constructor trims the name and retains nonnegative price.|
|deep-09-03|first=2, second=1 / 全体=3|Two instance counters become 2 and 1 while shared static total is 3.|
|deep-09-05|ノート|Default initializer supplies ノート.|
|deep-09-06|[未設定]|Intentional parameter self-assignment leaves the instance field 未設定.|
|deep-09-07|Aoi|this.name assigns the instance field from Aoi.|
|deep-10-01|120 / 3 / 360|Stored unit price120 and quantity3 yield computed total360.|
|deep-10-02|True / 3 / False / 3|Taking2 succeeds and leaves3; taking10 fails without changing3.|
|deep-10-03|Aoi|Setter trims surrounding spaces before getter reads Aoi.|
|deep-10-05|Aoi|Getter reads backing field Aoi rather than recurring.|
|deep-11-01|12|Virtual dispatch selects Rectangle.Area, 3×4.|
|deep-11-02|基本 / 詳細|Nonvirtual hidden method selection follows the declared variable type.|
|deep-11-03|12 / 25|Abstract dispatch yields rectangle12 and square25 in array order.|
|deep-11-04|Parent本体 / Child本体 / Aoi|Base constructor body runs before derived body, then saved name is read.|
|deep-11-05|詳細|Virtual override selects 詳細 through base reference.|
|deep-12-01|通知: 保存しました|Interface dispatch calls the console implementation.|
|deep-12-02|通知: 売上集計が完了しました|ReportService composes the report name and delegates notification.|
|deep-12-03|在庫集計が完了しました|Recording implementation captures the composed message without printing until inspected.|
|deep-12-06|確認|Explicit implementation is reachable through INotifier.|
|deep-13-01|a=10, b=20|Value assignment copies10; assigning20 to b leaves a10.|
|deep-13-02|20 / True|Reference copy aliases one Box; mutation20 is shared.|
|deep-13-03|first=20, second=30 / False|Mutation20 remains on first after second is rebound to new Box30.|
|deep-13-04|元 / 99|Struct copy separates Name assignment but shares Scores array mutation99.|
|deep-13-05|9 / False / True|Array Clone creates a new array but shares its Item, changing source Count to9.|
|deep-13-06|1 / 9|Each Item is constructed separately, preserving source1 and copy9.|
|deep-13-07|10 / 10|Boxing preserves original int10; unbox to int then widen to long10.|
|deep-14-01|False / False / True / False|Plain classes compare references; records compare values while distinct instances remain distinct.|
|deep-14-02|Pen:100 / Pen:80 / False|with copies the record and changes only copied price80.|
|deep-14-03|Pen,Book / True|Intentional shallow with copy shares List and reveals Pen,Book on original.|
|deep-14-04|Pen / Pen,Book|Replacing Items with new List separates later Add from original.|
|deep-14-05|False / True|Record array property compares references; SequenceEqual compares values.|
|deep-14-06|True / False / True|string == compares contents, object == references, virtual Equals string contents.|
|deep-15-01|10,3,4 / 3|Add4, Remove2 and replacement of index0 produce10,3,4 and Count3.|
|deep-15-02|4 / False|Case-insensitive PEN/pen lookup returns decremented4; absent CLIP returns False.|
|deep-15-03|save=3 / load=2|Case-insensitive frequency counting yields save3/load2.|
|deep-15-04|10 / Aoi|Closed generic boxes retain int10 and string Aoi.|
|deep-15-06|1,3|RemoveAll deletes even values and preserves1,3.|
|deep-15-08|商品コードが未登録です|Missing key is explicitly reported rather than treated as zero.|
|deep-16-01|開始 / 変換前 / 整数の形式ではありません / 後片付け / 終了|Intentional FormatException jumps over value printing, catch reports, finally cleans, then execution resumes.|
|deep-16-02|数量を入力し直してください|ReadQuantity FormatException propagates to caller catch, which reports a recovery instruction.|
|deep-16-03|外側の開始 / 生成 / 利用中 / 解放処理 / 外側の続き|using block constructs resource then disposes before outside continuation.|
|deep-16-04|生成 / 処理 / 解放処理|using declaration disposes on return from Process.|
|deep-16-05|1: C# / 2: .NET / 3: Web API|StringReader advances through three literal lines and stops at EOF null.|
|deep-16-06|数量=0|Intentional empty catch swallows parse failure and leaves quantity0; preserve problem demonstration.|
|deep-16-07|数量の変換に失敗しました|TryParse failure prints error then returns before quantity printing.|
|deep-16-09|C#|Reader is used within its lifetime and reads C#.|
|deep-17-01|8|Delegate invokes Double with4, returning8.|
|deep-17-02|8 / 8 / 集計完了|Lambda double4/add3+5 produce8 each, then Action reports completion.|
|deep-17-03|2 / 1|Predicate counts >=60 as2 and >=80 as1.|
|deep-17-04|True / False|Closure observes updated limit60 then80, yielding True then False for70.|
|deep-17-05|3 / 3 / 3|Intentional shared loop variable is3 when all deferred actions run.|
|deep-17-06|0 / 1 / 2|Per-iteration captured variables retain0,1,2.|
|deep-17-07|残り:2 / 最終:1|Only first removal notifies2; handler unsubscribe suppresses second notification; final count1.|
|deep-18-01|80, 90|Index loop filters >=70 preserving80,90 order.|
|deep-18-02|80, 90|Foreach filter is equivalent to index loop.|
|deep-18-03|80, 90|Where filters >=70 during Join enumeration, preserving source order.|
|deep-18-04|40点 / 80点 / 65点 / 90点|Select transforms every score into a label without removing elements.|
|deep-18-05|合格:90点 / 合格:80点|Filter then descending sort then labels yields90 before80.|
|deep-18-06|注文1:ノート×2 / 注文3:付箋×3|Paid orders1 and3 survive and retain input order.|
|deep-18-07|False, True, False, True|Intentional Select maps each score to boolean; it does not filter.|
|deep-18-08|80, 90|Corrected Where retains80 and90.|
|deep-18-09|3,1,2 / 1,2,3|OrderBy creates ordered result while source remains3,1,2.|
|deep-19-01|A:列を取得 / B:列挙を開始 / C:生成開始 / 受取:10 / D:次へ進む / 受取:20|Iterator body is deferred until enumeration and resumes across each yield.|
|deep-19-02|2,3,4 / 3,4|Deferred query sees Add4 on first enumeration then Remove2 on second.|
|deep-19-03|2,3 / 1,2,3,4|ToList snapshots2,3 before source Add4.|
|deep-19-04|判定:1 / 判定:2 / 判定:3 / 2 / 判定:1 / 判定:2 / 判定:3 / 5|Count and Sum independently enumerate Where, repeating predicate side effects for1,2,3.|
|deep-19-05|2 / 5|Materialized List count2 and sum5 require no repeated predicates.|
|deep-19-06|False / 240 / 80 / 100|No score below60; sum240, average80, maximum100.|
|deep-19-08|平均なし|Empty input is handled with 平均なし without calling Average.|
|deep-20-01|Todo / Doing / 2|Enum ToString gives declared names, explicit int cast gives Done2.|
|deep-20-02|99 / False|Undefined enum numeric value formats99 and IsDefined is False.|
|deep-20-03|状態を確認してください|TryParse accepts99 but IsDefined rejects it and error branch prints.|
|deep-20-04|件数:3, 合計:60 / 件数:2, 合計:9|Named tuple computes count3/total60 and decomposes count2/total9.|
|deep-20-05|件数:60, 合計:3|Intentional reversed return binds total60 to Count and count3 to Total.|
|deep-20-06|件数:3, 合計:60|Named return assigns correct Count3/Total60.|
|deep-20-07|C# / C#|Extension syntax and direct static call both trim same C# text.|

Cumulative existing Console coverage123/193 (191 ordinary+1stdin+1file); remaining70. Originals35/35 have separate selected-input/HTTP evidence. No blanket branch/input/platform guarantee. CS07 remains IN_PROGRESS; UI/browser/device acceptance separate. Work push uses existing [skip publish] guard.

Independent read-only reviewer console_expectations_guides approved76/76 source/teaching/manifest contracts and final full-output/build/lifecycle results. No defects or special handling requirements, no Docker rerun. Disjoint IDs from early47 confirm cumulative123/193.
