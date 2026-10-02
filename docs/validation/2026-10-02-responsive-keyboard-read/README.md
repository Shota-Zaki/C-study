# Local HTTP responsive, keyboard and read-error acceptance

Source work7d0048fe6b629f8bb224f7bd3dd405190fa83959. Chromium153.0.8010.12, installed Playwright, Node26.9.0; no installs.378 public-file fixture hashes match current source and the prior local-origin ledger. Fresh contexts load genuine pages at an ephemeral loopback HTTP /course/ subpath. Only one browser job ran at a time; task browser/server exited through finally. Product source unchanged.

50/50 bounded checks PASS:42 geometry checks,4 selected keyboard paths,4 actual UI paths using explicitly injected storage-error fixtures. Normal-context pageErrors empty; each storage fault context separately collects pageErrors and checks that they are empty after import.

The established scripts/test_visual_browser.py selection is retained:14 representative pages (eight chapter lessons, one deep-dive and five non-lesson page types) at1536x1040,1024x900 and390x844. Every document scrollWidth<=viewport width, with nonempty heading captured. This checks horizontal document overflow, not all interior clipping or all80 pages. Four viewport screenshots are retained:lesson05 desktop,lesson24 tablet,lesson13 mobile and desktop index. Visual inspection found readable headings, body introduction, navigation and controls without overlap in these four captures. Screenshots do not inspect all scroll positions, dark mode or native200%zoom.

Keyboard checks use native key events after harness sets the initial focus:Enter opens the mobile drawer; forward Tab through all visible drawer links/controls remains inside; Escape closes and restores opener focus. Control+k opens search and focuses its input; Escape closes it. Slash entered in a focused draft textarea remains text and does not open search. Space and ArrowDown select quiz radio choices; Space toggles completion. These selected flows do not constitute a complete keyboard/accessibility audit; reverse Tab and all other controls remain outside scope. No native file-picker call used.

Storage fixtures are separate from ordinary browser persistence:corrupt-json explicitly seeds malformed localStorage bytes, then native reload invokes the application's real read path; read-denied injects Storage.getItem throwing SecurityError and a read-only original-reader for test inspection. Both warn, preserve stored bytes while draft saves are blocked and keep entered text visible with unsaved status. Import through documented setInputFiles exercises the real File/change handler. A valid backup replaces corrupt data, clears the warning and restores the imported draft after navigation. Under persistent injected read denial, import writes the valid backup but reload warns again; this is successful persistent write with continuing read failure, not full recovery or natural OS permission testing.

The initial50 checks passed. Strengthened recovery assertions then exposed a harness TypeError caused by one assert.equal call lacking its expected argument. `harness-error-results.json` preserves that run; correcting the harness produced final50/50 PASS. No application defect was inferred from the harness mistake. Repeated runs were limited to these added assertions and error correction; source-output checks were not repeated.

Reproduce from repository root using the installed module and unchanged copied public dependencies (fixture parent contains course/index.html):

```
PLAYWRIGHT_MODULE=/absolute/path/to/playwright/index.mjs CSTUDY_FIXTURE=/absolute/path/to/fixture-parent node docs/validation/2026-10-02-responsive-keyboard-read/browser.mjs
```

Per-action timeout5s; finite50-case batch. Results and screenshots write beside the script. No installation. One browser job at a time. Native Safari not run:the selected authorized harness is cached Chromium and this batch makes no Safari-equivalence claim. No OS permission prompts requested or enabled. Published HTTPS, native Safari, iPhone/iPad, native200%zoom and complete keyboard acceptance remain unverified. CS07 IN_PROGRESS; source semantics coverage unchanged.
