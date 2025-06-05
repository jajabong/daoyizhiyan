# Buddhist Wisdom - AI Guide for Mindful Living

An AI-powered Buddhist wisdom platform that brings ancient teachings into modern life through compassionate conversations and practical guidance.

## 🕉️ About Buddhist Wisdom

Buddhist Wisdom is an intelligent conversation platform designed to help modern practitioners integrate Buddhist teachings into their daily lives. Our AI guide combines traditional dharma wisdom with contemporary understanding to offer practical, compassionate guidance for life's challenges.

### ✨ Core Features

- **Mindful Conversations**: Engage in meaningful dialogue about Buddhist principles and their real-world applications
- **Practical Guidance**: Receive actionable advice for meditation, stress management, relationships, and personal growth
- **Sacred Design**: Beautiful, Buddhist-inspired interface with traditional elements and modern aesthetics
- **Compassionate Responses**: AI trained on Buddhist principles of loving-kindness, wisdom, and non-judgment
- **Modern Application**: Bridge ancient wisdom with contemporary psychology and lifestyle needs

## 🪷 Buddhist Principles We Embrace

### Core Teachings
- **Mindfulness (Sati)**: Cultivating present-moment awareness in all activities
- **Loving-kindness (Metta)**: Developing compassion for yourself and all beings
- **Middle Way**: Finding balance between extremes in all aspects of life
- **Impermanence (Anicca)**: Understanding the temporary nature of all experiences
- **Interdependence**: Recognizing our deep connection to all life
- **Non-attachment**: Learning to let go of clinging to outcomes
- **Inner Peace**: Developing equanimity through consistent practice

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- OpenRouter API key for AI functionality

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/jajabong/daoyizhiyan.git
   cd daoyizhiyan
   ```

2. **Set up Python virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the `backend` directory:
   ```env
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   DEBUG=False
   HOST=0.0.0.0
   PORT=5000
   ```

5. **Start the application**
   ```bash
   cd backend
   python server.py
   ```

   The application will automatically find an available port (5000, 5050, 8080, etc.).

## 🎨 Design Philosophy

Our design incorporates traditional Buddhist aesthetics:

- **Sacred Geometry**: Mandala patterns and lotus designs throughout the interface
- **Buddhist Color Palette**: Saffron robes, sacred gold, meditation purple, and earth tones
- **Animated Elements**: Floating lotus petals, rotating dharma wheels, and breathing zen circles
- **Typography**: Balanced serif and sans-serif fonts reflecting both tradition and modernity
- **Interactive Elements**: Prayer flags, meditation bells, and sacred symbols

## 🛠️ Technical Architecture

- **Frontend**: HTML5, CSS3 with advanced animations, vanilla JavaScript
- **Backend**: Flask (Python) with RESTful API design
- **AI Integration**: OpenRouter API for conversational intelligence
- **Deployment**: Render-ready with comprehensive configuration
- **Responsive**: Mobile-first design with Buddhist aesthetic elements

## 🌸 Usage Examples

### Daily Meditation Guidance
"How can I establish a consistent meditation practice?"

### Stress Management
"I'm feeling overwhelmed at work. How can Buddhist principles help?"

### Relationship Wisdom
"How do I handle difficult people with compassion?"

### Emotional Balance
"I'm struggling with anger. What would Buddhist teachings suggest?"

## 🔧 Development

### Project Structure
```
buddhist-wisdom/
├── backend/
│   ├── server.py          # Flask application
│   └── .env               # Environment variables
├── frontend/
│   ├── index.html         # Main application page
│   ├── css/styles.css     # Buddhist-inspired styles
│   └── js/main.js         # Client-side logic
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

### Contributing

We welcome contributions that align with Buddhist values of compassion, wisdom, and helpfulness:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/mindful-enhancement`
3. Commit changes: `git commit -m "Add compassionate feature"`
4. Push to branch: `git push origin feature/mindful-enhancement`
5. Open a Pull Request

## 🚀 Deployment

### Render Deployment

1. Connect your GitHub repository to Render
2. Configure the following settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `cd backend && gunicorn server:app`
   - **Environment Variables**: Add your `OPENROUTER_API_KEY`

3. Deploy and share Buddhist wisdom with the world!

## 📜 License

This project is open source and available under the MIT License. May it benefit all beings.

## 🙏 Acknowledgments

- Inspired by the compassionate teachings of the Buddha
- Built with gratitude for the open-source community
- Dedicated to all beings seeking peace and wisdom

---

*"Peace comes from within. Do not seek it without."* — Buddha

**Gate Gate Pāragate Pārasaṃgate Bodhi Svāhā** 🕉️

© 2024 Buddhist Wisdom - Illuminating the Path to Enlightenment
