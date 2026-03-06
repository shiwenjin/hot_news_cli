---
name: hot_news_cli
description: |
  获取热门新闻列表的 CLI 工具用法。
  当用户说"看看最近有什么新闻"、"热点新闻"、"热门新闻"、
  "有什么好看的新闻"、或想要查看热门资讯时使用此技能。
---

# Hot News CLI 用法

多平台热榜命令行工具（Python 项目）。

## 安装

```bash
# 克隆项目
git clone https://github.com/shiwenjin/hot_news_cli.git
cd hot_news_cli

# 本地安装为 CLI
pip install -e .
```

或者使用 uv：

```bash
uv pip install -e .
```

## 使用

```bash
# 查看热门新闻
hot-news

# 指定数量
hot-news --count 20
```

## 输出示例

```
🔥 热门新闻

1. Some Interesting Title   💬 456 comments
   🔗 https://example.com

2. Another Great Story      💬 321 comments
   🔗 https://example.com

...
```
