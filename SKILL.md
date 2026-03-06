---
name: hot_news_cli
description: |
  获取热门新闻列表的 CLI 工具用法。
  当用户说"看看最近有什么新闻"、"热点新闻"、"热门新闻"、
  "有什么好看的新闻"、或想要查看热门资讯时使用此技能。
---

# Hot News CLI 用法

多平台热榜命令行工具（Python 项目），支持获取知乎等多个平台的热门内容。

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

## 命令

### 1. 列出所有可用平台

```bash
hot-news list
```

输出示例：

```json
{
  "platforms": [
    {"id": "zhihu", "name": "知乎", "icon": "💬"}
  ],
  "total": 1
}
```

### 2. 获取热榜数据

```bash
# 获取所有平台的热榜（默认每平台 20 条）
hot-news get

# 指定平台
hot-news get zhihu

# 指定返回条数
hot-news get -n 10

# 美化 JSON 输出
hot-news get --pretty

# 指定请求超时时间
hot-news get --timeout 30
```

输出示例：

```json
{
  "version": "1.0",
  "generated_at": "2024-01-01T00:00:00Z",
  "total_platforms": 1,
  "platforms": [
    {
      "id": "zhihu",
      "name": "知乎",
      "icon": "💬",
      "success": true,
      "count": 20,
      "trends": [
        {
          "rank": 1,
          "title": "有什么值得推荐的好书？",
          "description": "最近想读一些好书...",
          "hot": "1234 万热度",
          "url": "https://www.zhihu.com/question/123456",
          "extra": {}
        }
      ]
    }
  ]
}
```

## 选项说明

| 选项 | 简写 | 默认值 | 说明 |
|------|------|--------|------|
| `--limit` | `-n` | 20 | 每平台返回条数 |
| `--pretty` | - | false | 美化 JSON 输出 |
| `--timeout` | - | 10.0 | 请求超时时间（秒） |
