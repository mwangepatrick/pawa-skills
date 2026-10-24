# Heroic Knowledge Base browser fallback and visual verification

Target: https://docs.cosmopawa.com/. Articles use `ht_kb`, not ordinary WordPress Posts or Pages. Follow [REST management](rest-api.md) first. Use this browser procedure for administration only when supported REST operations are unavailable or incomplete and state the reason. Use the browser for visual verification after REST operations even when API read-back passes. The browser session may already be signed in. If authentication is required, let the user complete sign-in; never request, enter, or store credentials in this workflow.

## Discovery and draft preparation

Search the site's knowledge-base search and, when accessible, **Articles** in WordPress for title/slug and topic synonyms. Check drafts as well as published matches. Inspect the current category list in the editor or category administration and public category pages. Do not rely solely on homepage highlights as a complete article inventory.

Current taxonomy observed 2026-10-13: **Cash Book**, **Getting Started**, **Back Office**, **Front Office**, **How To**, **Integrations**. These names are a snapshot; inspect again per request. Prefer Front Office for checkout/customer-entry tasks and compare neighboring content for ambiguous topics.

Prepare title, slug, excerpt, HTML body, category choice/rationale, and a separate evidence ledger. Use semantic HTML (`p`, `h2`, `h3`, `ol`, `li`, `strong`) without scripts, inline styling, credentials, or duplicated H1. Preview numbered steps, emphasis, headings, tables if used, and special characters.

## New article: observed working path

1. Open WordPress administration. Choose **Articles > Add New Article**; confirm it is an Article/`ht_kb` editor.
2. Open Gutenberg **Options > Code editor**. Fill **Add title** and **Type text or HTML** with the prepared title and HTML. Inspect the resulting content before further actions.
3. Open **Settings**, select the **Article** tab if needed, expand **Article Categories**, and choose the verified category. Confirm the selected checkbox. Do not accidentally leave an unrelated default category.
4. Use **Add an excerpt** (or **Edit excerpt** when one exists) to enter the prepared excerpt. Inspect **Slug** and set/confirm the intended slug before publication; the editor may generate one automatically.
5. Preview and compare content and metadata with the evidence ledger. For draft-only intent, use the currently observed draft-save action, verify Draft status and persistence, and stop without publishing.
6. For authorized publication, click **Publish**, inspect the pre-publish panel for visibility/status/date and intended article, then click its final **Publish** button. Verify the success state and open the public permalink. Do not assume the first click completed publication.

The create-and-publish path above is the user's completed workflow. In this skill validation run, the existing article/editor/category controls were observed read-only; no test article was created or published. Gutenberg wording can change: the existing published article showed **Save** on 2026-10-13. Determine whether the current action publishes changes from status and current UI, not from a remembered button label.

## Update existing article

Open the matching **Edit Article**, confirm post ID/title/permalink/status, and capture the original content/metadata and modification marker. Limit edits to the request; preserve unrelated content and permalink. Before saving, compare with the current live/editor version to detect changes by another author. If it changed, reconcile rather than overwrite.

For an authorized live update, apply the reviewed changes and use the observed save/update action for the published article. Verify success and reload the public article. Existing published articles may not use the two-button new-publication flow.

**Draft-only update of a published article:** ordinary **Save/Update** can change the live page. Use a pending-revision mechanism only if actually available and verified. Otherwise save a separate local Markdown/HTML revision with metadata, original link, change summary and evidence notes; report its path and that the live page is unchanged. Do not switch the published article to Draft or create a publicly visible duplicate to simulate a draft revision.

## Verification and recovery

Verify the public permalink displays the requested title, full rendered body, numbered actions, exact UI wording, and expected links. Open the chosen public category listing and confirm the article appears there with the intended title; the breadcrumb alone is not the full category-placement check. Save a sanitized screenshot of the rendered article and optionally category listing using supported browser screenshot methods; return links and local screenshot paths/images. For private drafts, verify preview/storage rather than claiming public verification.

Derive each next click from a fresh accessibility/DOM observation; prefer current semantic labels. Never store element indices, DOM order assumptions, account tokens, or nonce URLs in skill instructions. If an action fails, inspect current state and publication status before retrying to avoid duplicates. If a label/control changed, locate its current equivalent and verify its role; report a concrete blocker when intent cannot be established. Retry public verification once after a deliberate reload if appropriate; unresolved rendering/category errors mean publication is unverified, not successful. Preserve artifacts and report the exact problem rather than repeatedly publishing.
