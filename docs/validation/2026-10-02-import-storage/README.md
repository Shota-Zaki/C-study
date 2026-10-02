# Local HTTP import/export and storage acceptance

Source: f013ecf4f60498ce80e8d63909933de1535a9fb9, work. Chromium 153.0.8010.12, installed Playwright, Node26.9.0. No installation or source changes. All378 copied public files matched the source and prior fixture ledger. Server bound an ephemeral loopback port; fresh disposable contexts loaded real pages under /course/. One browser job at a time; browser and task server closed in finally.

10/10 bounded checks PASS; pageErrors empty. Five rejected file inputs (version99, malformed JSON, 524289-byte file, invalid draft key, invalid quiz answer) each displayed the expected specific error and retained exactly the pre-existing localStorage bytes. Baseline draft was entered through the textarea, not injected storage. Valid import restored the normalized version2 state after application-triggered reload, then lesson navigation restored draft, selected answers and review flag. Import intentionally refreshes updatedAt on save, so that field alone is excluded from the input comparison. Export was captured through the browser download event and parsed JSON matched current stored state including updatedAt; exported.json preserves the synthetic download contents (with an added trailing newline).

Two separate fault-context cases inject only Storage.setItem to throw QuotaExceededError: edited draft remains visible with unsaved status and warning; valid import fails without persistent writes and rolls in-memory state back, confirmed by actual export of the prior fresh state. These are actual HTTP UI interactions with injected storage failure, not evidence of naturally exhausted browser storage. Read failure/corrupt existing storage and recovery from those states are outside this bounded batch. The fault page is not included in the normal pageErrors collection.

Harness uses documented Playwright file-input setInputFiles and download controls. It does not invoke the stalled native file picker. Prior in-app browser filechooser delay/export timeout remain recorded in the older evidence; this successful separate Chromium run does not diagnose that driver behavior. First successful run was repeated once only to preserve the download and strengthen rollback evidence. No product defects observed or fixes made.

Reproduce from repository root with an existing installed Playwright module and a task-owned copied public-file fixture:

```
PLAYWRIGHT_MODULE=/absolute/path/to/playwright/index.mjs CSTUDY_FIXTURE=/absolute/path/to/fixture-parent node docs/validation/2026-10-02-import-storage/browser.mjs
```

The fixture parent contains course/index.html and its unchanged public dependencies. Results write beside this script. Existing browser cache required; no dependency installation. Per-action timeout7s; short finite batch. Run only one browser job. Harness finally cleans browser and server after assertion failure; failure before browser launch/server setup should be checked separately.

CS07 remains IN_PROGRESS. This is loopback HTTP acceptance, not published HTTPS, native Safari, iPhone/iPad, responsive widths/zoom or complete keyboard acceptance. Previous source semantics coverage remains unchanged.
