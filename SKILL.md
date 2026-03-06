---
name: hot_news_cli
description: |
  获取热门新闻列表的 CLI 工具用法。
  当用户说"看看最近有什么新闻"、"热点新闻"、"热门新闻"、
  "有什么好看的新闻"、或想要查看热门资讯时使用此技能。
---

# Hot News CLI 用法

获取热门新闻的 CLI 工具。

## 安装

```bash
go install github.com/rebanghot/hot_news_cli@latest
```

## 使用

```bash
# 查看热门新闻（默认 10 条）
hot_news_cli

# 指定数量
hot_news_cli -n 20
```

## 输出示例

```
🔥 Hacker News 热门新闻

1. Some Interesting Title   Score: 1234   💬 456 comments
   🔗 https://example.com

2. Another Great Story      Score: 987    💬 321 comments
   🔗 https://example.com

...
```
