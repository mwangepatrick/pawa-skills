import { describe, it, expect, vi, beforeEach } from "vitest";

const mockClientQuery = vi.fn();
const mockRelease = vi.fn();
const mockConnect = vi.fn();
const mockPoolQuery = vi.fn();
const mockEnd = vi.fn();

const PoolMock = vi.fn().mockImplementation(() => ({
  query: mockPoolQuery,
  connect: mockConnect,
  end: mockEnd,
}));

vi.mock("pg", () => ({ Pool: PoolMock }));

const { PawaPosDbClient } = await import("../src/db-client");

const config = { host: "h", port: 5400, user: "u", password: "p", database: "d" };

beforeEach(() => {
  vi.clearAllMocks();
  mockConnect.mockResolvedValue({ query: mockClientQuery, release: mockRelease });
});

describe("PawaPosDbClient construction", () => {
  it("constructs the pool with connection config and read-only/timeout safety options", () => {
    new PawaPosDbClient(config);
    expect(PoolMock).toHaveBeenCalledWith({
      host: "h",
      port: 5400,
      user: "u",
      password: "p",
      database: "d",
      options: "-c default_transaction_read_only=on",
      statement_timeout: 10_000,
    });
  });
});

describe("listTables", () => {
  it("queries information_schema.tables and returns schema/table pairs", async () => {
    mockPoolQuery.mockResolvedValueOnce({ rows: [{ schema: "public", table: "stock" }] });
    const client = new PawaPosDbClient(config);
    const tables = await client.listTables();
    expect(mockPoolQuery).toHaveBeenCalledWith(expect.stringContaining("information_schema.tables"));
    expect(tables).toEqual([{ schema: "public", table: "stock" }]);
  });
});

describe("describeTable", () => {
  it("queries information_schema.columns with the table name as a bound parameter, not interpolated", async () => {
    mockPoolQuery.mockResolvedValueOnce({
      rows: [{ column_name: "id", data_type: "integer", is_nullable: "NO" }],
    });
    const client = new PawaPosDbClient(config);
    const columns = await client.describeTable("pos_payment_details");
    const [sql, params] = mockPoolQuery.mock.calls[0];
    expect(sql).toContain("$1");
    expect(sql).not.toContain("pos_payment_details");
    expect(params).toEqual(["pos_payment_details"]);
    expect(columns).toEqual([{ column_name: "id", data_type: "integer", is_nullable: "NO" }]);
  });
});

describe("runQuery", () => {
  it("rejects a non-SELECT/WITH statement without opening a connection", async () => {
    const client = new PawaPosDbClient(config);
    await expect(client.runQuery("DROP TABLE stock")).rejects.toThrow(
      /only SELECT\/WITH statements are permitted/
    );
    expect(mockConnect).not.toHaveBeenCalled();
  });

  it("re-asserts read-only, wraps the query with a row cap, and releases the client", async () => {
    mockClientQuery.mockResolvedValueOnce(undefined).mockResolvedValueOnce({ rows: [{ id: 1 }] });
    const client = new PawaPosDbClient(config);
    const rows = await client.runQuery("SELECT * FROM pos_payment_details");
    expect(mockConnect).toHaveBeenCalledTimes(1);
    expect(mockClientQuery).toHaveBeenNthCalledWith(1, "SET default_transaction_read_only = on;");
    expect(mockClientQuery).toHaveBeenNthCalledWith(
      2,
      "SELECT * FROM (SELECT * FROM pos_payment_details) AS _sub LIMIT 500"
    );
    expect(mockRelease).toHaveBeenCalledTimes(1);
    expect(rows).toEqual([{ id: 1 }]);
  });

  it("releases the client even if the wrapped query fails", async () => {
    mockClientQuery.mockResolvedValueOnce(undefined).mockRejectedValueOnce(new Error("syntax error"));
    const client = new PawaPosDbClient(config);
    await expect(client.runQuery("SELECT * FROM nope")).rejects.toThrow("syntax error");
    expect(mockRelease).toHaveBeenCalledTimes(1);
  });
});
