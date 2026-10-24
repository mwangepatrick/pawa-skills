# Better Stack

Official hosted MCP server (`https://mcp.betterstack.com`, OAuth or API key).
Per Better Stack it covers incidents, on-call, uptime monitors, status pages,
dashboards, and ClickHouse queries over logs, metrics, traces and errors.
Confirm the current tool list from the connected server before relying on any
name.

## Collect

1. List open and recently resolved incidents for the window.
2. Query error-level logs/errors for the same window and service when a
   telemetry source is configured. Inspect the source schema before writing a
   query; do not assume column names.
3. Capture incident ID, monitor/service, started/resolved time, cause, link.

## Map to the table

Bug = incident title or grouped error message; Events = log/error count (state
that incidents have no event count); Source ID = incident ID.

## Do not

Create, acknowledge, resolve, escalate or comment on incidents, or change
monitors, on-call or status pages, without the user approving the exact
action. These tools exist on the server; availability is not permission.
Prefer a read-only API token when using key authentication.
