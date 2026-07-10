# tweet-hook

Grok Build **Skill**：研究 X/Twitter 高互动帖的开头钩子，并批量生成可用的推文开头。

适用于：涨粉文案、话题讨论、产品宣发、AI/自媒体/Web3 内容号。

---

## 能干什么

| 能力 | 说明 |
|------|------|
| **抓取研究** | 用 X 搜索读公开高赞帖，按账号拆「开头」 |
| **五类钩子** | 制造矛盾 / 焦虑 / 话题 / 热度 / 抛钩子 |
| **批量生成** | 按主题输出可直接粘贴的开头 + 风险标注 |
| **风格复刻** | 可按某博主风格写（如「像小互 / 像 dontbesilent」） |
| **List 沉淀库** | 内置一份公开 List 的高赞开头拆解与骨架 |

### 内置资料

- `SKILL.md` — 主流程（Grok 读取）
- `references/hook-patterns.md` — 通用句式库
- `references/list-2067293665865998356/` — 列表研究样本与 swipe

### 做不到的

- 无法静默导出他人完整关注列表 / List 全员名单（需你提供 handle 或公开 list 可检索帖）
- 不编造赞转数据；私密号读不到

---

## 安装到 Grok Build

### 方式 A：用户级 Skill（全项目可用）

```bash
mkdir -p ~/.grok/skills/tweet-hook
cp -R ./* ~/.grok/skills/tweet-hook/
```

### 方式 B：项目级 Skill

```bash
mkdir -p .grok/skills/tweet-hook
cp -R ./* .grok/skills/tweet-hook/
```

重启或等待 Grok 自动 reload skills。

---

## 用法

在 Grok Build 中：

```text
/tweet-hook
```

或自然语言：

```text
按列表博主风格，主题：AI 工作流变现，写 12 条推文开头
```

```text
分析 @xxx @yyy 的高赞开头规律
```

---

## 输出会包含

- 开头原文拆解（类型 / 机制 / 骨架）
- 可复用句式
- 生成开头：`类型 | 风险 | 适合场景`
- 安全版 vs 进攻版对照

---

## License

MIT（骨架与方法论可自由使用；引用他人推文原文时请遵守平台规则与合理使用。）
