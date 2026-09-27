export interface SqlGuardResult {
  ok: boolean;
  error?: string;
}

const READ_ONLY_START = /^\s*(SELECT|WITH)\b/i;
const GUARD_ERROR = "only SELECT/WITH statements are permitted";

export function checkReadOnlySql(sql: string): SqlGuardResult {
  const trimmed = sql.trim();
  if (!READ_ONLY_START.test(trimmed)) {
    return { ok: false, error: GUARD_ERROR };
  }
  const semiIndex = trimmed.indexOf(";");
  if (semiIndex !== -1 && trimmed.slice(semiIndex + 1).trim().length > 0) {
    return { ok: false, error: GUARD_ERROR };
  }
  return { ok: true };
}
