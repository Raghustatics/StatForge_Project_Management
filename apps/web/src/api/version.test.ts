import { fetchVersion } from "./version";

const respond = (body: unknown, status = 200): typeof fetch =>
  () => Promise.resolve(new Response(JSON.stringify(body), { status }));

describe("fetchVersion", () => {
  it("[TC-01.3] fetchVersion returns the version info", async () => {
    const calls: string[] = [];
    const fetchFn: typeof fetch = (input) => {
      calls.push(String(input));
      return respond({ name: "StatForge API", version: "0.1.0", api: "v1" })(input);
    };
    await expect(fetchVersion(fetchFn)).resolves.toEqual({
      name: "StatForge API",
      version: "0.1.0",
      api: "v1",
    });
    expect(calls).toEqual(["/api/v1/version"]);
  });

  it("[TC-01.3] fetchVersion rejects a malformed body", async () => {
    await expect(fetchVersion(respond({ name: "StatForge API" }))).rejects.toThrow(
      "version request failed",
    );
  });

  it("[TC-01.3] fetchVersion rejects non-2xx", async () => {
    await expect(fetchVersion(respond({ detail: "x" }, 503))).rejects.toThrow(
      "version request failed",
    );
  });
});
