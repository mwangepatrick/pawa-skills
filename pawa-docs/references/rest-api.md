# REST management with browser verification

## Connect and discover before writing

1. Discover supported WordPress tools; prefer `pawa-wp` or compatible `pawa-wp-mcp` capabilities. Inspect current schemas, not remembered names. Choose a configured site alias and verify it resolves exactly to `https://docs.cosmopawa.com/`. A successful connection to another site is not sufficient.
2. Check the REST index, the `ht_kb` type registration and its associated taxonomies through read-only discovery. Standard discovery locations are `/wp-json/`, `/wp-json/wp/v2/types/ht_kb`, and `/wp-json/wp/v2/taxonomies`; follow returned links/namespace/rest_base and collection schema. Do not assume `/wp/v2/posts`, `/wp/v2/ht_kb`, ordinary `categories`, or a taxonomy name is correct. Inspect supported fields, methods, statuses and category property before mutations. Read all category pages and the necessary published/draft/pending/private article search pages; report incomplete visibility rather than declaring no duplicates.
3. Verify authenticated edit access with a supported connection check or read-only `context=edit` request against the intended collection/item. Public reads or a REST index prove reachability, not authentication or publishing permission. Inspect available operation capabilities/schema; record write/publish capability as unverified if it cannot be established without a mutation. Do not create a probe article to test access on production.
4. Use an existing securely provisioned connection. Application-password authentication over HTTPS is suitable for a supported REST client; the user provisions it outside the chat/skill/repository. Keep secret values in a protected credential store or externally provisioned environment, never skill files, committed site registries, generated articles or logs. The MCP may report alias, origin, credential-present status and verification results, never the password, Authorization header or raw sensitive server error. Handle authentication failure as an access problem, not an article-not-found result.

Do not create accounts, expand roles, install plugins, expose a hidden taxonomy or change site configuration merely to enable this workflow. Report the missing capability; a specifically authorized implementation task may address it. Browser sign-in and REST authentication are separate: a logged-in browser does not establish an external client's REST credentials.

## Search, save, and read back

- Search by topic synonyms, title and exact intended slug in the discovered article collection; account for pagination/status visibility. Inspect matching content and current taxonomy before creating. Preserve the existing article's ID/permalink for an update.
- For a new article, send title, semantic HTML content, slug, excerpt, selected category IDs under the discovered taxonomy field, and explicit `status: draft`. Read the returned ID back in edit context and compare raw title/content, slug, excerpt, category IDs, type and draft status with the prepared artifact. WordPress may sanitize content or resolve a slug collision; inspect differences, do not silently accept them.
- Publish only when requested and the evidence/preview passes: update that verified draft ID with explicit `status: publish`, then read back status, permalink and category IDs. The API path has no Gutenberg pre-publish clicks. Use the browser to verify the full rendered article and public category listing and save a sanitized screenshot. API persistence and rendered verification are separate completion checks.
- For an authorized live update, capture original raw content/metadata/status and `modified_gmt` or equivalent revision marker. Re-read immediately before writing and reconcile if it changed. Use only requested fields; preserve permalink/status/categories unless changing them is intended. Prefer a server-enforced version precondition when genuinely supported. A client re-read is not an atomic concurrency guarantee; do not claim it prevents all races. Read back the saved version and verify rendered output.
- A draft-only revision of a published article still needs a verified pending-revision mechanism or a separate local draft. `status: draft` on the existing published ID unpublishes it; `content` updates to that ID can change the live page. Ordinary REST revisions are history, not automatically an unpublished proposed-edit workflow.

## Ambiguous writes and bounded recovery

Before creation record the target alias/origin, intended slug, prepared content/metadata and operation start time in a non-secret local record. Keep the returned ID whenever available. Never automatically retry a mutating POST after timeout or connection loss; WordPress does not provide a generic create-idempotency guarantee.

