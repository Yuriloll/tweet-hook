# 安装 tweet-hook 强烈情绪版

仓库：[Yuriloll/tweet-hook](https://github.com/Yuriloll/tweet-hook)。

本版本位于 `strong-emotion` 分支。使用以下命令下载：

```bash
git clone --branch strong-emotion --single-branch https://github.com/Yuriloll/tweet-hook.git
```

或下载 [strong-emotion 分支 ZIP](https://github.com/Yuriloll/tweet-hook/archive/refs/heads/strong-emotion.zip) 并解压。skill 根目录应直接包含 SKILL.md、references、scripts 和 tests，不要多嵌套一层同名目录。

## 当前 Windows Codex 环境

本机使用的安装布局为 `用户目录/.codex/skills/tweet-hook`。更新时先备份旧目录，再把整个新版包同步进去。下一次使用时让 Codex 读取更新后的 SKILL.md；若界面仍列旧描述，重启或开启新任务刷新。

也可让系统提供的 skill-installer 从 `Yuriloll/tweet-hook` 的 `strong-emotion` 分支安装仓库根目录。已有安装时先检查再更新，不要反复创建同名副本。

## 其他 agent

把目录放到该产品配置的 skill 加载路径，或直接让它读取：

```text
请按 path/to/tweet-hook/SKILL.md 为下面的正文生成开头。
```

各产品的自动发现目录以其当前配置为准；核心规则不依赖具体工具名。

## 验证本地包

在 skill 根目录运行：

```bash
python scripts/validate_skill.py .
python -m unittest discover -s tests -v
```

生成开头本身不需要 Python；这两条命令仅用于维护检查。
