# Verification

Learned in the platform-api session of 2026-11-09 (FLWP-75718, platform-mcp); approved by the owner the same day.

- A check asserts on an output only the thing under test produces. A version line or an exit code another program could also give proves nothing: `make -C mcp wheel-test` passed twice for the wrong reason (it ran another binary of the same name on the `PATH`, then a wheel `uv` had cached under the same version) until it required a line only the new build prints and ran with `--no-cache`.
- Every test run writes to a log named after the agent (never shared: agents run checks in parallel), and the session shows its `tail -f` line as soon as the run starts, so the owner can follow it (owner, 2026-11-20). The log says which step is running; running totals stay out of it, since they change all the time and only get in the way. Nereus makes it deterministic in `make checks` (getnereus/nereus#1936).
