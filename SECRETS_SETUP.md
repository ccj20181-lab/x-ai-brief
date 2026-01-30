# GitHub Secrets 配置指南

## 📝 需要配置的 Secrets

在 GitHub 仓库中依次添加以下 Secrets：

### 1. ANTHROPIC_API_KEY
```
Name: ANTHROPIC_API_KEY
Value: ede5dcfb6ee24bc1abb5e6a14887d6c7.wPIlUa0hkFFD9mbM
```
*说明: 智谱 AI API Key，用于 Claude API 调用*

### 2. BIRD_AUTH_TOKEN
```
Name: BIRD_AUTH_TOKEN
Value: 48a507f0d909e68596a41eeff6f8308502f7da83
```
*说明: X.com Auth Token，用于 Bird CLI 抓取推文*

### 3. BIRD_CT0
```
Name: BIRD_CT0
Value: 53f1990b6fccdbf610c115aee1870acc4e0d694fc5a434f91019aabc9dbd79131d4aee86cb73d70d629a77c208b44b7ae55899d9ef2f426c18879c3013d2beb3f9dd439a539f8453984cc027590a9127
```
*说明: X.com CT0 Token，用于 Bird CLI 身份验证*

### 4. PUSHPLUS_TOKEN (可选)
```
Name: PUSHPLUS_TOKEN
Value: a6443f3a5d0f4b11a42c281f831b5c15
```
*说明: 微信推送 Token，用于推送简报到微信*

---

## 🔧 配置步骤

### 方法一：通过网页配置

1. 打开你的 GitHub 仓库
2. 点击 **Settings** 标签
3. 左侧菜单找到 **Secrets and variables** → **Actions**
4. 点击 **New repository secret**
5. 依次添加上述 4 个 Secrets

### 方法二：使用 GitHub CLI (gh)

```bash
# 安装 GitHub CLI (如果未安装)
# brew install gh

# 登录 GitHub
gh auth login

# 添加 Secrets
gh secret set ANTHROPIC_API_KEY "ede5dcfb6ee24bc1abb5e6a14887d6c7.wPIlUa0hkFFD9mbM"
gh secret set BIRD_AUTH_TOKEN "48a507f0d909e68596a41eeff6f8308502f7da83"
gh secret set BIRD_CT0 "53f1990b6fccdbf610c115aee1870acc4e0d694fc5a434f91019aabc9dbd79131d4aee86cb73d70d629a77c208b44b7ae55899d9ef2f426c18879c3013d2beb3f9dd439a539f8453984cc027590a9127"
gh secret set PUSHPLUS_TOKEN "a6443f3a5d0f4b11a42c281f831b5c15"
```

---

## ✅ 验证配置

配置完成后，可以通过以下方式验证：

### 1. 查看 Secrets 列表
```bash
gh secret list
```

### 2. 手动触发测试
在 GitHub 仓库页面：
- 进入 **Actions** 标签
- 选择 **X AI 博主精选简报** 工作流
- 点击 **Run workflow** → **Run workflow**

---

## 📅 定时任务

系统已配置为每天 **北京时间 07:00** 自动运行（UTC 时间 23:00）

---

**配置完成后，系统将自动每天抓取 X AI 博主内容并推送简报到微信！**