For a known ID, read that item and compare intended fields/status. For an unknown create ID, perform one reconciliation pass: search the exact slug and closely matching title across relevant accessible statuses with pagination, compare type/content/excerpt/category IDs and timestamps. A matching title alone does not identify the operation. A transformed slug may require the title/content comparison. If a matching saved article exists, continue from its ID; if no result can be established because search is incomplete/ambiguous, preserve the artifact and report uncertain persistence. Retry only after definitive failure/non-persistence is established, and at most once. Avoid concurrent duplicate creations. For conflicting content, reconcile with the original snapshot rather than overwrite or auto-delete.

## Desired `pawa-wp` capability contract

The repository now contains the narrow `pawa-wp` package. Discover its registered tools at runtime; a package on disk is not a live connection. Its public discovery can run without credentials; edit/write access requires separate secure provisioning. Required capabilities:

| Capability | Required behavior |
|---|---|
| Connection status and verify | Alias/origin, credential-present boolean, REST reachability, authenticated read and supported capabilities, separate unverified/denied states; no credential output. |
| Discover article type/taxonomy | Actual rest_namespace/rest_base, schema and term-field mapping for ht_kb and associated category taxonomy. |
| Search/list/read | Pagination, exact slug and text search, accessible statuses, edit-context raw content/metadata and modification marker. |
| Create draft | Explicit type/status, title/content/slug/excerpt/category IDs; structured returned ID and read-back data; no blind retries. |
| Update/publish | Existing ID, limited fields, expected revision marker where supported, explicit status/intent; structured results and read-back verification. |
| Visual verification | Supported browser connection opens the resulting public article/category and saves sanitized screenshots; do not claim HTML alone proves layout. |

Keep connection setup separate from site-content mutation. Narrow tool scope to documentation needs; FTP/PHP execution, users/roles, theme options and plugins are not required for this task.

The implemented package exposes `wp_connection_status`, `wp_verify_connection`, `wp_discover_articles`, `wp_list_categories`, `wp_search_articles`, `wp_read_article`, `wp_create_draft`, `wp_update_article`, and `wp_publish_article`. It is restricted to this origin and ht_kb. Writes default off; publish permission remains unverified in read-only checks. It performs client revision preflight and API read-back; browser screenshots/rendering remain separate. It does not enforce duplicate search within create; the skill's search/reconciliation step is required before using `wp_create_draft`. Connection credentials are provisioned by the user outside tool arguments and tracked files.

Public REST discovery on 2026-10-13 confirmed article rest_base **ht-kb**, taxonomy key **ht_kb_category**, category rest_base **ht-kb-category**, namespace **wp/v2**, and article category property **ht-kb-category** in the OPTIONS schema. Do not confuse the taxonomy registration key with the article property. Discover again rather than assuming this dated snapshot applies unchanged.

## Inspiration and limits

Read-only reference: WSL `/home/pixel/projects/personal/wp/pawa-wp-mcp`, HEAD `3e12533d1434d55a797eef13debeb12cc15ca6cd`, inspected 2026-10-13. Its TypeScript MCP uses a site-alias registry, `WpRestClient`, content handlers and inspection tools. Its current `PostType` accepts only post/page; list/read/create/update use posts/pages, create lacks slug/excerpt/categories, update lacks slug/excerpt/categories, and general pagination/discovery/edit-context/concurrency/reconciliation are absent. Reuse the architecture, not its claim of Heroic KB coverage. The reference stores application-password fields in a local sites registry; do not copy real credentials or FTP configuration. No `pawa-wp` tool is connected to this chat as of this inspection.

Authoritative mechanics: [custom REST types/taxonomies](https://developer.wordpress.org/rest-api/extending-the-rest-api/adding-rest-api-support-for-custom-content-types/), [authentication](https://developer.wordpress.org/rest-api/using-the-rest-api/authentication/), and [post field/status API](https://developer.wordpress.org/rest-api/reference/posts/). The discovered Heroic KB schema takes precedence over assumptions drawn from ordinary posts.
