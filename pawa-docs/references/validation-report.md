# Pawa documentation skill validation — 2026-10-13

## Scope and design

Created one repository skill, `pawa-docs`, with a concise entrypoint, evidence guide, WordPress workflow, worked example, behavioral cases and Codex UI metadata. Edits are confined to pawa-skills. No applicable AGENTS.md was found in pawa-skills or checked ancestor directories. Existing conventions use top-level skill folders and references; README lists the collection. No product source or live article was changed.

The user supplied the publication procedure and accuracy requirements. The design separates evidence collection from customer writing and publication, preserving draft/publish intent. A single long entrypoint would burden ordinary discovery; a publication-only guide would omit the main accuracy risks. Supporting references keep the detailed evidence and WordPress procedures accessible when needed.

## Baseline before skill creation

An isolated evaluator received two pressure requests, raw source facts, a duplicate article URL and no new skill. It correctly refused unsupported KRA PIN label, mandatory phone and instant verification claims. It also correctly chose a separate draft for a published article in a follow-up scenario. These accuracy/safety cases passed at baseline; no claim of an observed unsafe baseline failure is made.

Workflow-completeness criterion failed: the first response did not supply title/slug/excerpt metadata, the Heroic KB/code-editor/two-Publish procedure, a saved screenshot, or a category-listing verification. Exact baseline follow-up acknowledgement: "My first response omitted several workflow checks: identify the WordPress post type and editor; inspect publication status and the action performed by its save button; establish whether a pending-revision workflow exists; specify durable draft storage; capture the original content and modification timestamp; and verify the public result after any authorized publication. Holding publication alone did not define how to persist a draft safely."

The skill addresses those observed workflow gaps alongside the user's required accuracy constraints. Evaluation results with the skill are recorded below.

## Independent forward evaluation

Evaluator `/root/forward_test` read the skill and references plus raw source files. Evaluation was offline/read-only, with no live mutations or generated draft files. It applied three realistic requests rather than only reviewing prose:

| Case | Observed result |
|---|---|
| A: urgent new KRA guide using remembered labels | Chose a qualified revision of article 150 instead of a duplicate. Supplied title, existing slug, excerpt, Front Office choice and numbered customer prose; used default/configured distinction and save-icon wording. Held unsupported publication. |
| B: draft-only update claiming optional phone and instant verification | Preserved published article/permalink, proposed a separate durable local draft and original-state metadata, excluded instant-verification claim, and qualified blank-phone behavior. Explicitly said proposed draft path was not created. |
| C: authorized new article with current editor observations | Returned Options > Code editor, title/HTML, Settings > Article Categories, excerpt/slug, preview, both Publish buttons, success check, public article and category-listing verification, sanitized screenshot and link. Distinguished published Save behavior and concurrent update checks. |
| Deployment wording differs from seed; running POS unavailable | Recorded scopes/deployment identity, did not substitute seed label or claim runtime confirmation, retained unsafe target-specific content as draft. |

Representative evaluator decisions: "The published editor’s Save must not be used to simulate a draft" and "Saving these details does not confirm that the PIN has been verified with KRA." These are observed decisions, not evidence of actual WordPress persistence.

The evaluator found further accuracy details by following raw code: payment-shortcut interception can consume Ctrl+P, and phone is used as a downstream customer key despite no dialog empty check. Its draft focused a text entry field to avoid the inspected interceptor, while explicitly retaining runtime qualification. Parent independently read the interceptor, customer UPSERT and schema and updated the worked-example ledger. Also corrected provenance: implementation/migrations clean, article Markdown untracked.

Focused follow-up with the corrected files: evaluator classified "Ctrl+P always works" as contradicted, "Phone optional" as narrowly dialog-supported but unverified end to end, and "Save verifies PIN instantly" as unsupported. It again preserved the published article and proposed a separate draft. Exact result: "No remaining concrete defect found in the revised example or evidence rules for these cases." This limited rerun does not prove all future requests will comply.

## Packaging validation

- Bundled `skill-creator/scripts/quick_validate.py`: **Skill is valid!**
- Local Markdown reference resolution and portability: **7 links checked, 0 failures**. Entrypoint: 510 words.
- `git diff --check`: exit 0; only an informational CRLF conversion warning for README.
- Saved article and category JPEGs were reopened and visually inspected; both exclude the authenticated toolbar and show the intended page/title/category context.
- Skill not installed globally or pushed; all authored files remain in the requested pawa-skills repository for review/use.

## Direct checks

