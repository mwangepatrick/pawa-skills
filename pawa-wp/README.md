# pawa-wp

Documentation-only WordPress MCP for **https://docs.cosmopawa.com/** and Heroic KB **ht_kb** articles. Inspired by the broader WSL `wp/pawa-wp-mcp` project; does not include FTP, PHP execution, themes, plugins, users, roles, arbitrary sites or ordinary posts/pages.

## Setup

Use Node.js 20 or later. In this directory run `npm install` and `npm test`. Register an MCP stdio server named `pawa-wp` with command `node` and argument `D:\cp\pp\pawa-skills\pawa-wp\src\index.mjs`. The package requires the MCP SDK; tests use Node's built-in runner.

[mcp.example.json](mcp.example.json) is a credential-free example for clients supporting the `mcpServers` JSON format. Adapt the registration format to your client; it is not an active configuration and is not automatically loaded by every client. This change does not alter global Codex/Claude settings or copy the WSL connection registry.

Provision these environment variables through the client's protected secret mechanism or process environment. Never put actual credentials in this repository, MCP examples, articles or chat:

- `PAWA_WP_USERNAME`: WordPress application-password account.
- `PAWA_WP_APPLICATION_PASSWORD`: securely provisioned application password.
- `PAWA_WP_ALLOW_WRITES`: defaults off; set exactly `true` for authorized article work.
- `PAWA_WP_CATEGORY_TAXONOMY`: optional taxonomy key if discovery finds more than one associated hierarchical taxonomy. Discover first; do not guess.

No credential entry/setup tool is exposed. `wp_connection_status` reports credential presence only. `wp_verify_connection` performs read-only discovery/authentication/edit-collection checks; public reachability is not authentication, and publishing permission remains unverified until an authorized operation establishes it. The user provisions credentials and account permissions separately. This package does not enable REST on WordPress or configure accounts.

## Tools and workflow

1. `wp_connection_status`, `wp_verify_connection`, `wp_discover_articles`: confirm the fixed target, REST registration, edit access and taxonomy mapping.
2. `wp_search_articles`, `wp_list_categories`, `wp_read_article`: inspect current content and category taxonomy. Search returns completeness and inaccessible statuses, not a false no-match assurance. At most 20 pages per collection/status.
3. `wp_create_draft`: explicit title, HTML, slug, excerpt and existing category IDs. Always creates a draft and reads it back.
4. `wp_update_article`: explicit `draft` or `live_update` intent, ID and `expected_modified_gmt`. Rejects draft-only changes to a published article. No status argument; preserves current publication status.
5. `wp_publish_article`: explicit `publish` intent and version marker; only an inspected draft can be published. Reads it back.

Use the [pawa-docs skill](../pawa-docs/SKILL.md) to verify product claims before preparing content. Search for duplicates before creating; preserve ID and permalink for updates. Writes remain subject to the user's actual instruction—enabling the process flag is not approval for every publication.

Results contain structured JSON in MCP text content. Every write returns read-back comparison (`verified`, `differences`) and `browser_verification: required`. Sanitization/slug changes must be reviewed. Use the connected browser to check the public article and category listing and save a sanitized screenshot; this server does not itself capture browser screenshots.

## Safeguards and limits

- Fixed HTTPS origin; discovered route segments validated; redirects rejected to prevent forwarding credentials elsewhere.
- No secret values or server-response bodies in connection/error output. No write retries. Network failure, invalid write response or server 5xx can mean `WRITE_UNCERTAIN`; reconcile by ID or slug/title/content across accessible statuses before any retry. Read-back failure retains the returned ID in its error and must not trigger another write.
- Read/search output is restricted to article content/metadata needed for documentation; article password, author identifiers and unrelated meta fields are omitted.
- `modified_gmt` is checked immediately before update/publication, but this is a client preflight, **not an atomic server lock**. Concurrent edits can still race.
- Private/pending statuses may be inaccessible to some accounts. The tool reports incomplete search; it does not elevate privileges or create probe articles.
- No pending-revision mechanism. Draft-only changes to a published article must be stored separately locally.
- The live site's REST routes, credentials and write capabilities must be verified after registration. Local mocked tests do not prove live connectivity or publication.
