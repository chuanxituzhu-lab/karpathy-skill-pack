# TypeScript Advanced Patterns

> 融合自 `typescript-mastery` 的独特内容。Claude Code 原生理解 TypeScript，但以下高级模式需要专门参照。

## Branded Types

```typescript
type Brand<T, B> = T & { __brand: B }
type UserId = Brand<string, 'UserId'>
type OrderId = Brand<string, 'OrderId'>

function getUser(id: UserId) { /* ... */ }
function getOrder(id: OrderId) { /* ... */ }

getUser('abc' as UserId)  // OK
getUser('abc')            // Error: type safe!
```

## Template Literal Types

```typescript
type EventName = `on${Capitalize<string>}`
type CSSUnit = `${number}${'px' | 'em' | 'rem' | '%' | 'vh' | 'vw'}`
type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE'
type ApiPath = `/api/v1/${string}`
type ApiRoute = `${HttpMethod} ${ApiPath}`
```

## Conditional Types + infer

```typescript
type UnpackPromise<T> = T extends Promise<infer U> ? U : T
type FunctionArgs<T> = T extends (...args: infer A) => unknown ? A : never
type ReturnOf<T> = T extends (...args: unknown[]) => infer R ? R : never

// Real-world: extract element type from Array
type ElementType<T> = T extends (infer U)[] ? U : T
type A = ElementType<string[]>  // string
```

## Mapped Types with Key Remapping

```typescript
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K]
}

type Setters<T> = {
  [K in keyof T as `set${Capitalize<string & K>}`]: (value: T[K]) => void
}

type Person = { name: string; age: number }
type PersonAccessors = Getters<Person> & Setters<Person>
// { getName: () => string; getAge: () => number; setName: (v: string) => void; ... }
```

## satisfies Operator

```typescript
// Validates shape + infers narrowest type
const palette = {
  red: [255, 0, 0],
  green: '#00ff00',
  blue: [0, 0, 255],
} satisfies Record<string, string | number[]>

// palette.green is string (not string | number[])
// palette.red is number[] (not string | number[])
palette.green.toUpperCase()  // OK — inferred as string
```

## Utility Types Cheatsheet

| Pattern | Code |
|---|---|
| Deep Partial | `type DeepPartial<T> = { [K in keyof T]?: T[K] extends object ? DeepPartial<T[K]> : T[K] }` |
| Non-nullable | `type NonNull<T> = T extends null \| undefined ? never : T` |
| Pick by Value | `type PickByValue<T, V> = { [K in keyof T]: T[K] extends V ? K : never }[keyof T]` |
| Union to Intersection | `type UnionToIntersection<U> = (U extends any ? (k: U) => void : never) extends (k: infer I) => void ? I : never` |
