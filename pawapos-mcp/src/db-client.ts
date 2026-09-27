import { Pool } from "pg";
import { checkReadOnlySql } from "./sql-guard.js";

export interface PawaPosDbConfig {
  host: string;
  port: number;
  user: string;
  password: string;
  database: string;
}

export interface TableRef {
  schema: string;
  table: string;
}

export interface ColumnInfo {
  column_name: string;
  data_type: string;
  is_nullable: string;
}

export class PawaPosDbClient {
  private readonly pool: Pool;

  constructor(config: PawaPosDbConfig) {
    this.pool = new Pool({
      ...config,
      options: "-c default_transaction_read_only=on",
      statement_timeout: 10_000,
    });
  }

  async listTables(): Promise<TableRef[]> {
    const result = await this.pool.query(
      `SELECT table_schema AS schema, table_name AS table
       FROM information_schema.tables
       WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
       ORDER BY table_schema, table_name`
    );
    return result.rows;
  }

  async describeTable(table: string): Promise<ColumnInfo[]> {
    const result = await this.pool.query(
      `SELECT column_name, data_type, is_nullable
       FROM information_schema.columns
       WHERE table_name = $1
       ORDER BY ordinal_position`,
      [table]
    );
    return result.rows;
  }

  async runQuery(sql: string): Promise<Record<string, unknown>[]> {
    const guard = checkReadOnlySql(sql);
    if (!guard.ok) {
      throw new Error(guard.error);
    }
    const client = await this.pool.connect();
    try {
      await client.query("SET default_transaction_read_only = on;");
      const result = await client.query(`SELECT * FROM (${sql}) AS _sub LIMIT 500`);
      return result.rows;
    } finally {
      client.release();
    }
  }

  async close(): Promise<void> {
    await this.pool.end();
  }
}
