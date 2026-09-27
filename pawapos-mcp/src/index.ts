import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";
import { fileURLToPath } from "url";
import { dirname, resolve } from "path";
import dotenv from "dotenv";
import { PawaPosDbClient } from "./db-client.js";
import { dbToolDefinitions, dbToolHandlers } from "./tools.js";

const __dirname = dirname(fileURLToPath(import.meta.url));
dotenv.config({ path: resolve(__dirname, "../.env") });

function requireEnv(name: string): string {
  const value = process.env[name];
  if (!value) {
    throw new Error(`Missing required env var: ${name}`);
  }
  return value;
}

const dbClient = new PawaPosDbClient({
  host: requireEnv("PAWAPOS_LOCAL_DB_HOST"),
  port: Number(requireEnv("PAWAPOS_LOCAL_DB_PORT")),
  user: requireEnv("PAWAPOS_LOCAL_DB_USER"),
  password: requireEnv("PAWAPOS_LOCAL_DB_PASSWORD"),
  database: requireEnv("PAWAPOS_LOCAL_DB_NAME"),
});

const tools = dbToolDefinitions();
const handlers = dbToolHandlers(dbClient);

const server = new Server(
  { name: "pawapos-mcp", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({ tools }));

server.setRequestHandler(CallToolRequestSchema, async ({ params }) => {
  const handler = handlers[params.name];
  if (!handler) throw new Error(`Unknown tool: ${params.name}`);
  return (await handler(params.arguments ?? {})) as Record<string, unknown>;
});

const transport = new StdioServerTransport();
await server.connect(transport);

const shutdown = async () => {
  await dbClient.close();
  process.exit(0);
};

process.on("SIGINT", shutdown);
process.on("SIGTERM", shutdown);
