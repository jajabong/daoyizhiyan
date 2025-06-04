# 导入server.py中的app对象作为应用程序入口点
import sys
import os

# 确保backend目录在路径中
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 使用绝对导入
from backend.server import app

if __name__ == "__main__":
    app.run()
