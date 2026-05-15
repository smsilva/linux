# Error Handling

## Layers

Errors are caught at three layers so nothing surfaces as an unhandled exception.

### 1. API route layer (BFF)

Wraps all outbound calls to microservices. Maps service errors to HTTP responses using the standard error envelope (see [api-design.md](../api-design.md)).

```ts
try {
  const data = await usersApi.getMe(token)
  return Response.json({ data })
} catch (err) {
  return toHttpError(err) // maps ServiceError → { error: { code, message, status } }
}
```

### 2. React Query (client mutations)

`onError` callbacks handle mutation failures. Show a toast; do not crash the page.

```ts
useMutation({
  mutationFn: deleteItem,
  onError: (err) => toast.error(err.message),
})
```

### 3. Next.js error boundaries

- `error.tsx` — catches rendering errors per route segment; shows a recovery UI
- `global-error.tsx` — catches errors in the root layout; last resort

## Error classification

| Type              | Where caught          | User-visible action           |
|-------------------|-----------------------|-------------------------------|
| Validation (422)  | API route             | Return field-level errors     |
| Auth (401/403)    | middleware            | Redirect to `/login`          |
| Not found (404)   | Server Component      | Render `not-found.tsx`        |
| Server error (5xx)| API route / error.tsx | Show generic error + retry    |
| Network failure   | React Query           | Toast + retry button          |

## Logging

Errors are logged server-side with `pino`. Include `requestId` from the response meta so logs can be correlated with API calls.