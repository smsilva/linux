# Testing Guidelines

## Test Pyramid

```
         ▲ E2E (Playwright)
        ▲▲▲ Integration (React Testing Library + MSW)
      ▲▲▲▲▲▲▲ Unit (Vitest)
```

Aim for: **70% unit / 20% integration / 10% E2E**.

## Unit Tests

Use **Vitest**. Co-locate test files with source files: `foo.ts` → `foo.test.ts`.

```ts
import { describe, it, expect } from 'vitest'
import { formatPrice } from './formatPrice'

describe('formatPrice', () => {
  it('formats integer cents as currency string', () => {
    expect(formatPrice(1999)).toBe('$19.99')
  })

  it('returns "Free" for zero', () => {
    expect(formatPrice(0)).toBe('Free')
  })
})
```

**Rules:**
- No mocking of modules that are cheap to instantiate (utils, pure functions)
- Mock at the boundary: HTTP clients, file system, external SDKs
- One `describe` per module; name `it` blocks as sentences

## Integration Tests

Use **React Testing Library** with **MSW** for API mocking.

```tsx
import { render, screen } from '@testing-library/react'
import { server } from '@/test/server'
import { http, HttpResponse } from 'msw'
import { ItemList } from './ItemList'

it('renders items fetched from API', async () => {
  server.use(
    http.get('/api/v1/items', () =>
      HttpResponse.json({ data: [{ id: 1, name: 'Widget' }], meta: {} })
    )
  )

  render(<ItemList />)

  expect(await screen.findByText('Widget')).toBeInTheDocument()
})
```

**Rules:**
- Test behavior, not implementation — interact via labels/roles, not CSS selectors
- Assert what the user sees, not internal state

## E2E Tests

Use **Playwright**. Place tests under `e2e/`.

```ts
import { test, expect } from '@playwright/test'

test('user can create an item', async ({ page }) => {
  await page.goto('/items')
  await page.getByRole('button', { name: 'New Item' }).click()
  await page.getByLabel('Name').fill('My Widget')
  await page.getByRole('button', { name: 'Save' }).click()

  await expect(page.getByText('My Widget')).toBeVisible()
})
```

**Rules:**
- Use `getByRole` and `getByLabel` — never CSS selectors
- Each test is independent: seed data in `beforeEach`, clean up in `afterEach`
- Run against a real (local) stack, never mock the API in E2E tests

## Running Tests

```bash
# Unit + integration
pnpm test

# Watch mode
pnpm test:watch

# Coverage report
pnpm test:coverage

# E2E
pnpm test:e2e
```

## Coverage Thresholds

| Metric     | Minimum |
|------------|---------|
| Lines      | 80%     |
| Branches   | 75%     |
| Functions  | 80%     |

CI will fail if thresholds are not met.