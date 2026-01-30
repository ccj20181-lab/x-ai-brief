#!/usr/bin/env python3
"""
本地测试运行脚本
配置了所有必要的凭证，可以直接运行
"""

import os
import sys
from pathlib import Path

# 添加 scripts 目录到 Python 路径
scripts_dir = Path(__file__).parent / 'scripts'
sys.path.insert(0, str(scripts_dir))

# 配置环境变量
os.environ['ANTHROPIC_AUTH_TOKEN'] = 'ede5dcfb6ee24bc1abb5e6a14887d6c7.wPIlUa0hkFFD9mbM'
os.environ['ANTHROPIC_BASE_URL'] = 'https://open.bigmodel.cn/api/anthropic'
os.environ['BIRD_AUTH_TOKEN'] = '48a507f0d909e68596a41eeff6f8308502f7da83'
os.environ['BIRD_CT0'] = '53f1990b6fccdbf610c115aee1870acc4e0d694fc5a434f91019aabc9dbd79131d4aee86cb73d70d629a77c208b44b7ae55899d9ef2f426c18879c3013d2beb3f9dd439a539f8453984cc027590a9127'
os.environ['PUSHPLUS_TOKEN'] = 'a6443f3a5d0f4b11a42c281f831b5c15'

print("=" * 50)
print("X AI 博主精选简报 - 本地测试运行")
print("=" * 50)
print()
print("已配置环境变量：")
print("  ✓ ANTHROPIC_AUTH_TOKEN (智谱 AI)")
print("  ✓ BIRD_AUTH_TOKEN (X.com Auth)")
print("  ✓ BIRD_CT0 (X.com CT0)")
print("  ✓ PUSHPLUS_TOKEN (微信推送)")
print()
print("=" * 50)
print()

try:
    # 导入并运行主脚本
    from x_ai_digest import main as digest_main

    print("[开始运行] 生成简报...")
    print()
    digest_main()

    print()
    print("=" * 50)
    print("简报生成完成！")
    print("=" * 50)
    print()
    print("是否推送到微信？(需要输入 yes 确认)")

except Exception as e:
    print(f"\n[错误] 执行出错: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
