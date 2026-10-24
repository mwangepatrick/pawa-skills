---
name: pawa-docs
description: Use when creating, updating, reviewing, drafting, or publishing PawaPos customer documentation for docs.cosmopawa.com.
---

# PawaPos documentation

Produce accurate, usable customer articles for https://docs.cosmopawa.com/. This site uses WordPress Heroic Knowledge Base, post type `ht_kb`. Prefer **REST API through a supported MCP connection for article management**, then **browser verification of the rendered article and category listing**.

## Workflow

1. Establish the topic, audience, product/version, and requested **draft or publish** intent. Read applicable repository instructions. Search the live site's articles by topic, synonyms, shortcut, and workflow; inspect matching articles before creating another. For updates, capture current content, title, slug, excerpt, category, status, post ID, and modification marker; preserve the permalink unless its change is requested.
2. Inspect current category taxonomy and comparable articles. Choose the category by the customer's task and product area, explain the choice, and reuse an appropriate existing category. Never assume the taxonomy is unchanged or create a category without authorization.
3. Read [evidence.md](references/evidence.md). Build a claim-by-claim evidence ledger **before drafting**. Verify every feature claim, exact UI label, keyboard shortcut, required field, timing, prerequisite, and expected outcome against relevant source handlers/callees, migrations and configuration, plus the running UI/deployed configuration when available. Reconcile contradictions before publication. Describe concrete limits when a required source is unavailable; exclude unsupported instructions or retain a clearly qualified draft.
4. Write customer-facing content with purpose, prerequisites, numbered actions, expected outcome, correction steps, and concise troubleshooting. Supply a task-specific title, stable lowercase hyphenated slug, and short excerpt. Use exact verified UI names; distinguish default seed wording from site customization. Keep implementation evidence in the ledger, not the article. Never store credentials, session tokens, or real customer identifiers in skill files, examples, articles, or screenshots.
5. Read [rest-api.md](references/rest-api.md) for route discovery, connection checks, REST saves and read-back verification. Discover supported tools, preferably `pawa-wp`; verify the target alias/origin, authentication and actual `ht_kb`/category capabilities. Use REST for search, taxonomy reads, drafts, updates and authorized publication. Do not assume a tool is installed or guess custom routes. If REST is unavailable or incomplete, explain the specific limit and use the observed [WordPress browser workflow](references/wordpress.md). Let the user handle sign-in/credential provisioning. Respect draft/publish intent and existing authorization; skill changes do not authorize live article changes.
6. Review the preview against the ledger and requested scope. Recheck the existing article for concurrent changes before an update. After authorized publication, verify the rendered public article **and category listing**, save a sanitized screenshot, and return the public link and screenshot path/image. For drafts, verify durable draft storage and preview, return its location and state, and state what was not verified publicly.

## Decision guardrails

| Pressure or shortcut | Required decision |
|---|---|
| Approved old draft or urgent deadline | Recheck claims; approval is not evidence of behavior. |
| A variable is named `kra_pin` | Verify the displayed label and configured option; internal names are not UI labels. |
| Seed says one thing, deployed data another | Record both scopes and document the observed target deployment. |
| Button says Save or Update | Inspect publication status and the action's effect before saving. |
| Requested draft of a published article | Use a verified pending-revision workflow or a separate local draft; do not update or unpublish the live article. |
| API write timed out or response was lost | Reconcile the target article before retrying; absence of a response is not proof of failure. |

Read [worked-example.md](references/worked-example.md) when documenting customer tax details or learning the evidence format. It is a dated example, not proof of all installations. Behavioral evaluation cases and validation limits are in [validation.md](references/validation.md).
