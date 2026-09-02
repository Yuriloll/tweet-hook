# List Research: 2067293665865998356

- **List URL:** https://x.com/i/lists/2067293665865998356
- **Research date:** 2026-07-10
- **Method:** 列表抽样成员 + 各账号高赞帖（L3 检索时采集；任意 AI 可只读本库）
- **目标:** 每人约 8–10 条高赞开头 → 总结风格 → 供 tweet-hook **离线/在线** 生成用
- **当前表格记录数:** 90（以 `swipe-openers.md` 的实际数据行为准）
- **Portable:** 本目录纯 Markdown，Codex / Claude / Cursor / Grok 均可直接读

## Limits（务必读）

1. **无法导出完整 List 成员名单**（X 列表页需登录；工具无 List Members API）。
2. 成员来自列表时间线 **抽样**；若列表很大，本库是 **高活跃子集**，不是 100% 全员。
3. 「历史高赞」受搜索索引影响：优先返回可检索到的高互动帖；个别账号不足 10 条达标帖时按实际条数记。
4. **官方账号**（OpenAI / Anthropic 等）互动极高但开头是 PR 体，**不作为个人博主钩子训练主样本**（见 `official-pr.md` 简述）。
5. 赞数会变，文中为抓取时快照。

## Covered creators (personal / mid-size)

| Handle | 定位简述 | 表格记录数 |
|--------|----------|------------|
| @dontbesilent | 商业/内容方法论 · dbskill | 13 |
| @Saccc_c | AI 财富/产品 demo · build | 10 |
| @Phoenixyin13 | 认知/物理/AI 长评 | 11 |
| @Pluvio9yte | AI coding · 自媒体变现 · skill 开源 | 10 |
| @xiaohu | AI 资讯 · 测评 · 热点解读 | 10 |
| @bozhou_ai | AI coding 实战 · 教程 | 9 |
| @CuiMao | AI 视频 · 情绪/段子 | 9 |
| @xingbugengming | 零基础 vibe coding · 教程视频 | 8 |
| @nake13 | Coding agent · 圈内判断 | 10 |

## Files

- `swipe-openers.md` — 逐人开头拆解 + 可复用骨架 + 跨账号规律
- `official-pr.md` — 官方号开头对照（少用）

## Refresh

本 Skill 没有注册 `/tweet-hook refresh` 可执行命令。需要刷新时，用自然语言要求 Agent：

```text
使用 tweet-hook 重新研究 list 2067293665865998356，记录本轮日期和能力级别，更新可核实样本、逐账号记录数与总数，不把历史互动快照写成当前数据。
```

L1 环境下由用户粘贴新增成员或样本；L2/L3 环境可做外部研究。更新后运行 `python3 scripts/validate_skill.py .`。