- Read the local Markdown, shortcut handler and preceding interceptor, designer, dialog validation/load/phone lookup, Receipt setter and downstream customer UPSERT, and migration. Inspected implementation/migration files clean; local article untracked. Commits recorded in the worked example.
- Read-only configuration query: `SELECT code, type_code, description, active, def FROM id_type ORDER BY type_code`; active default TIN description was TAX IDENTIFICATION NUMBER. No customer rows read. Deployment identity unknown.
- Web fetch could not access the article and returned a verification page for the homepage; browser UI successfully opened both.
- Public article rendering matched local Markdown. WordPress editor confirmed Published, post 150, ht_kb, slug/excerpt and selected Front Office category. Options menu exposed Code editor. Current published editor button says Save.
- Category page listed the article and expected excerpt; saved article and category screenshots exclude authenticated toolbar.
- No draft creation, save, update, or publish actions performed on WordPress. New-article two-Publish flow is documented from the user's completed workflow, not re-executed in this run.

## REST-first update and narrow MCP — 2026-10-13

User requested REST for article management and browser visual verification, then clarified that the new MCP belongs in `D:\cp\pp\pawa-skills` and must cover PawaPos documentation only. Added `pawa-wp` beside the existing `pawapos-mcp`; no broader WSL tool modifications, global registration, credentials or site mutations.

Read-only inspiration: `/home/pixel/projects/personal/wp/pawa-wp-mcp`, HEAD `3e12533d1434d55a797eef13debeb12cc15ca6cd`. Read applicable WSL AGENTS files, README and REST/content/registry/index source, not real sites.json or .mcp credential configuration. Reused the site-alias/REST/MCP architecture while leaving FTP, PHP, themes, plugins, user/role management and other sites out of the new package.

### Skill behavior

Baseline evaluator `/root/rest_baseline` found existing skill gaps in actual REST route/schema discovery, authentication/edit checks, API read-back and ambiguous-write reconciliation. Revised SKILL.md, browser fallback and new REST reference address them. Independent `/root/rest_forward` applied four cases: discovered custom routes versus post/page-only tools, draft-only published update, lost create response with inaccessible private statuses, and API success with failed category listing. It selected discovered routes/capabilities, separate local draft, no blind retry/incomplete persistence, and unverified publication respectively. No live mutations or evaluator draft artifacts.

### MCP checks

- Test-first: initial client tests failed because no client existed. Implemented client/tool schemas and stdio server. Review found incorrect taxonomy key mapping and invalid JSON-null write response handling; regression tests reproduced both before fixes. Also reproduced and fixed edit-context article-password exposure with an output allowlist.
- Final Node tests: **16 passed, 0 failed**. Cover actual custom route/field discovery, redirects, pagination, secret-safe connection/error output, read-back, write-disabled default, draft-only published guard, stale-version guard, explicit publish intent, uncertain responses without retry, denied/incomplete search, and schema mismatch.
- Follow-up independent code review confirmed both reported defects resolved and found no newly introduced important defects.
- Actual SDK stdio handshake: connected a separate MCP client, listed **9 tools**, called wp_connection_status and closed. Reported fixed docs origin, no credentials, writes disabled.
- Dependencies installed successfully. No scripts from dependencies run. Offline cache attempt failed before normal registry installation succeeded.
- Read-only live client check succeeded after using permitted network access: reachable true, authenticated false, edit_access false, publish_access unverified. Confirmed article rest_base **ht-kb**, category key **ht_kb_category**, REST base and article field **ht-kb-category**, namespace wp/v2. Category list complete: Cash Book, Getting Started, Back Office, Front Office, How To, Integrations.
- No authenticated live reads/writes or publication performed. Credential-free registration example supplied; server is not yet registered in this chat and credentials must be provisioned separately.
- Updated skill format validation passed; **11 local Markdown links, 0 failures** across skill and MCP documentation; diff whitespace check passed.

### Remaining limits

Version preflight is not an atomic server lock. Search is bounded to 20 pages per status, and incomplete visibility is reported. Duplicate search/reconciliation remains required by the skill before create; WordPress creates are not made idempotent by the server. Browser checks/screenshots are separate from MCP persistence. Authentication/edit/publish permission and live write read-back remain untested until secure provisioning and an authorized article task. The original broader MCP is unchanged.

## Original example limits

No running POS dialog, target version, receipt print, downstream persistence execution/fiscal integration, anonymous browser session, or pending-revision plugin was verified. Screenshot shows the upper rendered article; full text and category membership were checked through browser accessibility/DOM observations. A full-height browser screenshot attempt was unsupported; the saved viewport screenshot remains usable. The existing article needs target-specific shortcut troubleshooting and save-icon clarification before it can be considered fully runtime-verified; no live edits were authorized by this skill-creation task. Do not equate packaging/evaluation passes with successful real publication or universal feature accuracy.
