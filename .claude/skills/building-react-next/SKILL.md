---
name: building-react-next
description: This skill should be used when the user asks to "build a React app", "create a Next.js page", "optimize React performance", "fix re-renders", "set up App Router", "add Server Components", "improve bundle size", "implement data fetching", or discusses "React hooks", "state management", "React 18", "React 19", "Next.js", "SSR", "SSG", "ISR", "Suspense", "Server Actions", or "React.memo". Unifies React 18+ best practices, Next.js App Router patterns, performance optimization strategies, and Vercel's 57 React guidelines into a single comprehensive reference.
version: 1.0.0
---

# React + Next.js Expert

## Purpose

Unified guide for React 18+ and Next.js development, combining Vercel's 57 React guidelines with production-proven performance patterns and Next.js best practices.

## When to Use

Auto-activates when:
- Creating React components or hooks
- Designing state management architecture
- Debugging re-renders or performance issues
- Building Next.js pages, layouts, or API routes
- Configuring Next.js (App Router, file conventions, SEO)
- Discussing data fetching strategies

## Core Principles

### 1. Component Design

- **Composition over Inheritance**: `children` prop, slots pattern, render props
- **Server Components First** (Next.js App Router): default to server, opt into client
- **Single Responsibility**: one component = one concern
- **Props Interface**: explicit with interface/type, use `children: React.ReactNode`

```typescript
// Good: explicit props, composition
interface CardProps {
  title: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
}

function Card({ title, children, footer }: CardProps) {
  return (
    <div className="card">
      <h2>{title}</h2>
      {children}
      {footer && <footer>{footer}</footer>}
    </div>
  );
}
```

### 2. Hooks Rules

- **Custom Hooks** for reusable stateful logic (prefix: `use`)
- **Dependencies**: exhaustive deps array, no lint overrides
- **State Location**: lift state to lowest common ancestor
- **useMemo/useCallback**: only for referential equality in deps, not premature optimization

```typescript
// Custom hook pattern
function useUser(userId: string) {
  const { data, error } = useSuspenseQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
  });
  return { user: data, error };
}
```

### 3. Performance (57 Guidelines Core)

- **Re-renders**: `React.memo` at export boundary, stable references, key props
- **Data Fetching**: Suspense + streaming, deduplicate, cache strategically
- **Bundle**: dynamic `import()` for code splitting, tree-shakeable imports
- **Images**: Next.js `Image` with lazy loading, proper sizing, WebP/AVIF

### 4. Next.js App Router

- **File Conventions**: `page.tsx` (route UI), `layout.tsx` (shared shell), `loading.tsx` (Suspense boundary), `error.tsx` (error boundary)
- **Data Fetching**: `fetch` with `cache: 'force-cache'` / `'no-store'`, parallel data fetching with `Promise.all`
- **SEO**: `generateMetadata` (not Head/next/head), sitemap generation, robots.txt
- **Server Actions**: for mutations, progressive enhancement

```typescript
// App Router page with metadata + parallel fetch
export const metadata: Metadata = {
  title: 'Dashboard',
  description: 'User dashboard',
};

export default async function DashboardPage() {
  const [user, posts] = await Promise.all([
    getCurrentUser(),
    getRecentPosts(),
  ]);
  return <DashboardView user={user} posts={posts} />;
}
```

### Resource Files

- [React Performance Deep Dive](resources/react-performance.md) — re-render debugging, bundle analysis, virtualization
- [Next.js Patterns](resources/nextjs-patterns.md) — middleware, auth, ISR, SSR strategies
- [Vercel 57 Guidelines Summary](resources/vercel-57.md) — condensed reference of all 57 rules
