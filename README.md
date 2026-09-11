# tweet-hook 2.1 · 强烈情绪版

本分支为 `strong-emotion`，提供默认高强度的独立版本。安装时请明确选择这个分支。

```bash
git clone --branch strong-emotion --single-branch https://github.com/Yuriloll/tweet-hook.git
```

也可以下载 [强烈情绪版 ZIP](https://github.com/Yuriloll/tweet-hook/archive/refs/heads/strong-emotion.zip)。具体安装见 [INSTALL.md](INSTALL.md)。

写中文 X 推文开头，默认按用户原始五个案例的高强度来：大判断、巨大反差、身份跃迁、赚钱欲望、行业冲击和强口语。直接给 6 条，最猛的一条排第一。

## 这次改了什么

2.1 根据用户反馈取消生成阶段对素材扩写的限制，删除模板里的降级条件，恢复用户原始案例作为强度基准；同步重写 36 条骨架与示范。支持围绕主题进行创作设定，新增经历或数字的版本统一作为创作草案呈现。

- 14 种情绪机制：解脱、惊讶、捡到宝、崩溃、质疑、迟到领悟、愿望投射等。
- [36 条原创骨架与 6 条成稿示范](references/emotional-openers.md)。
- [阿杭与余温的风格拆解](references/creator-styles.md)。
- 保留用户指定的 [五种优先模板](references/priority-templates.md)，与新机制配合使用。
- [近半年研究](references/research-2026-09.md)：172 条唯一推文 ID，165 条取得文字，48 张精选案例卡。来源为 6551 API 加登录浏览器中的 X 搜索。
- 原有 90 条 List 记录保留为额外参考，不默认塞进每次生成。

这是覆盖 2026-03-11 至 2026-09-11 窗口的逐月抽样，非完整推文集；互动不是开头有效性的因果证据。参见 [机器索引](references/research-2026-09.json)。

## 用法

先按 [安装说明](INSTALL.md) 放到 agent 能读取的 skill 目录，再直接说：

> 用 tweet-hook 帮我改开头，情绪再强一点。正文如下：……

> 给我 6 个更像余温那种“看完就想试”的开头。主题是：……

> 用阿杭那种现场破防的感觉写，只要 3 条。事情是：……

> 按全自动闭环体写，别动后面的正文：……

贴正文或给主题即可写。先挑最能刺激读者的角度，再写强判断，把反差和利害向读者推进。用户可以自由要求更狠、更上头、更有危机感或更像某个作者。需要研究新账号时，再调用数据工具。

## 文件

入口是 [SKILL.md](SKILL.md)，其他 agent 也可直接读取。参考文件按任务加载，不要求某一厂商 API，也不要求多 Agent。

## 验证

```bash
python scripts/validate_skill.py .
python -m unittest discover -s tests -v
```

验证包结构、本地链接、研究来源与计数。文案强度仍需真实输入试写；脚本不预测流量。
