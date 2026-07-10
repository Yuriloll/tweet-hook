---
name: tweet-hook
description: >
  Multi-agent skill: research viral social openers (X/Twitter etc.) and generate
  high-stop-rate tweet/post openings (contradiction, anxiety, topic, heat, hooks).
  Portable across Grok Build, Codex, Claude Code, Cursor, and similar agents.
  Use when the user wants tweet hooks, 推文开头, 爆款开头, hook formulas, X copy,
  or runs /tweet-hook.
metadata:
  short-description: "多 AI 通用：爆款推文开头研究 + 生成"
  compatible: "grok-build, codex, claude-code, cursor, copilot-chat, generic-agents"
---

# tweet-hook（多 AI 通用 · 爆款推文开头）

帮用户拆解高互动帖的**开头钩子**，并批量生成可直接发布的开头。  
**默认中文**；用户用其他语言时跟随用户。

本 skill **不绑定单一厂商工具名**。先探测环境能力，再选路径。

---

## 0. Runtime capability probe（先做这个）

调用任何「抓帖」能力前，判断当前 agent 具备哪一类能力（有则用，无则降级）：

| 级别 | 能力 | 典型环境 |
|------|------|----------|
| **L3** | 原生 X/Twitter 搜索、用户帖、list 检索 | Grok Build（`x_*` 工具）等 |
| **L2** | 网页搜索 / 打开 URL / 浏览器 | Codex、Claude Code、Cursor（视配置） |
| **L1** | 只能读本地文件 + 推理 | 无网络、或未开 MCP 的 agent |

**降级规则（必须遵守）：**

1. **有 L3** → 走「实时研究」+ 本地 swipe 库  
2. **仅 L2** → 用搜索/打开 `https://x.com/{handle}` 或公开转载页；抓不到互动数就标「未验证」  
3. **仅 L1** → **禁止假装刚抓了 X**；只用本仓库 `references/` 骨架 + 用户粘贴的原文生成  
4. 任何级别都**禁止编造**赞/转/浏览量

向用户简短说明当前模式，例如：`当前：L1 离线库模式` / `当前：L3 实时检索`。

---

## 1. What this skill does

| 能做 | 说明 |
|------|------|
| 研究开头 | 从高互动帖截取前 1–2 句，归类、抽骨架 |
| 五类钩子 | 矛盾 / 焦虑 / 话题 / 热度 / 钩子 |
| 批量生成 | 按主题输出可粘贴开头 + 类型/风险/场景 |
| 风格复刻 | 「像 @某博主」「像列表里 xxx 体」 |
| 沉淀 swipe | 把新骨架追加进 references（用户要求时） |

| 做不到 | 说明 |
|--------|------|
| 导出完整 following / list 全员 | 需用户粘贴 handle 或提供可检索 list |
| 读私密账号 | 不可用则跳过 |
| 保证各 AI 工具 API 一致 | 用能力分级，不写死唯一 API |

---

## 2. When invoked

1. 确认任务：`研究` / `生成` / `两者`  
2. 确认语种、赛道、目标（涨粉 / 讨论 / 转化 / 收藏）  
3. 输入来源（有一即可）：
   - handle 列表 `@a @b`
   - 公开 List 链接 / id
   - 用户粘贴的爆款原文
   - 仅主题（则用本地 swipe + 通用句式）  
4. 跑 **§0 能力探测**，选定 L1/L2/L3

---

## 3. Knowledge base（所有 AI 必读）

生成或研究时，按需读取本 skill 目录下文件（路径相对 skill 根目录）：

| 文件 | 用途 |
|------|------|
| `references/hook-patterns.md` | 五类钩子定义 + 通用骨架 |
| `references/list-2067293665865998356/swipe-openers.md` | 实战高赞开头拆解 + 15 模板 |
| `references/list-2067293665865998356/README.md` | 样本范围与限制 |
| `references/list-2067293665865998356/official-pr.md` | 官方 PR 体对照（少学） |

若用户说「按我列表风格」或提到 list `2067293665865998356`：  
**优先套用 swipe-openers 的骨架与组合表**，再套用户主题。

---

## 4. Research workflow（研究模式）

目标账号建议每轮 **5–15 个**；每人尽量 **5–10 条** 高互动原创帖（转发降权）。

### 4.1 采集（按级别）

**L3 — 原生 X 检索（示例：Grok）**

- 关键词/高级搜：`from:{handle} min_faves:{N}`  
- List：`list:{id}`  
- 语义搜：焦虑/争议/反常识 + 限定 usernames  
- 长帖：取线程全文，仍只分析开头  

N 按体量调：小号 20–100，中号 100–500，大号更高。

**L2 — 通用网页能力**

- 搜索：`site:x.com from {handle}` 或 `"{独有短句}"`  
- 打开用户主页、状态链接；能读到正文与大致热度则记录  
- 打不开或登录墙：请用户粘贴原文 / 截图文字  

