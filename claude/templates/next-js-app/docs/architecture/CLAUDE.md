# Architecture Docs

## Files in this directory

- **overview.md** — system diagram, technology stack, and key design decisions; start here for a high-level picture
- **api-design.md** — REST conventions, authentication header, response envelope, endpoint catalogue, and error codes

## Files in references/

Detailed deep-dives linked from `overview.md`:

- **auth-flow.md** — JWT lifecycle (login, refresh), NextAuth middleware configuration, and role model
- **data-flow.md** — server-side read path via Server Components, client mutation path through the BFF, state layers (Next.js cache / React Query / Zustand), and cache revalidation with Server Actions
- **deployment.md** — environment matrix, Docker image layout, Kubernetes resources per service, CI/CD pipeline steps, and required environment variables
- **error-handling.md** — three-layer error strategy (API route, React Query, Next.js error boundaries), error classification table, and server-side logging