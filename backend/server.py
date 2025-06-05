from flask import Flask, request, jsonify, send_from_directory
import os
import requests
from dotenv import load_dotenv
import logging
import socket

# 配置日志
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

app = Flask(__name__, static_folder='../frontend', static_url_path='')

# 获取OpenRouter API密钥
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
if not OPENROUTER_API_KEY:
    logger.warning("未设置OpenRouter API密钥，请在.env文件中设置OPENROUTER_API_KEY")

# 定义AI模型
AI_MODEL = "deepseek/deepseek-r1-0528:free"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

@app.route('/')
def index():
    """提供前端主页"""
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    """提供静态文件"""
    return send_from_directory('../frontend', path)

@app.route('/chat', methods=['POST'])
def chat():
    """处理聊天请求并调用AI API"""
    if not OPENROUTER_API_KEY:
        return jsonify({'error': 'OpenRouter API密钥未配置'}), 500

    try:
        user_message = request.json.get('message')
        if not user_message:
            return jsonify({'error': '未提供消息内容'}), 400

        ai_response = generate_ai_response(user_message)
        return jsonify({'response': ai_response})
    except Exception as e:
        logger.error(f"生成AI回复时出错: {e}")
        return jsonify({'error': '获取AI回复失败'}), 500

def generate_ai_response(user_message):
    """调用AI模型生成回复"""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    # 构建提示词以引导AI提供基于现代生活佛学的回复
    prompt_messages = [
        {"role": "system", "content": """你是生活智言，一位精通现代生活佛学、正念修行和佛教智慧的现代禅师。你深谙如何将佛学智慧应用于现代日常生活中。

回答要求：
1. 以温和、慈悲且实用的语言回答问题，每次回复不超过300字
2. 回答应基于现代生活佛学理念：正念(mindfulness)、慈悲心、内观、中道、无常观等概念
3. 重点关注日常生活应用：如何在工作、学习、人际关系、情绪管理中实践佛学智慧
4. 适当引用佛教经典智慧，但以现代人能理解的方式表达，避免过于深奥的佛学术语
5. 提供具体可行的修行建议和生活指导，而非空泛的哲学论述
6. 语言风格平和、温暖、易懂，既有佛学深度又贴近现代生活
7. 融入现代心理学和科学理解，展现佛学与现代生活的融合
8. 不管问题多么世俗或现实，都能以佛学智慧给予慈悲智慧的回应

核心理念：
- 正念觉察：活在当下，觉察内心和周围环境
- 慈悲智慧：以慈悲心对待自己和他人
- 中道平衡：在极端之间寻找智慧的平衡点
- 因缘观：理解万物相互依存的本质
- 无常观：接受变化是生活的自然规律
- 内心平静：通过修行培养内在的宁静与智慧

记住：你不是教条主义者，而是一位温暖的生活导师，用佛学智慧帮助现代人在日常生活中找到内心平静、智慧和慈悲。"""},
        {"role": "user", "content": user_message}
    ]

    data = {
        "model": AI_MODEL,
        "messages": prompt_messages,
        "temperature": 0.7,  # 控制回复的创造性和多样性
        "max_tokens": 800    # 控制回复长度
    }

    logger.info(f"发送请求到OpenRouter API: {AI_MODEL}")
    response = requests.post(OPENROUTER_API_URL, headers=headers, json=data)
    response.raise_for_status()  # 对错误响应(4xx或5xx)抛出异常

    result = response.json()
    logger.info("成功接收到API响应")
    
    # 提取AI消息
    if result and 'choices' in result and result['choices']:
        return result['choices'][0]['message']['content']
    else:
        logger.error(f"API返回异常格式: {result}")
        return "未能获得AI的回复，请稍后再试。"

if __name__ == '__main__':
    default_port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    debug_mode = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    # 尝试不同的端口，如果默认端口被占用
    ports_to_try = [default_port, 5050, 8080, 8000, 3000]
    
    for port in ports_to_try:
        try:
            logger.info(f"尝试在端口 {port} 启动服务器: host={host}, debug={debug_mode}")
            
            # 使用socket测试端口是否可用
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((host if host != '0.0.0.0' else '127.0.0.1', port))
            sock.close()
            
            if result != 0:  # 端口可用
                app.run(host=host, port=port, debug=debug_mode)
                break
            else:
                logger.warning(f"端口 {port} 已被占用，尝试下一个端口...")
        except Exception as e:
            logger.error(f"启动服务器时出错: {e}")
            # 继续尝试下一个端口
            continue
    else:  # 这个else属于for循环，当循环正常结束（没有被break打断）时执行
        logger.error("所有端口都被占用，无法启动服务器")
        print("错误: 所有端口都被占用，无法启动服务器。请手动指定一个可用端口。") 