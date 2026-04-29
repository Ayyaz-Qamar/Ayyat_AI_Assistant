// Step 8 mein bharenge - WebSocket
/* ===================================================
   AYYAT - WebSocket Connection
   Real-time bridge to backend (Llama brain)
   =================================================== */

class AyyatWebSocket {
    constructor() {
        this.ws = null;
        this.connected = false;
        this.reconnectTimer = null;
        this.handlers = {};

        // Auto-construct WebSocket URL based on current page
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        this.url = `${protocol}//${window.location.host}/ws`;
    }

    connect() {
        try {
            this.ws = new WebSocket(this.url);

            this.ws.onopen = () => {
                this.connected = true;
                console.log('[WS] Connected');
                this._emit('connected');
                if (this.reconnectTimer) {
                    clearTimeout(this.reconnectTimer);
                    this.reconnectTimer = null;
                }
            };

            this.ws.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    console.log('[WS] Received:', data);
                    this._emit('message', data);
                    // Also emit by type
                    if (data.type) {
                        this._emit(data.type, data);
                    }
                } catch (e) {
                    console.error('[WS] Parse error:', e);
                }
            };

            this.ws.onclose = () => {
                this.connected = false;
                console.log('[WS] Disconnected');
                this._emit('disconnected');
                this._scheduleReconnect();
            };

            this.ws.onerror = (error) => {
                console.error('[WS] Error:', error);
                this._emit('error', error);
            };

        } catch (e) {
            console.error('[WS] Connection failed:', e);
            this._scheduleReconnect();
        }
    }

    _scheduleReconnect() {
        if (this.reconnectTimer) return;
        this.reconnectTimer = setTimeout(() => {
            console.log('[WS] Reconnecting...');
            this.connect();
        }, 3000);
    }

    send(data) {
        if (!this.connected || !this.ws) {
            console.warn('[WS] Not connected, message dropped');
            return false;
        }
        try {
            this.ws.send(JSON.stringify(data));
            return true;
        } catch (e) {
            console.error('[WS] Send error:', e);
            return false;
        }
    }

    sendChat(text) {
        return this.send({ type: 'chat', text: text });
    }

    sendReset() {
        return this.send({ type: 'reset' });
    }

    on(event, handler) {
        if (!this.handlers[event]) {
            this.handlers[event] = [];
        }
        this.handlers[event].push(handler);
    }

    _emit(event, data) {
        if (this.handlers[event]) {
            this.handlers[event].forEach(h => h(data));
        }
    }
}

// Global instance
const ayyatWS = new AyyatWebSocket();
window.ayyatWS = ayyatWS;