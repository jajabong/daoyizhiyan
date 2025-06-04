#!/usr/bin/env python
"""
道易智言 - Render部署修复入口点
这个文件为Render部署创建一个单一明确的入口点
"""

import os
import sys

# 确保当前目录在路径中
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 直接导入app对象
from backend.server import app as application

# 为gunicorn提供明确的app变量
app = application

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port) 