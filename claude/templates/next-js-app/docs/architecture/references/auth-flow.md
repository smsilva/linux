# Auth Flow

## Overview

Authentication is handled by NextAuth.js using JWT strategy. The token is issued at login and attached to every subsequent request via the `Authorization` header.

## Login sequence

```
Browser → Next.js /api/auth/signin → Users API :3001/auth/login → JWT issued
```

```
POST /api/auth/signin
Body: { email, password }

→ Users API validates credentials
→ Returns JWT (15min expiry) + refresh token (7d, httpOnly cookie)
→ NextAuth stores session in memory; refresh token in cookie
```

## Token refresh

```
Browser (expired JWT) → Next.js middleware → detects expiry
→ POST /api/auth/refresh with refresh token cookie
→ Users API issues new JWT
→ Request retried transparently
```

## Middleware

`middleware.ts` at the root protects all routes except `/login` and `/api/auth/*`:

```ts
export const config = {
  matcher: ['/((?!login|api/auth).*)'],
}
```

## Role model

| Role    | Description                        |
|---------|------------------------------------|
| `user`  | Default role; own resources only   |
| `admin` | Full access to all resources       |

Roles are embedded in the JWT payload under `role`. Server Components and API routes check `session.user.role` before granting access.