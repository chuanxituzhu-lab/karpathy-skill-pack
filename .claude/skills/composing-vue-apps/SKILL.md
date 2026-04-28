---
name: composing-vue-apps
description: This skill should be used when the user asks to "build a Vue 3 app", "use Composition API", "set up Pinia", "configure Vue Router", "create composables", "migrate from Options API", or discusses "Vue 3", "Nuxt", "script setup", "ref", "reactive", "computed", "watch", "defineProps", "Vue state management", or "Vue performance". Covers Vue 3 Composition API, Pinia state management, Vue Router patterns, reactive system mastery, and TypeScript integration.
version: 1.0.0
---

# Vue 3 Expert

## Purpose

Complete solution guide for Vue 3 development: Composition API, Pinia, Vue Router, TypeScript integration, and production patterns.

## When to Use

Auto-activates when:
- Creating Vue 3 components or composables
- Designing state management with Pinia
- Setting up Vue Router with guards
- Writing `<script setup>` composition logic
- Migrating Options API → Composition API
- Discussing reactive patterns or Vue performance

## Core Patterns

### 1. Composition API
```vue
<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'

interface Props {
  userId: string
}
const props = defineProps<Props>()
const emit = defineEmits<{
  update: [value: string]
}>()

const data = ref<User | null>(null)
const isLoading = computed(() => data.value === null)

watch(() => props.userId, async (id) => {
  data.value = await fetchUser(id)
})
</script>
```

### 2. Pinia State Management
```typescript
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const posts = ref<Post[]>([])

  const displayName = computed(() =>
    user.value ? `${user.value.name} (${user.value.role})` : ''
  )

  async function fetchUser(id: string) {
    user.value = await api.getUser(id)
  }

  return { user, posts, displayName, fetchUser }
})
```

### 3. Best Practices

- **Script Setup**: always use `<script setup lang="ts">`
- **Typed Props**: `defineProps<Props>()` over runtime declarations
- **Composables**: extract reusable logic to `useXxx` composables
- **Reactivity**: `ref` for primitives, `reactive` for objects, `computed` for derived
- **Watchers**: explicit `deep: true` only when needed, use immediate for init
- **Lifecycle**: `onMounted` for async init, `onUnmounted` for cleanup

### Resource Files
- [Vue3 Advanced Patterns](resources/vue3-advanced.md) — composables, custom directives, render functions
- [Vue Performance](resources/vue-performance.md) — hydration, chunk splitting, reactive tuning
