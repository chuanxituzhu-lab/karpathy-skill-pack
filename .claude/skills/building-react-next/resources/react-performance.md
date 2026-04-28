# React Performance Deep Dive

## Re-render Debugging

### Step 1: Identify the Problem
```bash
npm install why-did-you-render @welldone-software/why-did-you-render
```

```typescript
if (process.env.NODE_ENV === 'development') {
  const whyDidYouRender = require('@welldone-software/why-did-you-render')
  whyDidYouRender(React, { trackAllPureComponents: true })
}
```

### Step 2: Fix Common Causes

| Cause | Fix |
|---|---|
| Inline function props | `useCallback` or extract to module level |
| Inline object/array props | `useMemo` with stable deps |
| Context re-renders | Split context, use selectors, `use-context-selector` |
| Too many state updates | Batch with `unstable_batchedUpdates` (React 18 auto-batches) |
| Large lists | Virtualize with `react-window` / `@tanstack/virtual` |

### Step 3: Measure
```typescript
import { Profiler } from 'react'

function onRender(id, phase, actualDuration) {
  if (actualDuration > 50) console.warn(`${id} is slow (${actualDuration}ms)`)
}

<Profiler id="Dashboard" onRender={onRender}>
  <Dashboard />
</Profiler>
```

## Bundle Optimization

```javascript
// Dynamic import for code splitting
const Chart = dynamic(() => import('./Chart'), {
  loading: () => <Skeleton />,
  ssr: false,  // if chart needs window
})
```

## Data Fetching Rules

1. **Suspense + streaming** over waterfall `useEffect` chains
2. **Deduplicate** requests (TanStack Query / SWR handle this)
3. **Prefetch** likely navigations (`
