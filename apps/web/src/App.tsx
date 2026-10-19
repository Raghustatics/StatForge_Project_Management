import { useEffect, useState } from "react";
import { fetchVersion, type VersionInfo } from "./api/version";

type State =
  | { kind: "loading" }
  | { kind: "ready"; info: VersionInfo }
  | { kind: "error" };

export function App({ loadVersion = fetchVersion }: { loadVersion?: () => Promise<VersionInfo> }) {
  const [state, setState] = useState<State>({ kind: "loading" });

  useEffect(() => {
    let active = true;
    loadVersion().then(
      (info) => active && setState({ kind: "ready", info }),
      () => active && setState({ kind: "error" }),
    );
    return () => {
      active = false;
    };
  }, [loadVersion]);

  return (
    <main className="placeholder">
      <h1>StatForge</h1>
      {state.kind === "loading" && <p>Connecting to the StatForge API…</p>}
      {state.kind === "ready" && (
        <p>{`API ${state.info.api} · version ${state.info.version}`}</p>
      )}
      {state.kind === "error" && (
        <p role="alert">
          Can't reach the StatForge API. Check that the api service is running, then reload the
          page.
        </p>
      )}
    </main>
  );
}
