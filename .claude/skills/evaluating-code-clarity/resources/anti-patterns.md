# Anti-Patterns Catalog

## Naming Smells

| Smell | Bad | Good |
|---|---|---|
| Type prefix | `IUserService`, `TUser` | `UserService`, `User` |
| Hungarian notation | `strName`, `iCount` | `name`, `count` |
| Generic manager | `DataManager`, `Utils` | `UserRepository`, `StringFormatter` |
| Abbreviations | `usr`, `conf`, `msg` | `user`, `config`, `message` |

## Function Smells

- **Too many params**: `function createUser(name, email, role, plan, locale, tz)` → use options object
- **Boolean trap**: `function process(order, isUrgent, isTest)` → split or use enum
- **Flag parameters**: `render(true)` vs `renderWithHeader()` — prefer explicit function names
- **Side effects**: function modifies global state silently → make side effects explicit
- **Return chaos**: returns `string | null | undefined | false` → union type with Result

## Code Structure Smells

- **God object**: one class does everything → split by responsibility
- **Shotgun surgery**: one change requires edits in 10 files → consolidate logic
- **Callback pyramid**: 3+ levels of nesting → extract or use async/await
- **Copy-paste inheritance**: same logic in 3 places → extract to shared function
- **Premature abstraction**: one-use wrapper "for future flexibility" → YAGNI

## TypeScript-Specific Smells

- **`any` proliferation**: `any` in → `any` out → use `unknown` + type guards
- **Type assertion abuse**: `as SomeType` → prefer `satisfies` or type narrowing
- **Over-engineering generics**: `<T extends Record<string, unknown>>` when `T` is unused → remove
- **`namespace` for modules**: ES modules exist now → use `export/import`
