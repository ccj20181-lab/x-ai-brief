#!/usr/bin/env python3
"""
推送到微信测试脚本
"""

import os
import sys
from pathlib import Path

# 配置环境变量
os.environ['PUSHPLUS_TOKEN'] = 'a6443f3a5d0f4b11a42c281f831b5c15'

# 添加 scripts 目录到 Python 路径
scripts_dir = Path(__file__).parent / 'scripts'
sys.path.insert(0, str(scripts_dir))

try:
    from send_pushplus import main as push_main
    push_main()
except Exception as e:
    print(f"[错误] {e}")
    sys.exit(1)
