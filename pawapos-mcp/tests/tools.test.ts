import { describe, it, expect, vi, beforeEach } from "vitest";
import type { PawaPosDbClient } from "../src/db-client";

const mockListTables = vi.fn();
const mockDescribeTable = vi.fn();
const mockRunQuery = vi.fn();

const client = {
  listTables: mockListTables,
  describeTable: mockDescribeTable,
  runQuery: mockRunQuery,
} as unknown as PawaPosDbClient;

const { dbToolHandlers } = await import("../src/tools");

type TextResult = { content: { type: "text"; text: string }[]; isError?: boolean };
const textOf = (result: TextResult) => result.content[0].text;

beforeEach(() => vi.clearAllMocks());

describe("list_tables", () => {
  it("returns the table list as JSON", async () => {
    mockListTables.mockResolvedValueOnce([{ schema: "public", table: "stock" }]);
    const result = await dbToolHandlers(client).list_tables({});
    expect(JSON.parse(textOf(result))).toEqual([{ schema: "public", table: "stock" }]);
  });
});

describe("describe_table", () => {
  it("returns column info as JSON", async () => {
    mockDescribeTable.mockResolvedValueOnce([{ column_name: "id", data_type: "integer", is_nullable: "NO" }]);
    const result = await dbToolHandlers(client).describe_table({ table: "stock" });
    expect(mockDescribeTable).toHaveBeenCalledWith("stock");
    expect(JSON.parse(textOf(result))[0].column_name).toBe("id");
  });

  it("returns isError true when table is missing from input", async () => {
    const result = await dbToolHandlers(client).describe_table({});
    expect(result.isError).toBe(true);
  });
});

describe("run_query", () => {
  it("returns query rows as JSON", async () => {
    mockRunQuery.mockResolvedValueOnce([{ id: 1 }]);
    const result = await dbToolHandlers(client).run_query({ sql: "SELECT * FROM stock" });
    expect(mockRunQuery).toHaveBeenCalledWith("SELECT * FROM stock");
    expect(JSON.parse(textOf(result))).toEqual([{ id: 1 }]);
  });

  it("returns isError true with the guard message when the client rejects the sql", async () => {
    mockRunQuery.mockRejectedValueOnce(new Error("only SELECT/WITH statements are permitted"));
    const result = await dbToolHandlers(client).run_query({ sql: "DROP TABLE stock" });
    expect(result.isError).toBe(true);
    expect(textOf(result)).toContain("only SELECT/WITH statements are permitted");
  });
});
