#!/usr/bin/env python
"""
道易智言 - Render部署调试脚本
打印Python模块路径和可用模块信息
"""

import os
import sys
import pkgutil
import importlib
import importlib.util
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def print_system_info():
    """打印系统和Python环境信息"""
    logger.info("===== 系统环境信息 =====")
    logger.info(f"Python版本: {sys.version}")
    logger.info(f"当前工作目录: {os.getcwd()}")
    logger.info(f"模块搜索路径: {sys.path}")
    
    # 打印环境变量
    logger.info("===== 关键环境变量 =====")
    for key in ['PORT', 'DEBUG', 'OPENROUTER_API_KEY', 'PYTHONPATH']:
        value = os.environ.get(key)
        if key == 'OPENROUTER_API_KEY' and value:
            # 隐藏API密钥的实际值
            logger.info(f"{key}: {'*' * 10}")
        else:
            logger.info(f"{key}: {value}")

def test_imports():
    """测试关键模块导入"""
    logger.info("===== 测试模块导入 =====")
    
    # 尝试导入关键模块
    modules_to_test = [
        'flask', 'gunicorn', 'requests', 'backend',
        'backend.server', 'render_fix'
    ]
    
    for module_name in modules_to_test:
        try:
            importlib.import_module(module_name)
            logger.info(f"成功导入模块: {module_name}")
        except ImportError as e:
            logger.error(f"无法导入模块 {module_name}: {e}")
    
    # 特殊处理wsgi.py文件
    logger.info("===== 检查wsgi.py文件 =====")
    wsgi_paths = ['wsgi.py', 'backend/wsgi.py']
    for path in wsgi_paths:
        if os.path.exists(path):
            logger.info(f"找到wsgi文件: {path}")
            # 尝试执行wsgi.py
            try:
                sys.path.insert(0, os.path.dirname(os.path.abspath(path)))
                if path == 'wsgi.py':
                    import wsgi
                    logger.info("成功导入根目录wsgi模块")
                elif path == 'backend/wsgi.py':
                    # 动态导入，避免直接导入失败
                    spec = importlib.util.spec_from_file_location("backend.wsgi", path)
                    if spec:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        logger.info("成功执行backend/wsgi.py文件")
            except Exception as e:
                logger.error(f"导入/执行{path}失败: {e}")
        else:
            logger.warning(f"找不到wsgi文件: {path}")

def list_available_modules():
    """列出当前环境中可用的所有模块"""
    logger.info("===== 可用模块列表 =====")
    all_modules = [name for _, name, _ in pkgutil.iter_modules()]
    logger.info(f"可用模块总数: {len(all_modules)}")
    logger.info(f"可用模块: {', '.join(sorted(all_modules))}")
    
    # 检查特定目录中的文件
    logger.info("===== 目录文件 =====")
    for dir_path in ['.', 'backend']:
        if os.path.exists(dir_path):
            files = os.listdir(dir_path)
            logger.info(f"目录 '{dir_path}' 中的文件: {files}")
        else:
            logger.error(f"目录 '{dir_path}' 不存在")

if __name__ == "__main__":
    logger.info("开始诊断Render部署问题...")
    print_system_info()
    list_available_modules()
    test_imports()
    logger.info("诊断完成")
    
    # 尝试导入app并运行
    try:
        from backend.server import app
        logger.info("成功导入app对象，应用可以启动")
    except Exception as e:
        logger.error(f"导入app对象失败: {e}")

    # 退出状态，便于Render查看结果
    sys.exit(0) 