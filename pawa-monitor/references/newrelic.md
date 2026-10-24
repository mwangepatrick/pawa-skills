# New Relic

Official hosted MCP server, a preview feature. Source: New Relic's
[setup guide](https://docs.newrelic.com/docs/agentic-ai/mcp/setup/) and
[tool reference](https://docs.newrelic.com/docs/agentic-ai/mcp/tool-reference/).
Tool names below come from that reference; still confirm them against the
connected server, since preview tools can change.

- US endpoint `https://mcp.newrelic.com/mcp/`, EU `https://mcp.eu.newrelic.com/mcp/`.
- OAuth is the supported authentication. API-key setups are not supported for
  Claude Code or Codex, and some tools (`natural_language_to_nrql_query`,
  `analyze_deployment_impact`) are OAuth-only.
- The account needs MCP enabled in feature control and a group role that can
  read the MCP server (for example Organization Read Only).

## Collect

1. `list_available_new_relic_accounts`, then `get_entity` to resolve the
   application/service in scope.
2. `list_entity_error_groups` for Errors Inbox groups in the window.
3. `get_error_statistics` for counts, first/last seen and trend per group.
4. `search_errors` for raw events of the top groups when a stack or message is
   needed.
5. `search_incident` / `list_recent_issues` for open alert issues.
6. `execute_nrql_query` only when the above cannot answer; test queries against
   real event types and attributes first.
7. Optional context: `list_change_events` and `analyze_deployment_impact`
   (OAuth-only) to link a bug to a deployment.

## Map to the table

Bug = error group message/class; Events = count from `get_error_statistics`;
Source ID = error group ID or issue ID.

## Safety

All listed tools are read-only per the reference. Treat that as documented, not
guaranteed; do not use any tool that is not read-only without approval.
