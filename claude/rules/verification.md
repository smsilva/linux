# Verification

Learned in the platform-api session of 2026-11-09 (FLWP-75718, platform-mcp); approved by the owner the same day.

- A check asserts on an output only the thing under test produces. A version line or an exit code another program could also give proves nothing: `make -C mcp wheel-test` passed twice for the wrong reason (it ran another binary of the same name on the `PATH`, then a wheel `uv` had cached under the same version) until it required a line only the new build prints and ran with `--no-cache`.
- Before using a Jira transition id, list the issue's transitions, or pass the transition's name: ids differ per workflow and issue type. Id 2 was "Homologado" on a Story and "Blocked" on a Bug of the same project, and a bug went to Blocked by mistake.
- Before designing or delivering an issue, read why each of its closed dependencies was closed: one closed as superseded or not planned changes the target (owner, 2026-11-10). Nereus #162 (deploy main to live) was designed against #161's VPS, closed as superseded on 2026-10-30, and that surfaced only at the first real run.
