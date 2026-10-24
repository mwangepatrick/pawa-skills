# Sentry

Official hosted MCP server (`https://mcp.sentry.dev/mcp`, OAuth). Per Sentry's
docs it covers organizations, projects, issues and Seer analysis. Confirm the
current tool list from the connected server before relying on any name.

## Collect

1. Resolve the organization and project(s) in scope.
2. List unresolved issues for the window, sorted by last seen or frequency,
   filtered to the environment. Include regressions.
3. For the top issues, fetch detail: error type and message, top stack frame,
   release, first/last seen, event count, affected users, permalink.
4. Seer analysis is optional. Present it as a suggestion, never as a finding.

## Map to the table

Bug = issue title; Source ID = short ID; Events = event count; users affected
goes in `Why ranked here`.

## Do not

Resolve, ignore, assign or merge issues, or change alert rules, without the
user approving the exact action.
