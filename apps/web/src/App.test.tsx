import { render, screen } from "@testing-library/react";
import { App } from "./App";

describe("placeholder page", () => {
  it("[TC-01.3] shows the api version from /api/v1/version", async () => {
    render(<App loadVersion={() => Promise.resolve({ name: "StatForge API", version: "0.1.0", api: "v1" })} />);
    expect(await screen.findByText("API v1 · version 0.1.0")).toBeInTheDocument();
    expect(screen.getByRole("heading", { level: 1, name: "StatForge" })).toBeInTheDocument();
  });

  it("[TC-01.3] shows a loading message first", () => {
    render(<App loadVersion={() => new Promise(() => {})} />);
    expect(screen.getByText("Connecting to the StatForge API…")).toBeInTheDocument();
  });

  it("[TC-01.3] shows a plain error when the api is unreachable", async () => {
    render(<App loadVersion={() => Promise.reject(new Error("version request failed"))} />);
    expect(await screen.findByRole("alert")).toHaveTextContent(
      "Can't reach the StatForge API. Check that the api service is running, then reload the page.",
    );
  });
});