**L1 — 仅本地**

- 请用户粘贴 3–20 条爆款全文，或直接基于 `references/` 做「风格仿写」  
- 输出中标注：`样本来源：本地库 / 用户粘贴`

### 4.2 只分析「开头」

每条截取 **前 1–2 句 / 前约 40–80 字**（到首个换行或强标点）：

| 字段 | 说明 |
|------|------|
| 账号 | @handle 或「用户粘贴」 |
| 开头原文 | 原话 |
| 类型 | 矛盾 / 焦虑 / 话题 / 热度 / 钩子（可叠加） |
| 机制 | 为何停滑（一句） |
| 互动 | 有则记，无则「未验证」 |
| 骨架 | 去实体后的句式 |

### 4.3 必须输出的归纳

覆盖五类，每类：**定义一句 + 2–4 骨架 + 1 条改写示例**。  
详细类型库见 `references/hook-patterns.md`（引用骨架即可，勿整文件贴给用户）。

---

## 5. Generation workflow（生成模式）

用户给出主题 / 产品 / 观点后：

1. 读 `hook-patterns.md`；若相关再读 `swipe-openers.md`  
2. 按目标选 **2–3 个** 钩子类型（可 2 型叠加，见 swipe 组合表）  
3. 每类生成 **3–5 条** 可粘贴开头；可标「像 @xxx 体」  
4. 每条标注：`类型 | 风险(低/中/高) | 适合(涨粉/讨论/转化/收藏)`  
5. 给 **1 安全版 + 1 进攻版**  
6. 可选：补「开头后第一句怎么接」，避免标题党断崖  

### 写作约束

- 一行内建立冲突、缺口或数字；少形容词  
- 焦虑类 = 揭示代价，不是恐吓诈骗  
- 无真实数据时不写假精确数字；可用「据我观察 / 我们测下来」  
- 中文开头常见 **15–40 字**；英文约 **8–16 words**  
- 脏话/攻击性口语仅当用户人设需要且明确要求  

### 无检索时的合格输出

即使 L1，也必须给出：可用开头列表 + 骨架 + 不建议写法。  
不得声称「刚从 X 抓了全网爆款」除非本轮真实检索过。

---

## 6. Output templates

### 研究

```markdown
## 运行模式
L1 / L2 / L3

## 样本池
...

## 开头拆解表
| 账号 | 开头 | 类型 | 机制 | 骨架 |

## 五类规律
### 矛盾 / 焦虑 / 话题 / 热度 / 钩子

## Top 句式
1. ...
```

### 生成

```markdown
## 运行模式
L1 / L2 / L3

## 主题
...

## 推荐开头
1. ...  — 类型 | 风险 | 适合
2. ...

## 骨架
- ...

## 安全版 / 进攻版
- ...

## 不建议
- ...
```

---

## 7. Quality bar

- 开头单独出现时，读者 0.5s 内知道「有冲突/有缺口/有结果」  
- 去掉形容词仍成立  
- 同批开头同一骨架不超过 2 次  
- 像广告口号 → 重写  

---

## 8. Install hints（给用户，非强制）

各产品目录名可能变化，原则：**把本仓库放到该产品的 skills / 指令加载路径**。

| 环境 | 常见做法 |
|------|----------|
| **Grok Build** | `~/.grok/skills/tweet-hook/` 或项目 `.grok/skills/tweet-hook/`；`/tweet-hook` |
| **Claude Code** | 项目 `.claude/skills/tweet-hook/` 或用户 skills 目录；或 `@SKILL.md` |
| **Codex** | 项目 skills / AGENTS 可读路径；或对话中 `@` 本目录 |
| **Cursor** | `.cursor/skills/tweet-hook/` 或 Rules 引用本 `SKILL.md` |
| **任意 Agent** | 将本目录加入仓库，系统提示写：`Follow skills/tweet-hook/SKILL.md` |

详见仓库根目录 `INSTALL.md`。

---

## 9. Optional: extend swipe file

用户要求沉淀时：仅追加 **骨架 + 类型 + 可选一句示例** 到  
`references/swipe-file.md`（可新建）。  
避免大段搬运他人全文；注意平台与版权。

---

## 10. Tool name appendix（可选映射，非唯一）

若当前环境存在下列工具，可优先使用；**没有则忽略，走 L2/L1**：

| 意图 | 可能工具名（随产品而异） |
|------|--------------------------|
| X 关键词/高级搜 | `x_keyword_search`, Twitter/X API MCP, web_search |
| X 语义搜 | `x_semantic_search` |
| 拉帖/线程 | `x_thread_fetch`, `web_fetch`, browser |
| 用户资料 | `x_user_search`, web profile |
| 读本地 skill | `read_file`, 内置 file read |

**禁止**因缺少某一工具名而拒绝生成开头。
