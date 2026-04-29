/* ===================================================
   AYYAT - Main App Controller (Final)
   Backend TTS, tri-lingual support
   =================================================== */

// ===== DOM Elements =====
const statusIndicator = document.getElementById('statusIndicator');
const statusText = document.getElementById('statusText');
const orbLabel = document.getElementById('orbLabel');
const chatContainer = document.getElementById('chatContainer');
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const micBtn = document.getElementById('micBtn');
const clockTime = document.getElementById('clockTime');
const quickBtns = document.querySelectorAll('.quick-btn');

// Audio player for TTS
const audioPlayer = new Audio();


// ===== Language Detection =====
function detectLang(text) {
    if (/[\u0600-\u06FF]/.test(text)) return 'ur';   // Urdu/Arabic script
    if (/[\u0900-\u097F]/.test(text)) return 'hi';   // Hindi/Devanagari script
    return 'en';
}


// ===== Live Clock =====
function updateClock() {
    const now = new Date();
    const h = String(now.getHours()).padStart(2, '0');
    const m = String(now.getMinutes()).padStart(2, '0');
    clockTime.textContent = `${h}:${m}`;
}
updateClock();
setInterval(updateClock, 1000);


// ===== Status Updates =====
function setStatus(state, message) {
    const labels = {
        idle:       'IDLE',
        listening:  'LISTENING',
        thinking:   'THINKING',
        speaking:   'SPEAKING',
        error:      'ERROR',
        connecting: 'CONNECTING',
    };

    statusIndicator.className = 'status-indicator';
    if (['idle', 'listening', 'thinking', 'speaking', 'error'].includes(state)) {
        statusIndicator.classList.add(state);
    }

    statusText.textContent = message || labels[state] || state.toUpperCase();
    orbLabel.textContent = labels[state] || state.toUpperCase();

    if (window.orb && ['idle', 'listening', 'thinking', 'speaking', 'error'].includes(state)) {
        window.orb.setState(state);
    }
}


// ===== Chat Messages =====
function addMessage(text, sender = 'ayyat', lang = null) {
    const detectedLang = lang || detectLang(text);

    const msg = document.createElement('div');
    msg.className = `chat-message ${sender}`;

    const label = document.createElement('div');
    label.className = 'msg-label';
    label.textContent = sender === 'user' ? 'YOU' : 'AYYAT';

    const content = document.createElement('div');
    content.className = 'msg-text';
    content.textContent = text;

    // Urdu = RTL, Hindi & English = LTR
    if (detectedLang === 'ur') {
        content.style.direction = 'rtl';
        content.style.textAlign = 'right';
        content.style.fontSize = '1.1rem';
    }

    msg.appendChild(label);
    msg.appendChild(content);
    chatContainer.appendChild(msg);

    chatContainer.scrollTop = chatContainer.scrollHeight;
    return msg;
}


// ===== Send Message =====
function sendMessage(text) {
    text = text.trim();
    if (!text) return;

    const userLang = detectLang(text);
    addMessage(text, 'user', userLang);

    setStatus('thinking');
    chatInput.value = '';
    chatInput.disabled = true;
    sendBtn.disabled = true;

    if (window.ayyatWS && window.ayyatWS.connected) {
        window.ayyatWS.sendChat(text);
    } else {
        sendViaHTTP(text);
    }
}

async function sendViaHTTP(text) {
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text }),
        });
        const data = await response.json();
        if (data.reply) {
            const lang = data.lang || detectLang(data.reply);
            addMessage(data.reply, 'ayyat', lang);
            await speakViaBackend(data.reply, lang);
        }
    } catch (e) {
        addMessage('Connection error. Please check the server.', 'ayyat');
        setStatus('error');
    } finally {
        setStatus('idle');
        chatInput.disabled = false;
        sendBtn.disabled = false;
        chatInput.focus();
    }
}


