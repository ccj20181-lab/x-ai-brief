#!/usr/bin/env python3
"""
X AI 博主简报生成器
使用 Bird CLI 抓取 X 博主推文，使用 Claude AI 生成简报
"""

import json
import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

import anthropic
import pytz


# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_PATH = Path(__file__).parent / "config.json"


def load_config() -> dict:
    """加载配置文件"""
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def run_bird_command(username: str, count: int = 20) -> str:
    """运行 Bird CLI 命令抓取推文"""
    cmd = f"bird user-tweets {username} -n {count}"
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            return result.stdout
        else:
            print(f"[警告] @{username} 抓取失败: {result.stderr}")
            return ""
    except subprocess.TimeoutExpired:
        print(f"[警告] @{username} 抓取超时")
        return ""
    except Exception as e:
        print(f"[警告] @{username} 抓取出错: {e}")
        return ""


def parse_bird_output(output: str, blogger_name: str, category: str) -> list:
    """解析 Bird CLI 输出"""
    tweets = []
    if not output:
        return tweets

    blocks = output.split("──────────────────────────────────────────────────")

    for block in blocks:
        if not block.strip():
            continue

        lines = block.strip().split("\n")
        if len(lines) < 3:
            continue

        # 提取推文内容
        content_lines = []
        url = ""
        timestamp = ""

        for line in lines[1:]:
            if line.startswith("🔗"):
                url = line.replace("🔗", "").strip()
            elif line.startswith("📅"):
                timestamp = line.replace("📅", "").strip()
            elif line.strip() and not line.startswith("┌─"):
                content_lines.append(line)

        content = "\n".join(content_lines).strip()

        if content and len(content) > 50:  # 过滤太短的内容
            tweets.append({
                "content": content[:500],  # 限制长度
                "url": url,
                "timestamp": timestamp,
                "author": blogger_name,
                "category": category
            })

    return tweets


def fetch_tweets_from_bloggers(config: dict) -> list:
    """从所有博主抓取推文"""
    feeds_config = config["rss_feeds"]
    all_tweets = []

    def fetch_single_blogger(key, info):
        print(f"  - 抓取 @{key}...")
        output = run_bird_command(info["url"], 20)
        tweets = parse_bird_output(output, info["name"], info["category"])
        print(f"    获取 {len(tweets)} 条")
        return tweets

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {
            executor.submit(fetch_single_blogger, key, info): key
            for key, info in feeds_config.items()
        }
        for future in as_completed(futures):
            tweets = future.result()
            all_tweets.extend(tweets)

    return all_tweets


def filter_tweets(tweets: list, config: dict) -> list:
    """过滤推文"""
    filters = config.get("filters", {})
    min_length = filters.get("min_length", 50)
    exclude_keywords = filters.get("exclude_keywords", [])
    include_keywords = filters.get("include_keywords", [])

    filtered = []
    for tweet in tweets:
        content = tweet.get("content", "")

        # 长度检查
        if len(content) < min_length:
            continue

        # 排除关键词
        if any(kw in content for kw in exclude_keywords):
            continue

        # 包含关键词（可选）
        if include_keywords:
            if not any(kw in content for kw in include_keywords):
                continue

        filtered.append(tweet)

    return filtered


def prepare_content_for_claude(tweets: list) -> str:
    """准备发送给 Claude 的内容"""
    sections = []

    # 按分类分组
    by_category = {}
    for tweet in tweets:
        cat = tweet.get("category", "其他")
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(tweet)

    for cat, tweet_list in by_category.items():
        cat_items = []
        for tweet in tweet_list[:10]:  # 每分类最多10条
            content = tweet.get("content", "")
            author = tweet.get("author", "")
            url = tweet.get("url", "")
            cat_items.append(f"- **{author}**: {content}\n  链接: {url}")
        sections.append(f"## {cat}\n" + "\n".join(cat_items))

    return "\n\n".join(sections)


def get_api_key() -> str:
    """获取 API Key"""
    api_key = os.environ.get("ANTHROPIC_AUTH_TOKEN") or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("请设置 ANTHROPIC_AUTH_TOKEN 或 ANTHROPIC_API_KEY 环境变量")
    return api_key


def generate_digest_with_claude(content: str, config: dict, today: str) -> str:
    """使用 Claude 生成简报"""
    api_key = get_api_key()

    base_url = os.environ.get("ANTHROPIC_BASE_URL")
    if base_url:
        client = anthropic.Anthropic(api_key=api_key, base_url=base_url)
    else:
        client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""你是一位资深的 AI 领域内容编辑，需要根据以下原始推文内容生成一份精炼的中文 AI 博主精选简报。

