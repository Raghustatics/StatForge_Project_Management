import AxeBuilder from "@axe-core/playwright";
import { expect, test } from "@playwright/test";

test("[TC-01.3] page shows the version served by /api/v1/version", async ({ page, request }) => {
  const response = await request.get("/api/v1/version");
  expect(response.ok()).toBe(true);
  const info = (await response.json()) as { api: string; version: string };
  await page.goto("/");
  await expect(page.getByRole("heading", { level: 1, name: "StatForge" })).toBeVisible();
  await expect(page.getByText(`API ${info.api} · version ${info.version}`)).toBeVisible();
});

test("[TC-01.3] placeholder page has no serious or critical axe violations", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByText(/API v1 · version/)).toBeVisible();
  const results = await new AxeBuilder({ page }).analyze();
  const blocking = results.violations.filter(
    (v) => v.impact === "serious" || v.impact === "critical",
  );
  expect(blocking).toEqual([]);
});
