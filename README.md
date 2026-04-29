<div align="center">

# 🤖 Ayyat — AI Voice Assistant

### *Your Jarvis-style bilingual AI companion for Windows*

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Llama](https://img.shields.io/badge/Llama_3.3-7C3AED?style=for-the-badge&logo=meta&logoColor=white)](https://groq.com/)
[![Groq](https://img.shields.io/badge/Groq-F55036?style=for-the-badge&logo=groq&logoColor=white)](https://groq.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

[![Made with ❤️](https://img.shields.io/badge/Made_with-❤️-red?style=flat-square)](https://github.com)
[![Bilingual](https://img.shields.io/badge/Languages-EN_|_UR_|_HI-blue?style=flat-square)]()
[![Voice First](https://img.shields.io/badge/Voice-First-purple?style=flat-square)]()
[![Free](https://img.shields.io/badge/100%25-Free-brightgreen?style=flat-square)]()

---

**Ayyat** is a futuristic AI voice assistant that talks, thinks, and takes action — just like Jarvis from Iron Man. Speak naturally in English, Urdu, or Hindi, and Ayyat will open apps, search the web, send WhatsApp messages, control your system, and more.

[**🚀 Quick Start**](#-quick-start) • [**✨ Features**](#-features) • [**📸 Demo**](#-demo) • [**🛠️ Tech Stack**](#%EF%B8%8F-tech-stack) • [**📖 Setup**](#-installation--setup)

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🎙️ **Voice First**
- Continuous listening mode
- Browser-based speech recognition
- Natural conversation flow
- Hands-free operation

</td>
<td width="50%">

### 🌍 **Multilingual**
- English (Indian accent)
- Urdu (Pakistani female voice)
- Hindi (native pronunciation)
- Auto language detection

</td>
</tr>
<tr>
<td width="50%">

### 🧠 **Smart Brain**
- Llama 3.3 70B via Groq
- Context-aware conversations
- Memory across turns
- Lightning-fast responses (<1s)

</td>
<td width="50%">

### ⚡ **Real Actions**
- Open any Windows application
- Web search with summaries
- Send WhatsApp messages
- Play music/videos on YouTube
- System control (volume, brightness, lock)

</td>
</tr>
<tr>
<td width="50%">

### 🎨 **Modern UI**
- Animated AI orb visualizer
- Glassmorphism design
- Real-time status indicators
- Mobile responsive
- Dark theme with neon accents

</td>
<td width="50%">

### 🔧 **Powerful Backend**
- FastAPI + WebSocket
- 14 built-in tools
- Edge TTS (neural voices)
- Modular architecture
- Easy to extend

</td>
</tr>
</table>

</div>

---

## 🎯 What Can Ayyat Do?

```
👤 You: "Open Chrome and play Atif Aslam songs"
🤖 Ayyat: ✓ Chrome opened ✓ YouTube playing Atif Aslam

👤 You: "السلام علیکم"
🤖 Ayyat: "وعلیکم السلام! میں آپ کی کیا مدد کر سکتی ہوں؟"

👤 You: "What's the latest news on AI?"
🤖 Ayyat: [Searches web and provides a summary]

👤 You: "Volume up"
🤖 Ayyat: ✓ Volume increased

👤 You: "Send Ali a WhatsApp saying I'll be late"
🤖 Ayyat: ✓ Message sent on WhatsApp
```

---

## 🛠️ Tech Stack

<div align="center">

### Backend
![Python](https://img.shields.io/badge/Python_3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![WebSocket](https://img.shields.io/badge/WebSocket-010101?style=flat-square&logo=socketdotio&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-499848?style=flat-square&logo=gunicorn&logoColor=white)

### AI & Voice
![Groq](https://img.shields.io/badge/Groq_API-F55036?style=flat-square&logo=groq&logoColor=white)
![Llama](https://img.shields.io/badge/Llama_3.3_70B-7C3AED?style=flat-square&logo=meta&logoColor=white)
![Edge TTS](https://img.shields.io/badge/Edge_TTS-0078D4?style=flat-square&logo=microsoftedge&logoColor=white)
![Speech Recognition](https://img.shields.io/badge/Speech_Recognition-FF6F00?style=flat-square)

### Frontend
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)
![Canvas API](https://img.shields.io/badge/Canvas_API-FF6B6B?style=flat-square)

### Tools & Automation
![PyAutoGUI](https://img.shields.io/badge/PyAutoGUI-3776AB?style=flat-square&logo=python&logoColor=white)
![PyWhatKit](https://img.shields.io/badge/PyWhatKit-25D366?style=flat-square&logo=whatsapp&logoColor=white)
![pygame](https://img.shields.io/badge/pygame-2C3E50?style=flat-square)

</div>

---

## 🚀 Quick Start

### Prerequisites

- 🐍 **Python 3.11+** ([Download](https://python.org))
- 🪟 **Windows 10/11** (for system control features)
- 🌐 **Internet connection** (for AI & web tools)
- 🔑 **Groq API key** (free at [console.groq.com](https://console.groq.com))

### One-Line Install (after Python setup)

```bash
git clone https://github.com/YourUsername/Ayyat_AI_Assistant.git
cd Ayyat_AI_Assistant
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## 📖 Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/YourUsername/Ayyat_AI_Assistant.git
cd Ayyat_AI_Assistant
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

> 💡 If `PyAudio` fails:
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

### 4️⃣ Get Your Free Groq API Key

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up with Google
3. Navigate to **API Keys** → **Create API Key**
4. Copy the key (starts with `gsk_...`)

### 5️⃣ Setup Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=gsk_your_actual_key_here
```

⚠️ **Never commit `.env` to GitHub** (it's in `.gitignore`)

### 6️⃣ Run the Server

```bash
cd backend
python main.py
```

### 7️⃣ Open in Browser

Visit: **http://127.0.0.1:8000**

🎉 **You're ready! Start talking to Ayyat.**

---

## 📁 Project Structure

```
Ayyat_AI_Assistant/
│
├── 📂 backend/
│   ├── 📂 core/                    # Voice & LLM modules
│   │   ├── stt.py                  # Speech-to-text
│   │   ├── tts.py                  # Text-to-speech
│   │   ├── wake_word.py            # Wake word detection
│   │   └── llm.py                  # Groq LLM integration
│   │
│   ├── 📂 tools/                   # Action tools (14 capabilities)
│   │   ├── apps.py                 # Application launcher
│   │   ├── web_search.py           # Web search
│   │   ├── whatsapp.py             # WhatsApp messaging
│   │   ├── media.py                # YouTube playback
│   │   ├── system.py               # Volume, brightness, lock
│   │   └── registry.py             # Tool registry
│   │
│   ├── main.py                     # FastAPI server
│   ├── assistant.py                # Voice loop orchestrator
│   ├── config.py                   # Settings & API keys
│   └── responses.py                # Bilingual greetings
│
├── 📂 frontend/
│   ├── 📂 css/
│   │   └── style.css               # Modern UI styling
│   ├── 📂 js/
│   │   ├── app.js                  # Main controller
│   │   ├── orb.js                  # Animated orb
│   │   └── websocket.js            # Real-time connection
│   └── index.html                  # Jarvis HUD
│
├── .env                            # API keys (not in git)
├── .gitignore
├── requirements.txt
├── run.bat                         # Windows launcher
└── README.md
```

---

## 🎮 Usage

### Voice Mode (Continuous Listening)

1. Click the **🎤 microphone button** to activate
2. The button turns **green** (continuous mode ON)
3. Speak naturally — Ayyat listens, responds, and listens again
4. Click again to stop

### Text Mode

1. Type your message in the input bar
2. Press **Enter** or click **Send**
3. Ayyat responds in voice + text

### Quick Actions

Click any action card for instant commands:
- ⏱ Time
- 📝 Notepad
- 😄 Joke
- 🔊 Volume
- 💡 Help

### Example Commands

<details>
<summary><b>📂 App Control</b></summary>

```
"Open Chrome"
"Launch VS Code"
"Open notepad"
"Start calculator"
"Open Spotify"
```

</details>

<details>
<summary><b>🎵 Media Playback</b></summary>

```
"Play Atif Aslam songs"
"Play tum hi ho"
"YouTube pe coding tutorial laga do"
```

</details>

<details>
<summary><b>🌐 Web Search</b></summary>

```
"What is quantum computing?"
"Search latest AI news"
"Imran Khan kaun hai?"
```

</details>

<details>
<summary><b>⚙️ System Control</b></summary>

```
"Volume up"
"Brightness 80"
"Mute"
"Lock screen"
"Shutdown in 60 seconds"
```

</details>

<details>
<summary><b>💬 WhatsApp</b></summary>

```
"WhatsApp Ali — meeting at 5"
"Send a message to +923001234567"
```

</details>

<details>
<summary><b>🇵🇰 Urdu</b></summary>

```
"السلام علیکم"
"آپ کا نام کیا ہے"
"وقت کیا ہوا ہے"
```

</details>

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Frontend (Browser)                │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │
│  │ Orb HUD  │  │ Mic/STT  │  │ WebSocket Client │  │
│  └──────────┘  └──────────┘  └──────────────────┘  │
└──────────────────────┬──────────────────────────────┘
                       │ WebSocket (ws://)
                       │ HTTP API
┌──────────────────────▼──────────────────────────────┐
│                FastAPI Server (Python)               │
│  ┌──────────────────────────────────────────────┐   │
│  │           Assistant Orchestrator              │   │
│  └─────┬────────────────┬──────────────┬───────┘   │
│        │                │              │            │
│   ┌────▼────┐     ┌────▼────┐    ┌───▼─────────┐  │
│   │  LLM    │     │ Tools   │    │ Edge TTS    │  │
│   │ (Groq)  │     │ (14x)   │    │ (Voice)     │  │
│   └─────────┘     └─────────┘    └─────────────┘  │
└─────────────────────────────────────────────────────┘
```

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/awesome-feature`)
3. Commit your changes (`git commit -m 'Add awesome feature'`)
4. Push to the branch (`git push origin feature/awesome-feature`)
5. Open a Pull Request

### Ideas for Contributions

- 🎯 New tools (calendar, email, etc.)
- 🌍 More language support
- 🎨 Theme variations
- 📱 Mobile app version
- 🤖 Custom wake word with Porcupine
- 🎭 Animated avatar (Live2D/3D)

---

## 🐛 Troubleshooting

<details>
<summary><b>Voice not working?</b></summary>

- Ensure microphone permissions are granted in Chrome
- Use Chrome browser (best speech recognition support)
- Check system volume and browser tab is not muted
</details>

<details>
<summary><b>"GROQ_API_KEY not found"?</b></summary>

- Make sure `.env` file is in the **root** folder (not in `backend/`)
- Format: `GROQ_API_KEY=gsk_your_key_here` (no quotes, no spaces)
</details>

<details>
<summary><b>Server won't start?</b></summary>

- Verify virtual environment is activated: `(venv)` should show in terminal
- Reinstall dependencies: `pip install -r requirements.txt`
- Check port 8000 is not in use
</details>

<details>
<summary><b>Tools not executing?</b></summary>

- Confirm running on Windows (system tools are Windows-specific)
- Check application paths in `backend/config.py`
- Ensure `pyautogui` and `pycaw` are installed
</details>

---

## 🗺️ Roadmap

- [x] ✅ Voice + Text input
- [x] ✅ Bilingual support (EN/UR/HI)
- [x] ✅ 14 action tools
- [x] ✅ Modern web UI
- [x] ✅ Continuous listening mode
- [ ] 🔄 Custom wake word (offline)
- [ ] 🔄 3D avatar integration
- [ ] 🔄 Calendar & email tools
- [ ] 🔄 Mobile app
- [ ] 🔄 Proactive notifications
- [ ] 🔄 Multi-user support

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Credits & Acknowledgments

- **[Groq](https://groq.com/)** — Lightning-fast LLM inference
- **[Meta AI](https://ai.meta.com/)** — Llama 3.3 model
- **[Microsoft](https://www.microsoft.com/)** — Edge TTS neural voices
- **[FastAPI](https://fastapi.tiangolo.com/)** — Modern Python web framework
- **[Anthropic](https://anthropic.com/)** — For inspiration in AI design

---

## 👨‍💻 Author

<div align="center">

**Built with ❤️ by Ayyaz Qamar**

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/YourUsername)
[![LinkedIn](www.linkedin.com/in/ayyaz-qamar-41bb51383)
[![Email](ayyazqamar12@gmail.com)

</div>

---

<div align="center">

### ⭐ Star this repo if you find it helpful!

**Made for those who dream of building their own AI Assistant** 🚀

</div>
