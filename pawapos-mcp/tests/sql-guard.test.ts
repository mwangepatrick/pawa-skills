import { describe, it, expect } from "vitest";
import { checkReadOnlySql } from "../src/sql-guard";

const GUARD_ERROR = "only SELECT/WITH statements are permitted";

describe("checkReadOnlySql", () => {
  it("accepts a SELECT statement", () => {
    expect(checkReadOnlySql("SELECT * FROM stock")).toEqual({ ok: true });
  });

  it("accepts a lowercase select statement", () => {
    expect(checkReadOnlySql("select * from stock")).toEqual({ ok: true });
  });

  it("accepts a WITH statement", () => {
    expect(checkReadOnlySql("WITH t AS (SELECT 1) SELECT * FROM t")).toEqual({ ok: true });
  });

  it("accepts a SELECT with a single trailing semicolon", () => {
    expect(checkReadOnlySql("SELECT 1;")).toEqual({ ok: true });
  });

  it("accepts leading whitespace before SELECT", () => {
    expect(checkReadOnlySql("   SELECT 1")).toEqual({ ok: true });
  });

  it('rejects "INSERT"', () => {
    expect(checkReadOnlySql("INSERT INTO stock VALUES (1)")).toEqual({ ok: false, error: GUARD_ERROR });
  });

  it('rejects "UPDATE"', () => {
    expect(checkReadOnlySql("UPDATE stock SET qty = 1")).toEqual({ ok: false, error: GUARD_ERROR });
  });

  it('rejects "DELETE"', () => {
    expect(checkReadOnlySql("DELETE FROM stock")).toEqual({ ok: false, error: GUARD_ERROR });
  });

  it('rejects "DROP"', () => {
    expect(checkReadOnlySql("DROP TABLE stock")).toEqual({ ok: false, error: GUARD_ERROR });
  });

  it('rejects "ALTER"', () => {
    expect(checkReadOnlySql("ALTER TABLE stock ADD COLUMN x int")).toEqual({ ok: false, error: GUARD_ERROR });
  });

  it('rejects "CREATE"', () => {
    expect(checkReadOnlySql("CREATE TABLE x (id int)")).toEqual({ ok: false, error: GUARD_ERROR });
  });

  it("rejects a multi-statement string with a trailing write after a semicolon", () => {
    expect(checkReadOnlySql("SELECT 1; DROP TABLE stock")).toEqual({ ok: false, error: GUARD_ERROR });
  });
});
