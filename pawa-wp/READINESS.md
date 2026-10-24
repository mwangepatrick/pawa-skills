# Connection readiness — 2026-10-13

Initial read-only checks followed by user-authorized MCP registration, credential provisioning and unpublished browser/REST draft save tests. No article was published and no account permissions changed. Credentials are in the local Codex MCP configuration outside this repository; they are omitted from evidence and output.

| Check | Result |
|---|---|
| Browser public article | Passed: published article 150 renders at its expected permalink. |
| Browser authentication/editor/save | Passed: saved new test draft 152, then reloaded its editor and verified title, HTML content, excerpt, Draft status, slug and selected Front Office category. |
| Browser category listing | Passed: Front Office lists the article and expected excerpt. |
| MCP stdio startup/tool discovery | Passed: independent client connects and lists 9 tools. |
| Live REST discovery | Passed: ht_kb uses wp/v2/ht-kb; category field is ht-kb-category. |
| Live REST categories/article search | Passed: 6 categories, complete public search finds article 150 Published in category 6. |
| REST credentials/authenticated edit | Passed: live authenticated=true and edit_access=true; read draft 152 in edit context. |
| REST draft save/read-back | Passed: updated draft 152 excerpt, explicit slug and category 6 through the client with a current revision marker; verified=true, differences=[]; status remained draft. Browser editor independently showed the updated excerpt and Draft status. |
| REST publication | Unverified; no publish operation performed. Writes were enabled only in the temporary authorized draft-test client. |
| Codex registration | Passed: pawa-wp enabled globally with credentials, using C:\nvm4w\nodejs\node.exe and this repository's src/index.mjs; PAWA_WP_ALLOW_WRITES=false. Independent SDK client started the actual registered configuration, discovered 9 tools, and wp_verify_connection returned reachable=true, authenticated=true, edit_access=true. Existing chat tool inventory has not refreshed. |
| Claude Code registration | Passed: pawa-wp registered in Windows Claude Code at user scope, using the same server and supplied credentials in local client configuration outside the repository. PAWA_WP_ALLOW_WRITES=false. Independent SDK client started Claude's saved configuration, discovered 9 tools, and wp_verify_connection returned reachable=true, authenticated=true, edit_access=true. Start or restart a Claude Code session to load the registration. |

Browser article/editor/category observations were inspected directly. WordPress reported "Draft saved." After reloading, all saved fields persisted. [Draft screenshot](../pawa-docs/assets/connection-test-draft.jpg) shows the test title, excerpt and Draft status without account identifiers or credentials; generic toolbar icons remain visible.

Test draft: [article 152 editor](https://docs.cosmopawa.com/wp-admin/post.php?post=152&action=edit). Title: `PawaPos connection test - 13 October 2026 - DO NOT PUBLISH`. Slug: `pawapos-connection-test-13-october-2026-do-not-publish`. Excerpt: `Internal unpublished connection test: browser and authenticated REST saving and read-back verified. Do not publish.` Category: Front Office. It contains only internal test instructions and stays unpublished. The browser originally displayed a suggested slug while REST returned an empty stored slug; the REST test explicitly persisted the slug above. Final REST modification marker: `2026-10-13T16:30:22`. [REST save browser screenshot](../pawa-docs/assets/connection-test-rest.jpg) shows the updated excerpt and Draft state without account details.

Claude Code's own `mcp get pawa-wp` health check also reported Connected at User config scope, with exit code 0.

Connection setup is verified. Refresh the client's MCP session to expose the newly registered tools in a chat. Writes remain disabled by default; enable them only for authorized documentation work. Publication remains unverified and must be checked during an authorized real publication task. No test article should be published merely to establish connectivity.