今天日期: {today}

原始内容:
{content}

## 生成要求:

### 1. 内容筛选标准
优先选择符合以下特征的内容:
- **实用价值**: 提供具体的工具、技巧、工作流
- **观点独到**: 有深度的思考和分析
- **时效性强**: 最新的 AI 工具和趋势
- **传播性强**: 具有话题性和讨论价值

### 2. 板块结构（严格按以下顺序）

**🤖 今日摘要**
- 用 100 字概括当日核心主题和热点

**🛠️ AI工具精选（3-5条）**
- Claude Code、Cursor、Copilot 等工具的新功能和技巧
- 每条包含: [标题/描述] + **核心价值** + **适用场景**
- 控制在 100 字内

**⚙️ AI工作流（3-5条）**
- 自动化工作流的设计思路和实现
- MCP、Agent、Skills 等框架的应用
- 每条包含: 描述 + **实现方式** + **效果**
- 控制在 100 字内

**✍️ 提示词工程（2-3条）**
- 高质量 Prompt 设计技巧
- 结构化提示词方法论
- 每条包含: 技巧/方法 + **应用场景**
- 控制在 100 字内

**💻 AI编程实践（3-5条）**
- 代码生成、重构、调试的 AI 辅助
- 编程工具对比和选择
- 每条包含: 实践内容 + **工具** + **效果**
- 控制在 100 字内

**📝 内容创作（2-3条）**
- AI 辅助内容创作的方法和工具
- 提升创作效率的技巧
- 每条包含: 方法 + **工具** + **效果**
- 控制在 100 字内

**🧠 AI思考与判断力（2-3条）**
- 对 AI 时代的深度思考
- 判断力比技能更重要的观点
- 每条包含: 观点 + **分析**
- 控制在 100 字内

**🎯 博主推荐**
列出 5-10 位最值得关注的博主及其专注领域

### 3. 风险提示（必须包含）
```
⚠️ **内容提示**: 本简报内容来自 X 平台博主，仅供参考。使用 AI 工具时请根据实际情况判断。
```

### 4. 语言风格
- 专业性与可读性平衡
- 简洁明了，直击要点
- 每条内容控制在 80-100 字
- 使用加粗、列表等方式提升可读性

### 5. 格式要求
- 使用 Markdown 格式
- 导语 100 字以内
- **精选内容保留原推文链接**
- 总长度控制在 2000-3000 字

直接输出简报内容，不需要额外说明。"""

    message = client.messages.create(
        model=config["claude"]["model"],
        max_tokens=config["claude"]["max_tokens"],
        temperature=config.get("claude", {}).get("temperature", 0.3),
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return message.content[0].text


def save_digest(content: str, config: dict, today: str):
    """保存简报文件"""
    digests_dir = PROJECT_ROOT / config["output"]["digests_dir"]
    digests_dir.mkdir(exist_ok=True)

    # 保存日期文件
    date_file = digests_dir / f"{today}.md"
    with open(date_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[完成] 已保存: {date_file}")

    # 更新 latest.md
    latest_file = digests_dir / "latest.md"
    with open(latest_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[完成] 已更新: {latest_file}")


def main():
    """主函数"""
    print("=" * 50)
    print("X AI 博主精选简报生成器")
    print("=" * 50)

    # 加载配置
    config = load_config()

    # 获取北京时间日期
    tz = pytz.timezone("Asia/Shanghai")
    today = datetime.now(tz).strftime(config["output"]["date_format"])
    print(f"\n日期: {today}")

    # 抓取数据
    print("\n[1/3] 正在抓取 X 博主推文...")
    tweets = fetch_tweets_from_bloggers(config)
    print(f"      获取 {len(tweets)} 条原始推文")

    # 过滤数据
    print("\n[2/3] 正在过滤和分类...")
    filtered = filter_tweets(tweets, config)
    print(f"      筛选后 {len(filtered)} 条推文")

    # 检查是否有内容
    if not filtered:
        print("\n[错误] 没有符合条件的推文，退出")
        sys.exit(1)

    # 准备内容
    raw_content = prepare_content_for_claude(filtered)

    # 生成简报
    print("\n[2/3] 正在使用 AI 生成简报...")
    digest = generate_digest_with_claude(raw_content, config, today)

    # 保存
    print("\n[3/3] 正在保存简报...")
    save_digest(digest, config, today)

    print("\n" + "=" * 50)
    print("生成完成!")
    print("=" * 50)


if __name__ == "__main__":
    main()
