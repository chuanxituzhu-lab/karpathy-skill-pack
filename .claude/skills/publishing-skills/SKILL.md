---
name: publishing-skills
description: 技能/Agent 发布原则。每次发布新 skills 或 agents 时必须遵循的命名、原创性、蒸馏和发布流程。
---

# 技能/Agent 发布原则

每次创建或发布 skills/agents 时，按以下流程执行。

---

## 一、命名规则（Naming）

必须使用**动名词（Gerund）**格式：`{动作}-{领域}`

| 正确 ✅ | 错误 ❌ |
|---------|---------|
| evaluating-code-clarity | code-quality-review |
| building-react-next | react-helper |
| testing-full-pyramid | test-patterns |
| publishing-skills | skill-publisher |

禁止：品牌名、版本号、模糊泛词（helper/utils/tools）

---

## 二、蒸馏流程（Distillation）

新增技能必须经过 6 步蒸馏：

```
Step 1  收集原始知识源
   ↓
Step 2  合并重叠（相似度>70%必须合并）
   ↓
Step 3  安全审核（禁止: base64/curl远程/命令注入）
   ↓
Step 4  负熵验证（新技能数 < 旧技能数 或 覆盖新领域）
   ↓
Step 5  宪法约束（是否遵守 Karpathy 4 原则）
   ↓
Step 6  注册触发（关键词 + 意图 + 文件路径 + 内容模式）
```

---

## 三、可发布性判断

```
该技能是否与已有技能高度重叠（>50%相似）？
├─ 是 → 合并或摒弃
└─ 否 → 功能价值是否明确？
  ├─ 否 → 摒弃
  └─ 是 → 安全审核通过？
    ├─ 否 → 重设计
    └─ 是 → 是否为原创（区别于直接复现）？
      ├─ 否 → 增加独特视角
      └─ 是 → ✅ 可发布
```

---

## 四、发布清单（Release Checklist）

### 发布前
- [ ] 命名符合动名词规范
- [ ] 不与现有技能冲突
- [ ] SKILL.md 含完整 YAML frontmatter
- [ ] 安全审核通过（无恶意内容）
- [ ] 已注册 skill-rules.json 触发条件
- [ ] 已更新 plugin.json
- [ ] 已更新 CLAUDE.md / README.md 技能表

### 发布后
- [ ] git commit + push
- [ ] 打版本标签：`git tag v{version} && git push --tags`
- [ ] 验证：在新会话中技能可被自动触发

---

## 五、禁止行为（Anti-Patterns）

| 禁止 | 原因 |
|------|------|
| 复制官方技能不改名 | 抄袭，无法通过原创性检查 |
| 添加未蒸馏的原始知识源 | 增加系统熵，违反负熵原则 |
| 同时发布多个相似技能 | 应合并为一个 |
| 添加可执行恶意命令的技能 | 安全红线 |
| 修改原生 Claude Code 行为 | 违反宪法原则 3（外科手术式） |
