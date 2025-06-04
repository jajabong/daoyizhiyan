#!/usr/bin/env python
# 主应用入口点 - 解决Render部署问题

import os
from backend.server import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port) 