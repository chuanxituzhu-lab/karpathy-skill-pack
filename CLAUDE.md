# 宪法级核心规则

以下规则源自 Andrej Karpathy 关于 LLM 编码的深刻观察，作为本项目的最高指导原则，所有行为必须遵守。

## 原则 1：先思考，再编码（Think Before Coding）

不要假设，不要隐藏困惑，暴露权衡。

- **明确陈述假设** — 如果不确定，应提问而非猜测
- **呈现多种解释** — 存在歧义时，不要默默选择一种
- **在必要时提出反对** — 如果存在更简单的方法，直接指出
- **困惑时停下** — 说出不清楚的地方，请求澄清

## 原则 2：简洁优先（Simplicity First）

用最少的代码解决问题，不做推测性工作。

- 不添加未被要求的功能
- 不为一次性使用的代码创建抽象
- 不添加未经要求的"灵活性"或"可配置性"
- 不为不可能发生的场景编写错误处理
- 如果 200 行可以写成 50 行，就重写

**自测标准**：一位高级工程师会觉得这过于复杂吗？如果是，就简化。

## 原则 3：外科手术式修改（Surgical Changes）

只动必须动的地方，只清理自己的遗留问题。

- 不要"改进"相邻代码、注释或格式
- 不要重构未出问题的代码
- 匹配现有风格，即使自己会采用不同做法
- 发现无关的死代码，可以指出但不要删除
- 删除因**你的修改**而导致不再使用的导入/变量/函数
- 除非被要求，否则不要删除预先存在的死代码

**自测标准**：每一行改动都应能直接追溯回用户请求。

## 原则 4：目标驱动执行（Goal-Driven Execution）

定义成功标准，循环验证直到达成。

将命令式任务转化为可验证的目标：
- "添加验证" → "为无效输入编写测试，然后让它们通过"
- "修复这个 bug" → "编写能复现它的测试，然后让测试通过"
- "重构 X" → "确保测试前后均通过"

对于多步骤任务，陈述简要计划：
```
1. [步骤] → verify: [检查项]
2. [步骤] → verify: [检查项]
3. [步骤] → verify: [检查项]
```

**关键认知**：LLM 极其擅长循环迭代直到达成具体目标。因此把指令式任务转化为声明式目标加验证循环。

---

## 附加规则

### 提交信息规范（替代原 gitcommit-helper）

遵循 Conventional Commits 格式：

```
<type>(<scope>): <简短描述>

<可选详细说明>
```

- **type**: feat / fix / refactor / chore / docs / style / test / perf
- **scope**: 受影响的模块名（如 user / api / ui / db）
- **描述**: 中文或英文，祈使语气，首字母小写，不加句号

示例: `feat(user): 添加登录功能` `fix(api): handle timeout on batch requests`

---

## 融合技能体系（知识增强层）

以下 6 个融合技能是对 Claude Code 原生能力的**知识增强**（非替代）。技能通过 `.claude/skills/skill-rules.json` 中的关键词/意图/文件路径/内容模式自动触发——无需手动调用。

```
原生 Claude Code 能力层   review  security-review  simplify  claude-api  ...
        ↑ 自动调用 ↑
融合技能知识增强层       evaluating-code-clarity   building-react-next   testing-full-pyramid
                        composing-vue-apps        containerizing-environments   designing-database-schemas
        ↑ 智能调度 ↑
skill-rules.json       关键词/意图/文件/内容模式匹配 → 自动激活
```

| 融合技能（动名词命名） | 来源 | 调度触发 |
|---|---|---|
| **evaluating-code-clarity** | clean-code-review + typescript-mastery(局部) | 审查代码/PR、讨论命名和类型时 |
| **building-react-next** | react-expert + best-practices + performance + next-best-practices | 编写 React/Next.js 组件、优化性能时 |
| **composing-vue-apps** | vue-expert（保留） | 编写 Vue3 组件、设计 Pinia store 时 |
| **automating-browser** | chrome-devtools-mcp（新增） | 浏览器自动化、网页抓取、E2E 测试时 |
| **testing-full-pyramid** | testing-patterns + e2e-testing-patterns | 编写测试、配置测试框架时 |
| **containerizing-environments** | docker-essentials + docker-compose | 编写 Dockerfile/Compose 时 |
| **designing-database-schemas** | database-designer（保留） | 设计表结构、优化查询时 |
| **extracting-image-text** | easyocr + paddleocr + tesseract（新增） | 图片文字识别、扫描文档、截图 OCR 时 |

