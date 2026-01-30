---
name: x-ai-brief
description: X(Twitter) AI 博主精选简报。每天抓取 20 位顶级 AI 博主的高质量内容，使用 Claude 生成结构化简报，通过 GitHub Actions 自动运行并推送到微信。
---

# X AI 博主精选简报

自动化的每日 AI 博主内容精选系统，抓取 X(Twitter) 上 20 位优质 AI 博主的高质量推文，使用 Claude AI 生成精炼的中文简报。

## 功能

1. **数据源抓取**
   - 使用 Bird CLI 抓取 X 博主推文
   - 20 位精选 AI 领域博主
   - 自动过滤和分类

2. **Claude AI 分析**
   - 内容筛选和质量评估
   - 按主题分类整理
   - 生成结构化简报

3. **输出格式**
   - Markdown 简报文件
   - 微信推送通知 (PushPlus)
   - GitHub Pages 托管

## 使用方法

### 本地运行

```bash
cd ~/.claude/skills/x-ai-brief

# 安装依赖
pip install -r requirements.txt

# 设置环境变量
export BIRD_AUTH_TOKEN="your-auth-token"
export BIRD_CT0="your-ct0-token"
export ANTHROPIC_API_KEY="your-api-key"

# 运行简报生成
python scripts/x_ai_digest.py

# 推送到微信
python scripts/send_pushplus.py
```

### 输出文件

- `digests/YYYY-MM-DD.md` - 日期简报
- `digests/latest.md` - 最新简报

## 文件结构

```
~/.claude/skills/x-ai-brief/
├── scripts/
│   ├── x_ai_digest.py        # 主脚本
│   ├── send_pushplus.py      # 微信推送
│   ├── config.json           # 博主配置
│   └── fetch_tweets.py       # 推文抓取
├── digests/                   # 简报输出目录
├── .github/workflows/         # GitHub Actions
└── requirements.txt           # Python 依赖
```

## 配置

编辑 `scripts/config.json` 可自定义：
- 博主列表
- 过滤条件
- Claude 模型和参数
- 输出目录

## 自动化

GitHub Actions 配置为每天北京时间 07:00 自动运行，需要在 GitHub Secrets 中配置：
- `BIRD_AUTH_TOKEN` - Bird CLI Auth Token
- `BIRD_CT0` - Bird CLI CT0 Token
- `ANTHROPIC_API_KEY` - Claude API 密钥
- `PUSHPLUS_TOKEN` - 微信推送令牌 (可选)
