# Architecture Overview

## System Design

This is a Next.js application with a microservices backend. The frontend and backend are deployed independently and communicate via REST APIs.

```
┌─────────────────────────────────────────────────┐
│                   Next.js App                    │
│  ┌──────────────┐   ┌──────────────────────────┐ │
│  │  App Router  │   │      Server Components    │ │
│  │  (RSC/Pages) │   │   (data fetching layer)   │ │
│  └──────────────┘   └──────────────────────────┘ │
└────────────────────────┬────────────────────────┘
                         │ HTTP / REST
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
   ┌─────────────┐ ┌──────────┐ ┌─────────────┐
   │  Users API  │ │ Items API│ │ Notif. API  │
   │  :3001      │ │  :3002   │ │  :3003      │
   └──────┬──────┘ └────┬─────┘ └──────┬──────┘
          └─────────────┼──────────────┘
                        ▼
               ┌─────────────────┐
               │   PostgreSQL    │
               │   (shared DB)   │
               └─────────────────┘
```

## Technology Stack

| Layer       | Technology             |
|-------------|------------------------|
| Frontend    | Next.js 15, React 19   |
| Styling     | Tailwind CSS           |
| State       | Zustand + React Query  |
| Backend     | Node.js + Fastify      |
| Database    | PostgreSQL + Prisma    |
| Auth        | NextAuth.js (JWT)      |
| Infra       | Docker + Kubernetes    |

## Key Design Decisions

- **Server Components by default** — only use Client Components for interactivity
- **API routes for BFF** — Next.js API routes act as a Backend-for-Frontend, proxying microservice calls and handling auth
- **Shared types package** — `packages/types` is consumed by both frontend and backend services to keep contracts in sync
- **Environment-based service discovery** — service URLs are injected via environment variables; no hardcoded hostnames

## Further Reading

- [Auth Flow](references/auth-flow.md) — JWT lifecycle, token refresh, middleware, and role model
- [Data Flow](references/data-flow.md) — read/write paths, state layers, and cache revalidation
- [Deployment](references/deployment.md) — environments, container layout, Kubernetes resources, and CI/CD
- [Error Handling](references/error-handling.md) — error layers, classification table, and logging