export type VersionInfo = { name: string; version: string; api: string };

const isVersionInfo = (body: unknown): body is VersionInfo => {
  if (typeof body !== "object" || body === null) return false;
  const record = body as Record<string, unknown>;
  return ["name", "version", "api"].every((key) => typeof record[key] === "string");
};

export async function fetchVersion(fetchFn: typeof fetch = fetch): Promise<VersionInfo> {
  const response = await fetchFn("/api/v1/version");
  const body: unknown = response.ok ? await response.json() : null;
  if (!isVersionInfo(body)) throw new Error("version request failed");
  return body;
}
