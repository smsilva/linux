# Data Flow

## Server Components (read path)

Data fetching happens in Server Components. No client-side fetch for initial page load.

```
Browser request
  → Next.js Server Component
    → fetch() to internal microservice (server-to-server, no CORS)
      → Microservice queries PostgreSQL via Prisma
        → Returns data
    → Component renders HTML
  → Browser receives fully-rendered HTML
```

## Client mutations (write path)

Mutations go through Next.js API routes (BFF layer), never directly to microservices from the browser.

```
Browser
  → POST /api/items (Next.js API route)
    → Validates session (NextAuth)
    → Forwards to Items API :3002 with service token
      → Prisma writes to PostgreSQL
    → Returns result
  → React Query invalidates cache
  → Server Component re-fetches on next navigation
```

## State layers

| Layer         | Tool           | Scope                              |
|---------------|----------------|------------------------------------|
| Server cache  | Next.js fetch  | Per-request or ISR (revalidate)    |
| Client cache  | React Query    | In-memory, invalidated on mutation |
| UI state      | Zustand        | Ephemeral; not persisted           |

## Revalidation

Use `revalidatePath` or `revalidateTag` in Server Actions after mutations to bust the Next.js cache:

```ts
'use server'
import { revalidatePath } from 'next/cache'

export async function deleteItem(id: string) {
  await itemsApi.delete(id)
  revalidatePath('/items')
}
```