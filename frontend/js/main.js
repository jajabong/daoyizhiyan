// 道易智言 - 主JavaScript文件

document.addEventListener('DOMContentLoaded', () => {
    const messageForm = document.getElementById('messageForm');
    const userInput = document.getElementById('userInput');
    const chatMessages = document.getElementById('chatMessages');
    const submitButton = document.querySelector('#messageForm button');
    
    // 设置后端API URL
    const API_URL = '/chat';
    
    // 添加事件监听器
    messageForm.addEventListener('submit', handleSubmit);
    
    // 添加欢迎消息
    addWelcomeMessage();
    
    // 处理表单提交
    async function handleSubmit(e) {
        e.preventDefault();
        const message = userInput.value.trim();
        
        // 检查消息是否为空
        if (!message) return;
        
        // 禁用输入框和按钮
        setInputState(false);
        
        // 添加用户消息到聊天窗口
        addMessage(message, 'user');
        
        // 清空输入框
        userInput.value = '';
        
        // 显示加载指示器
        const loadingMessage = addLoadingMessage();
        
        try {
            // 调用API获取AI回复
            const response = await fetchAIResponse(message);
            
            // 移除加载指示器
            loadingMessage.remove();
            
            // 添加AI回复到聊天窗口
            addMessage(response, 'ai');
        } catch (error) {
            // 移除加载指示器
            loadingMessage.remove();
            
            // 添加错误消息
            addErrorMessage(error.message);
            console.error('获取AI回复时出错:', error);
        } finally {
            // 重新启用输入框和按钮
            setInputState(true);
            
            // 聚焦到输入框
            userInput.focus();
        }
        
        // 滚动到最新消息
        scrollToBottom();
    }
    
    // 设置输入状态（启用/禁用）
    function setInputState(enabled) {
        userInput.disabled = !enabled;
        submitButton.disabled = !enabled;
        
        if (!enabled) {
            submitButton.classList.add('disabled');
        } else {
            submitButton.classList.remove('disabled');
        }
    }
    
    // 获取AI回复
    async function fetchAIResponse(message) {
        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message })
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || '服务器错误');
            }
            
            const data = await response.json();
            return data.response;
        } catch (error) {
            console.error('API调用出错:', error);
            throw new Error('无法连接到服务器，请稍后再试');
        }
    }
    
    // 添加欢迎消息
    function addWelcomeMessage() {
        const systemDiv = document.createElement('div');
        systemDiv.classList.add('message', 'system');
        
        const welcomeText = document.createElement('p');
        welcomeText.textContent = '欢迎来到道易智言。心中有疑，可问道于此。';
        
        systemDiv.appendChild(welcomeText);
        chatMessages.appendChild(systemDiv);
        
        // 添加道家初始引导消息
        const aiDiv = document.createElement('div');
        aiDiv.classList.add('message', 'ai');
        
        const aiText = document.createElement('p');
        aiText.textContent = '万物皆有象，言象而明道。心有所思，何不道来？';
        
        aiDiv.appendChild(aiText);
        chatMessages.appendChild(aiDiv);
    }
    
    // 添加消息到聊天窗口
    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender);
        
        const messageText = document.createElement('p');
        messageText.textContent = text;
        
        messageDiv.appendChild(messageText);
        chatMessages.appendChild(messageDiv);
        
        // 滚动到最新消息
        scrollToBottom();
        
        return messageDiv;
    }
    
    // 添加加载指示器
    function addLoadingMessage() {
        const loadingDiv = document.createElement('div');
        loadingDiv.classList.add('message', 'ai', 'loading');
        
        // 添加一个简单的加载动画
        loadingDiv.innerHTML = '<p>道易智言：思考中<span>.</span><span>.</span><span>.</span></p>';
        loadingDiv.classList.add('loading-dots');

        chatMessages.appendChild(loadingDiv);
        
        // 滚动到最新消息
        scrollToBottom();
        
        return loadingDiv;
    }
    
    // 添加错误消息
    function addErrorMessage(errorText) {
        const errorDiv = document.createElement('div');
        errorDiv.classList.add('message', 'system', 'error');
        
        const errorMessage = document.createElement('p');
        errorMessage.textContent = `错误: ${errorText}`;
        
        errorDiv.appendChild(errorMessage);
        chatMessages.appendChild(errorDiv);
        
        return errorDiv;
    }
    
    // 滚动到最新消息
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // 初始化时聚焦输入框
    userInput.focus();
}); 