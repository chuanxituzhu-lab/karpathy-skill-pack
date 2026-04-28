# E2E Testing Patterns

> 融合自 `e2e-testing-patterns`。与 testing-mastery/SKILL.md 中的单元测试互补。

## Playwright Best Practices

### Locators (prioritized)
```typescript
// ⭐ Best
page.getByRole('button', { name: 'Submit' })    // Role-based
page.getByTestId('submit-btn')                   // Test ID (data-testid)

// ⚠️ Fragile
page.locator('.btn-submit')                      // CSS class
page.locator('#submit-btn')                      // ID
page.locator('div > button:nth-child(3)')        // DOM structure
```

### Page Object Pattern
```typescript
class LoginPage {
  constructor(private page: Page) {}

  async goto() { await this.page.goto('/login') }
  async fillEmail(email: string) {
    await this.page.getByLabel('Email').fill(email)
  }
  async fillPassword(password: string) {
    await this.page.getByLabel('Password').fill(password)
  }
  async submit() {
    await this.page.getByRole('button', { name: 'Sign in' }).click()
  }
}
```

### Test Isolation
```typescript
// Each test gets fresh state — use worker-scoped fixtures for heavy setup
import { test as base, expect } from '@playwright/test'

const test = base.extend({
  authenticatedPage: async ({ browser }, use) => {
    const context = await browser.newContext({
      storageState: 'auth.json',
    })
    const page = await context.newPage()
    await use(page)
    await context.close()
  },
})
```

## Cypress Best Practices

```typescript
// Custom commands
Cypress.Commands.add('login', (email: string, password: string) => {
  cy.session([email, password], () => {
    cy.visit('/login')
    cy.get('[data-testid="email"]').type(email)
    cy.get('[data-testid="password"]').type(password)
    cy.get('[data-testid="submit"]').click()
    cy.url().should('not.include', '/login')
  })
})

// Use cy.session() to cache authentication
it('loads dashboard', () => {
  cy.login('user@test.com', 'password123')
  cy.visit('/dashboard')
  cy.contains('Welcome back').should('be.visible')
})
```

## CI Configuration

### Playwright in CI
```yaml
- name: Run E2E tests
  run: npx playwright test
- name: Upload report
  uses: actions/upload-artifact@v4
  if: failure()
  with:
    name: playwright-report
    path: playwright-report/
```

## Flakiness Prevention

| Issue | Fix |
|---|---|
| Timing-dependent | Use auto-retrying assertions (`toBeVisible`, `toHaveText`) |
| API-dependent | Mock API with MSW or `page.route()` |
| Shared state | Isolate tests, use fresh DB per run |
| Animation | `page.waitForTimeout(300)` or wait for stable state |
| Cross-browser | Run on Chromium by default, sanity-check on Firefox/Safari |
