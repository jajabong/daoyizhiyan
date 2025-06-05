// Buddhist Wisdom - Main JavaScript Application

document.addEventListener('DOMContentLoaded', () => {
    const messageForm = document.getElementById('messageForm');
    const userInput = document.getElementById('userInput');
    const chatMessages = document.getElementById('chatMessages');
    const submitButton = document.querySelector('#messageForm button');
    
    // Backend API configuration
    const API_URL = '/chat';
    
    // Initialize application
    initializeApp();
    
    // Event listeners
    messageForm.addEventListener('submit', handleSubmit);
    userInput.addEventListener('keypress', handleKeyPress);
    
    // Initialize the application
    function initializeApp() {
        // The welcome message is already in the HTML, so we don't need to add it here
        // Focus on the input field
        userInput.focus();
        
        // Add subtle entrance animation
        setTimeout(() => {
            document.querySelector('.chat-container').style.opacity = '1';
        }, 100);
    }
    
    // Handle enter key press
    function handleKeyPress(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit(e);
        }
    }
    
    // Handle form submission
    async function handleSubmit(e) {
        e.preventDefault();
        const message = userInput.value.trim();
        
        // Validate message
        if (!message) return;
        
        // Disable input during processing
        setInputState(false);
        
        // Add user message to chat
        addMessage(message, 'user');
        
        // Clear input field
        userInput.value = '';
        
        // Show loading indicator with Buddhist aesthetic
        const loadingMessage = addLoadingMessage();
        
        try {
            // Get AI response
            const response = await fetchAIResponse(message);
            
            // Remove loading indicator
            loadingMessage.remove();
            
            // Add AI response to chat
            addMessage(response, 'ai');
            
        } catch (error) {
            // Remove loading indicator
            loadingMessage.remove();
            
            // Add error message
            addErrorMessage(error.message);
            console.error('Error getting AI response:', error);
            
        } finally {
            // Re-enable input
            setInputState(true);
            
            // Focus input field
            userInput.focus();
        }
        
        // Scroll to latest message
        scrollToBottom();
    }
    
    // Set input state (enabled/disabled)
    function setInputState(enabled) {
        userInput.disabled = !enabled;
        submitButton.disabled = !enabled;
        
        if (!enabled) {
            submitButton.classList.add('disabled');
            userInput.style.opacity = '0.6';
        } else {
            submitButton.classList.remove('disabled');
            userInput.style.opacity = '1';
        }
    }
    
    // Fetch AI response from backend
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
                throw new Error(errorData.error || 'Server error occurred');
            }
            
            const data = await response.json();
            return data.response;
            
        } catch (error) {
            console.error('API call error:', error);
            throw new Error('Unable to connect to Buddhist Wisdom. Please try again in a moment.');
        }
    }
    
    // Add message to chat window
    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender);
        
        // Add message decoration for system/AI messages
        if (sender === 'ai') {
            const decoration = document.createElement('div');
            decoration.classList.add('message-decoration');
            decoration.innerHTML = '<div class="lotus-small">🪷</div>';
            messageDiv.appendChild(decoration);
        }
        
        // Create message content container
        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');
        
        const messageText = document.createElement('p');
        messageText.textContent = text;
        
        messageContent.appendChild(messageText);
        messageDiv.appendChild(messageContent);
        
        // Add entrance animation
        messageDiv.style.opacity = '0';
        messageDiv.style.transform = 'translateY(20px)';
        
        chatMessages.appendChild(messageDiv);
        
        // Trigger animation
        setTimeout(() => {
            messageDiv.style.opacity = '1';
            messageDiv.style.transform = 'translateY(0)';
        }, 50);
        
        // Scroll to latest message
        scrollToBottom();
        
        return messageDiv;
    }
    
    // Add loading indicator with Buddhist aesthetic
    function addLoadingMessage() {
        const loadingDiv = document.createElement('div');
        loadingDiv.classList.add('message', 'ai', 'loading');
        
        // Create decorative loading message
        const decoration = document.createElement('div');
        decoration.classList.add('message-decoration');
        decoration.innerHTML = '<div class="lotus-small">🪷</div>';
        
        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');
        
        const loadingText = document.createElement('p');
        loadingText.innerHTML = 'Reflecting on your question<span class="loading-dots"><span>.</span><span>.</span><span>.</span></span>';
        
        messageContent.appendChild(loadingText);
        loadingDiv.appendChild(decoration);
        loadingDiv.appendChild(messageContent);
        
        chatMessages.appendChild(loadingDiv);
        
        // Scroll to latest message
        scrollToBottom();
        
        return loadingDiv;
    }
    
    // Add error message with compassionate tone
    function addErrorMessage(errorText) {
        const errorDiv = document.createElement('div');
        errorDiv.classList.add('message', 'system', 'error');
        
        const decoration = document.createElement('div');
        decoration.classList.add('message-decoration');
        decoration.innerHTML = '<div class="lotus-small" style="filter: sepia(100%) hue-rotate(320deg);">🪷</div>';
        
        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');
        
        const errorMessage = document.createElement('p');
        errorMessage.textContent = `I apologize, but I encountered an issue: ${errorText}. Please take a mindful breath and try again.`;
        
        messageContent.appendChild(errorMessage);
        errorDiv.appendChild(decoration);
        errorDiv.appendChild(messageContent);
        
        chatMessages.appendChild(errorDiv);
        
        return errorDiv;
    }
    
    // Smooth scroll to bottom
    function scrollToBottom() {
        const scrollTarget = chatMessages.scrollHeight - chatMessages.clientHeight;
        const currentScroll = chatMessages.scrollTop;
        const distance = scrollTarget - currentScroll;
        
        if (Math.abs(distance) < 10) {
            chatMessages.scrollTop = scrollTarget;
            return;
        }
        
        // Smooth scroll animation
        const duration = 300;
        const startTime = performance.now();
        
        function animateScroll(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Easing function for smooth animation
            const easeProgress = 1 - Math.pow(1 - progress, 3);
            
            chatMessages.scrollTop = currentScroll + (distance * easeProgress);
            
            if (progress < 1) {
                requestAnimationFrame(animateScroll);
            }
        }
        
        requestAnimationFrame(animateScroll);
    }
    
    // Add meditation bell sound effect (optional enhancement)
    function playMeditationBell() {
        // This could be enhanced with actual audio in the future
        // For now, we'll use a visual indication
        const bell = document.querySelector('.meditation-bell');
        if (bell) {
            bell.style.transform = 'scale(1.2)';
            setTimeout(() => {
                bell.style.transform = 'scale(1)';
            }, 200);
        }
    }
    
    // Easter egg: Typing "om" or similar mantras triggers special effects
    userInput.addEventListener('input', (e) => {
        const value = e.target.value.toLowerCase();
        const mantras = ['om', 'aum', 'namaste', 'peace', 'metta'];
        
        if (mantras.some(mantra => value.includes(mantra))) {
            document.body.style.filter = 'sepia(10%) hue-rotate(15deg) brightness(1.05)';
            setTimeout(() => {
                document.body.style.filter = '';
            }, 1000);
        }
    });
}); 