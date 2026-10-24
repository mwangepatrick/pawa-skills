# Evidence and accuracy

## Ledger

For each claim record: article wording, source path and line/function, repository commit and dirty-file status, migration/config query or setting, UI observation and version/environment, date, conclusion, and unresolved limitation. Mark claims verified for a stated scope, qualified, contradicted, or unchecked. Do not label an entire article verified because a few key facts pass.

Locate relevant repositories from the workspace and their instructions. In this workspace typical sources are `D:\cp\pp\pawapos-fo\PawaPosFo` (Front Office), `D:\cp\pp\pawapos-bo` (Back Office), and `D:\cp\pp\pawapos-dblog` (schema, seeds, migrations). Paths may change; confirm rather than assuming. Read relevant files without modifying product repositories for a documentation task.

| Claim | Evidence to follow |
|---|---|
| Shortcut | Key handler, preceding interception, screen/context, guards, and target dialog. Do not infer application-wide scope from one screen. |
| UI label/button | Designer/resources, runtime overrides/localization, and running UI if available. Distinguish visible text, tooltip, accessible name, icon, and internal identifier. |
| Required field | Save handler, validation helpers, callee, schema/API constraints, and configured rules. A label or suggested preparation does not prove a requirement. |
| Dropdown/default | Query/binding, code/value mapping, seed and later migrations, active/default flags, read-only target configuration, displayed option. A seed is a default, not proof of today's customer configuration. |
| Timing | Execution sequence and runtime observation. Separate entering details before payment, saving locally, remote verification, and printing. No latency or tax-authority verification claim from a generic setter. |
| Prerequisite/feature/outcome | Permissions, settings, version gates, downstream callers, integrations, persistence, and actual UI result. Receipt output depends on the configured print path/template. |

Use supported read-only configuration tools when available. Query only necessary non-sensitive configuration columns; avoid customer rows, secrets, connection strings, and credential files. State which environment a connector represents; unknown deployment identity prevents generalization to all sites.

## Contradictions and unavailable sources

Compare code, migrations, live configuration, running product UI, and existing documentation explicitly. Trace differences to version, runtime overrides, customized data, or article error. Do not choose whichever source matches the proposed wording. An existing published article is a writing reference, not implementation proof.

If the target UI/configuration cannot be inspected, say exactly what was checked and what was not. A source-backed general statement may be usable with an explicit scope/default qualification; a target-specific instruction requiring missing evidence remains a draft until resolved. Never promise unsupported certainty. Do not invent placeholder UI labels, validation timing, receipt results, permissions, or configuration prerequisites to make a procedure feel complete.

Use synthetic, clearly fictional examples only when needed. Prefer descriptions such as "the customer's PIN" to plausible government identifiers. Crop or redact private data and authenticated account/session details before saving screenshots; use public-page views when they suffice. Do not capture credentials during sign-in.