// ===== Backend TTS =====
async function speakViaBackend(text, lang = null) {
    if (!text) return;

    const detectedLang = lang || detectLang(text);
    setStatus('speaking');

    try {
        audioPlayer.pause();
        audioPlayer.currentTime = 0;

        const response = await fetch('/api/tts', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text, lang: detectedLang }),
        });

        if (!response.ok) {
            throw new Error(`TTS failed: ${response.status}`);
        }

        const blob = await response.blob();
        const audioUrl = URL.createObjectURL(blob);
        audioPlayer.src = audioUrl;

        return new Promise((resolve) => {
            audioPlayer.onended = () => {
                URL.revokeObjectURL(audioUrl);
                setStatus('idle');
                chatInput.disabled = false;
                sendBtn.disabled = false;
                chatInput.focus();
                resolve();
            };

            audioPlayer.onerror = () => {
                URL.revokeObjectURL(audioUrl);
                setStatus('idle');
                chatInput.disabled = false;
                sendBtn.disabled = false;
                resolve();
            };

            audioPlayer.play().catch(err => {
                console.error('[TTS] Play failed:', err);
                setStatus('idle');
                chatInput.disabled = false;
                sendBtn.disabled = false;
                resolve();
            });
        });
    } catch (e) {
        console.error('[TTS] Error:', e);
        setStatus('idle');
        chatInput.disabled = false;
        sendBtn.disabled = false;
    }
}


// ===== Mic Input =====
let recognition = null;
let isListening = false;

function setupMic() {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) {
        micBtn.style.opacity = '0.4';
        micBtn.title = 'Speech recognition not supported. Use Chrome.';
        return;
    }

    recognition = new SR();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-IN';

    recognition.onstart = () => {
        isListening = true;
        micBtn.classList.add('active');
        setStatus('listening');
    };

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        sendMessage(transcript);
    };

    recognition.onerror = (event) => {
        if (event.error === 'not-allowed') {
            addMessage('Microphone permission denied. Please allow mic access.', 'ayyat');
            setStatus('error');
        } else {
            setStatus('idle');
        }
        isListening = false;
        micBtn.classList.remove('active');
    };

    recognition.onend = () => {
        isListening = false;
        micBtn.classList.remove('active');
    };
}

function toggleMic() {
    if (!recognition) {
        addMessage('Speech recognition not available. Please use Chrome browser.', 'ayyat');
        return;
    }

    if (isListening) {
        recognition.stop();
    } else {
        try {
            recognition.lang = 'en-IN';
            recognition.start();
        } catch (e) {
            console.error('[Mic] Start error:', e);
        }
    }
}


// ===== Event Listeners =====
sendBtn.addEventListener('click', () => sendMessage(chatInput.value));

chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage(chatInput.value);
    }
});

micBtn.addEventListener('click', toggleMic);

quickBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const cmd = btn.dataset.cmd;
        if (cmd) sendMessage(cmd);
    });
});


// ===== WebSocket Handlers =====
window.ayyatWS.on('connected', () => {
    setStatus('idle', 'CONNECTED');
    setTimeout(() => setStatus('idle'), 1500);
});

window.ayyatWS.on('disconnected', () => {
    setStatus('error', 'DISCONNECTED');
});

window.ayyatWS.on('ayyat', async (data) => {
    const lang = data.lang || detectLang(data.text);
    addMessage(data.text, 'ayyat', lang);
    await speakViaBackend(data.text, lang);
});

window.ayyatWS.on('status', (data) => {
    if (data.state) {
        setStatus(data.state, data.message);
    }
});

window.ayyatWS.on('error', (data) => {
    addMessage(`Error: ${data.message || 'Unknown error'}`, 'ayyat');
    setStatus('error');
    setTimeout(() => setStatus('idle'), 2000);
    chatInput.disabled = false;
    sendBtn.disabled = false;
});


// ===== Initialize =====
document.addEventListener('DOMContentLoaded', () => {
    setStatus('connecting');
    setupMic();
    window.ayyatWS.connect();

    chatInput.focus();

    // Initial welcome - English only, no "bilingual" mention
    setTimeout(() => {
        chatContainer.innerHTML = '';
        const welcomeMsg = "Hello, I'm Ayyat. How can I help you?";
        addMessage(welcomeMsg, 'ayyat', 'en');
        speakViaBackend(welcomeMsg, 'en');
    }, 1500);
});