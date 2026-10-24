# MCP setup (user performs these)

A skill cannot install or sign in to MCP servers. Run these yourself, then ask
the agent to run the preflight. Restart the agent session after adding servers;
servers added mid-session are not loaded until restart.

## Claude Code

```text
claude mcp add --transport http --scope user sentry https://mcp.sentry.dev/mcp
claude mcp add --transport http --scope user betterstack https://mcp.betterstack.com
claude mcp add --transport http --scope user newrelic https://mcp.newrelic.com/mcp/
```

Use `--scope user` so the servers are available in every project. New Relic EU
accounts use `https://mcp.eu.newrelic.com/mcp/`. New Relic OAuth needs Claude
Code 2.1.186 or later. Then start a new session, run `/mcp`, pick each server
and complete the browser sign-in. `claude mcp list` shows `Needs authentication`
until you do. Verify Sentry against https://docs.sentry.io/ai/mcp/.

## Codex

New Relic (Codex 0.154.0 or later):

```text
codex mcp add newrelic --url https://mcp.newrelic.com/mcp/
```

or in `~/.codex/config.toml`:

```toml
[mcp_servers.newrelic]
url = "https://mcp.newrelic.com/mcp/"
```

Do the same with `url` for Sentry and Better Stack, then complete each browser
OAuth flow. Syntax changes between Codex versions; check its current docs.

## Credentials

Never commit tokens or put them in skill files. Prefer OAuth.
