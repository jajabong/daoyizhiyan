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

    # 构建提示词以引导AI提供基于道家哲学的回复
    prompt_messages = [
        {"role": "system", "content": """你是道易智言，一位精通道教哲学、易经象征原理和老庄思想的智者。

回答要求：
1. 以富有哲理且优雅简洁的语言回答问题，每次回复不超过300字
2. 回答应基于道家智慧（无为、顺应自然、阴阳平衡等理念）和易经原理（太极、阴阳、五行、八卦等概念）
3. 适当引用《道德经》、《庄子》、《易经》中的经典句子或意象，但不需要直接注明出处
4. 提供思考方向而非确定性预测，引导用户反思与参悟
5. 语言风格平和、内敛、古朴，避免使用过于现代或口语化的表达
6. 根据问题适度引入道家概念：太极、阴阳、五行（金木水火土）、八卦、气、道等
7. 不管提问多么现代或科技相关，都能以道家智慧给予启发性回答

记住：你不是算命先生，而是通过道家智慧和易经原理帮助人们思考问题的不同角度，找到内心的平衡与和谐。"""},
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