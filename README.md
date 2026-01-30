# 每日 X AI 博主简报生成系统 - GitHub Actions 配置指南

## 📖 项目简介

这是一个基于 Claude Agent Skills 和 GitHub Actions 的自动化 AI 博主内容精选系统。它会每天定时抓取 X(Twitter) 上 20 位优质 AI 博主的高质量推文，通过 AI 分析整理成结构化简报，并自动推送到微信。

### ✨ 核心特性

- ⏰ **全自动定时任务** - 每天自动运行，无需人工干预
- 🐦 **多博主数据抓取** - 精选 20 位 AI 领域优质博主
- 🤖 **AI 智能分析** - 使用 Claude AI 自动筛选、分类、提炼
- 💰 **零成本运行** - GitHub Actions 个人使用完全免费
- 💬 **微信推送** - 集成 PushPlus 自动推送到微信

---

## 🚀 快速开始

### 步骤 1: 准备 GitHub 仓库

1. **创建或使用现有仓库**
   ```bash
   # 在你的 GitHub 账号下创建一个新仓库
   # 例如: x-ai-brief
   ```

2. **将 skill 文件复制到仓库**
   ```bash
   cp -r ~/.claude/skills/x-ai-brief/* ~/Projects/x-ai-brief/
   cd ~/Projects/x-ai-brief
   ```

### 步骤 2: 配置 GitHub Secrets

在 GitHub 仓库中配置以下 Secrets：

1. **打开仓库设置**
   - 进入你的 GitHub 仓库
   - 点击 `Settings` > `Secrets and variables` > `Actions`
   - 点击 `New repository secret`

2. **添加以下 Secrets**:
   ```
   Name: BIRD_AUTH_TOKEN
   Value: 你的 Bird CLI Auth Token

   Name: BIRD_CT0
   Value: 你的 Bird CLI CT0 Token

   Name: ANTHROPIC_API_KEY
   Value: 你的 Claude API Key

   Name: PUSHPLUS_TOKEN (可选)
   Value: 你的 PushPlus Token
   ```

### 步骤 3: 测试运行

**手动触发（推荐）**
1. 进入 `Actions` 标签页
2. 选择 `X AI 博主简报` 工作流
3. 点击 `Run workflow` > `Run workflow`

---

## 📊 数据源配置

当前配置的 20 位 AI 博主：

| 博主 | 专注领域 |
|------|----------|
| 宝玉 (dotey) | Claude Code、Skills、AI工具应用 |
| winter | AI编程、软件工程思考 |
| 冰河 (binghe) | AI工具实战、变现案例 |
| 立党 (lidangzzz) | AI观点、投资 |
| 曾博 (himself65) | AI、投资 |
| 王欣然 (bboczeng) | AI、股市分析 |
| Frank (frankdegods) | AI投资、Claude Code |
| Peter Steinberger (steipete) | Bird/Clawdbot作者 |
| Brave2049 | AI深度思考 |
| KK.aWSB | 科技播客推荐 |
| cafe99 | AI内容创作 |
| 塔子 (tazi8848) | 提示词工程 |
| 熊敬之 (XiongJingzhi) | LangChain、AI工程化 |
| HappyQQ | Skills、MCP |
| 摆烂程序媛 (wanerfu) | AI学习技巧 |
| Simon Wong | AI判断力 |
| boon陈庚阳 (A9Quant) | 金融AI |
| keitaro | Notion AI |
| 老拐瘦 (geyunfei) | AI元应用 |
| 星河 (StarRiverXH) | AI编程工具 |

---

## 📱 微信推送配置（可选）

### 获取 PushPlus Token

1. 访问 [PushPlus官网](https://www.pushplus.plus/)
2. 微信扫码登录
3. 复制你的 Token
4. 添加到 GitHub Secrets: `PUSHPLUS_TOKEN`

---

## 💰 费用说明

### GitHub Actions
- ✅ **个人账户**：每月 2000 分钟免费
- ✅ **公共仓库**：完全免费
- 本次任务每次运行约 2-3 分钟

### Claude API
- 使用 Claude API 生成简报
- 每次生成简报约消耗 2000-3000 tokens
- 成本极低

---

## 📈 输出文件

- `digests/YYYY-MM-DD.md` - 按日期归档的简报
- `digests/latest.md` - 最新简报

简报内容结构：
- 🤖 今日摘要
- 🛠️ AI工具
- ⚙️ AI工作流
- ✍️ 提示词
- 💻 AI编程
- 📝 内容创作
- 🚀 AI应用
- 🧠 AI思考

---

**创建时间**: 2026-01-30
**维护者**: Henry
**许可证**: MIT
