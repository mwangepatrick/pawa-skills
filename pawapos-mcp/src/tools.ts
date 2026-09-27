import { z } from "zod";
import { zodToJsonSchema } from "zod-to-json-schema";
import type { PawaPosDbClient } from "./db-client.js";

const ListTablesSchema = z.object({});
const DescribeTableSchema = z.object({ table: z.string().min(1) });
const RunQuerySchema = z.object({ sql: z.string().min(1) });

function toSchema(s: z.ZodType): Record<string, unknown> {
  const schema = zodToJsonSchema(s) as Record<string, unknown>;
  delete schema.$schema;
  return schema;
}

type TextContent = { type: "text"; text: string };
type ToolResponse = { content: TextContent[]; isError?: boolean };
const ok = (text: string): ToolResponse => ({ content: [{ type: "text", text }] });
const fail = (e: unknown): ToolResponse => ({
  content: [{ type: "text", text: `Error: ${e instanceof Error ? e.message : String(e)}` }],
  isError: true,
});

export function dbToolDefinitions() {
  return [
    {
      name: "list_tables",
      description: "List all user tables in the PawaPOS local database",
      inputSchema: toSchema(ListTablesSchema),
    },
    {
      name: "describe_table",
      description: "Get column name, data type, and nullability for a table",
      inputSchema: toSchema(DescribeTableSchema),
    },
    {
      name: "run_query",
      description: "Run a read-only SELECT/WITH query (results capped at 500 rows)",
      inputSchema: toSchema(RunQuerySchema),
    },
  ];
}

export function dbToolHandlers(
  client: PawaPosDbClient
): Record<string, (args: unknown) => Promise<ToolResponse>> {
  return {
    list_tables: async () => {
      try {
        const tables = await client.listTables();
        return ok(JSON.stringify(tables, null, 2));
      } catch (e) {
        return fail(e);
      }
    },
    describe_table: async (args) => {
      try {
        const { table } = DescribeTableSchema.parse(args);
        const columns = await client.describeTable(table);
        return ok(JSON.stringify(columns, null, 2));
      } catch (e) {
        return fail(e);
      }
    },
    run_query: async (args) => {
      try {
        const { sql } = RunQuerySchema.parse(args);
        const rows = await client.runQuery(sql);
        return ok(JSON.stringify(rows, null, 2));
      } catch (e) {
        return fail(e);
      }
    },
  };
}