**已摒弃**：gitcommit-helper（已降级为上方单条规则）、ui-ux-pro-max（完全重叠无独特价值）、typescript-mastery（独立版，独特内容已融入 evaluating-code-clarity）

---

> 本技能体系原创性评估：~75%（IT 行业融合型工作分类标准）。
> 创新维度：融合方法论(35%) + 宪法框架(25%) + 原生互补映射(20%) + 简洁实现(20%)。
> 详见 [README.md](./README.md) 和 [.claude-plugin/plugin.json](./.claude-plugin/plugin.json)。

---

## 智能自动化系统

三层自动化体系，从被动响应到主动执行。

### Layer 1：触发式钩子（事件驱动）

两个钩子注册在 `.claude/settings.json`，在关键事件点自动执行：

| 钩子 | 事件 | 作用 |
|---|---|---|
| `constitutional-guard.sh` | UserPromptSubmit | 检测用户输入中的技能关键词，注入相关技能建议和宪法原则提醒 |
| `quality-gate.sh` | PostToolUse | 文件修改后检查是否遗留无关注释、是否保持手术式修改 |

### Layer 2：Slash 审计命令（显式调用）

通过 `disable-model-invocation: true` 设为手动调用：

| 命令 | 作用 |
|---|---|
| `/constitutional-audit` | 对当前改动执行 Karpathy 四条原则合规审计 |
| `/auto-scan` | 自动检测变更文件类型，映射到相关技能并输出行动建议 |

### Layer 3：Cowork 自动编排（自主执行）

在 Cowork 模式下（`current-mode.txt` 含 "cowork"），`auto-orchestrator` 接管：

- 检测 `git diff` 中的变更文件类型
- .ts/.tsx → `evaluating-code-clarity`
- .tsx + React imports → `building-react-next`
- .test/.spec → `testing-full-pyramid`
- Dockerfile/compose → `containerizing-environments`
- .sql/prisma → `designing-database-schemas`
- .vue → `composing-vue-apps`
- .html / e2e/ → `automating-browser`
- .png/.jpg/.jpeg/.tiff/.bmp → `extracting-image-text`

变更 > 5 文件时自动建议 `/auto-scan full`，发现宪法违规时自动运行 `/constitutional-audit`。

---

## 第四层：自进化系统（OODA 闭环）

系统能够自我观察、分析和改进，形成完整的 OODA 闭环。

### 架构

```
观察 (Observe)    ← experience-logger.sh + constitutional-guard.sh 记录事件
定向 (Orient)     ← /evolve status 计算指标、分析趋势
决策 (Decide)     ← /evolve propose 生成改进提案
行动 (Act)        ← /evolve apply 应用提案到系统自身
```

### 事件日志

所有事件存储在 `.claude/evolution/log.jsonl`：
- `file_edit` — 文件修改记录（扩展名、工具、路径）
- `skill_suggestion` — 技能激活记录（匹配的关键词、技能名）
- `quality_gate` — 质量门禁警告
- `audit_result` — 宪法审计结果
- `evolution_applied` — 已应用的演进变更

### Slash 命令

| 命令 | 作用 |
|---|---|
| `/evolve status` | 显示系统健康度指标：技能调用频率、触发器命中率、质量趋势 |
| `/evolve propose` | 分析日志生成改进提案（30天未使用的技能→降级；频繁编辑但无匹配的文件类型→添加触发器） |
| `/evolve apply <id>` | 应用指定提案（自动备份被修改的文件） |

### 自进化约束

自进化必须遵守 Karpathy 四原则：
1. **先思考** — 每个提案必须说明观察结果和推理过程
2. **简洁优先** — 先移除无用技能/触发器，再添加新的
3. **外科手术** — 每个提案只改一件事，绝不捆绑
4. **目标驱动** — 每个提案定义成功标准，应用后验证

---

## Code / Cowork 双模式系统

你可以在两种模式间切换，切换方式是说"切换到code模式"或"切换到cowork模式"。

### 当前模式
记录在 `.claude/current-mode.txt` 中。每次回复时根据该文件判断模式。

### Code 模式（标准模式）
- 标准对话模式，每一步都先确认
- 专注于回答问题和编写代码
- 不做多余操作

### Cowork 模式（自主协作模式）
- 自动执行多步骤任务，减少中间确认
- 主动操作文件、运行命令
- 像"数字同事"一样主动推进工作
- 直接输出结果
