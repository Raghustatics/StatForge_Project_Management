# Risk Register

| ID | Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|
| R-01 | Release 1 breadth (88 templates, 8 drafted methodologies, PM suite, SPC, AI, Outlook, IDE) overruns | High | High | 30 small gates; a/b splits logged; ported engines | Owner |
| R-02 | Owner review bandwidth blocks gates (G21, G25 especially) | High | High | Plan review time per gate; review packets kept short | Owner |
| R-03 | Statistical errors damage trust | Medium | Critical | `/stats-validate` with NIST/R references; statistician agent; no UI before validation | Agents |
| R-04 | No Minitab outputs for the example datasets | High | Medium | NIST/R/textbook references; optional Minitab trial later | Owner |
| R-05 | Outlook web UI changes break the bridge; tenant policies forbid it | Medium | Medium | Opt-in, manual-paste fallback, kill switch, later Graph integration | Agents |
| R-06 | IP challenge over ported PMO code | Low | High | Written confirmation of ownership; no Altius data or process ported | Owner |
| R-07 | Minitab datasets committed to a public repo | Low | High | `.gitignore` before the first commit; gate-reviewer check | Agents |
