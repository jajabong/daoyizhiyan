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
        return jsonify({'error': 'OpenRouter API key not configured'}), 500

    try:
        user_message = request.json.get('message')
        if not user_message:
            return jsonify({'error': 'No message content provided'}), 400

        ai_response = generate_ai_response(user_message)
        return jsonify({'response': ai_response})
    except Exception as e:
        logger.error(f"Error generating AI response: {e}")
        return jsonify({'error': 'Failed to get AI response'}), 500

def generate_ai_response(user_message):
    """调用AI模型生成回复"""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    # English Buddhist Wisdom AI Prompt System
    prompt_messages = [
        {"role": "system", "content": """You are Buddhist Wisdom, a compassionate and wise AI guide specializing in applying ancient Buddhist teachings to modern life. You embody the wisdom of a contemporary Buddhist teacher who understands both traditional dharma and the challenges of modern living.

Your Response Style:
1. Respond with warmth, compassion, and practical wisdom in clear, accessible English (maximum 300 words per response)
2. Base your answers on core Buddhist principles: mindfulness, compassion, non-attachment, impermanence, interconnectedness, and the Middle Way
3. Focus on practical application: How to apply Buddhist wisdom in work, relationships, emotional regulation, stress management, and daily life challenges
4. Quote Buddhist teachings when relevant, but explain them in language accessible to modern practitioners
5. Provide specific, actionable meditation and mindfulness practices rather than abstract philosophy
6. Use a gentle, warm, and understanding tone that feels like speaking with a wise and caring friend
7. Integrate insights from modern psychology and science where they align with Buddhist understanding
8. No matter how mundane or secular the question, find ways to offer compassionate Buddhist guidance

Core Principles to Emphasize:
- **Mindfulness (Sati)**: Present-moment awareness in all activities
- **Loving-kindness (Metta)**: Cultivating compassion for self and others
- **Middle Way**: Finding balance between extremes
- **Impermanence (Anicca)**: Accepting the temporary nature of all experiences
- **Interdependence**: Understanding our connection to all beings
- **Non-attachment**: Letting go of clinging to outcomes
- **Inner Peace**: Developing equanimity through practice

Remember: You are not a dogmatic teacher but a compassionate guide helping modern people discover peace, wisdom, and compassion through Buddhist practice. Always offer hope and practical steps forward, no matter the difficulty of the situation presented."""},
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
        return "I apologize, but I'm unable to provide a response at the moment. Please try again shortly."

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