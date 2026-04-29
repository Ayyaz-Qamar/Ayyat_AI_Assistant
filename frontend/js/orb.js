// Step 8 mein bharenge - Animated orb
/* ===================================================
   AYYAT - Animated Orb (Canvas)
   States: idle, listening, thinking, speaking, error
   =================================================== */

class AyyatOrb {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.state = 'idle';
        this.time = 0;
        this.intensity = 0.5;
        this.targetIntensity = 0.5;
        this.particles = [];

        this._setupCanvas();
        this._initParticles();
        this._animate();

        window.addEventListener('resize', () => this._setupCanvas());
    }

    _setupCanvas() {
        const dpr = window.devicePixelRatio || 1;
        const rect = this.canvas.getBoundingClientRect();
        this.canvas.width = rect.width * dpr;
        this.canvas.height = rect.height * dpr;
        this.ctx.scale(dpr, dpr);
        this.cx = rect.width / 2;
        this.cy = rect.height / 2;
        this.radius = Math.min(rect.width, rect.height) / 2 - 20;
    }

    _initParticles() {
        // Floating particles around the orb
        for (let i = 0; i < 50; i++) {
            this.particles.push({
                angle: Math.random() * Math.PI * 2,
                distance: this.radius * (1 + Math.random() * 0.5),
                speed: 0.001 + Math.random() * 0.003,
                size: 1 + Math.random() * 2,
                opacity: 0.3 + Math.random() * 0.5,
            });
        }
    }

    setState(state) {
        const validStates = ['idle', 'listening', 'thinking', 'speaking', 'error'];
        if (!validStates.includes(state)) return;
        this.state = state;

        // Adjust intensity based on state
        switch (state) {
            case 'idle':      this.targetIntensity = 0.4; break;
            case 'listening': this.targetIntensity = 0.7; break;
            case 'thinking':  this.targetIntensity = 0.9; break;
            case 'speaking':  this.targetIntensity = 1.0; break;
            case 'error':     this.targetIntensity = 0.6; break;
        }
    }

    _getColor() {
        switch (this.state) {
            case 'listening': return { r: 0,   g: 217, b: 255 };  // cyan
            case 'thinking':  return { r: 251, g: 191, b: 36  };  // amber
            case 'speaking':  return { r: 74,  g: 158, b: 255 };  // blue
            case 'error':     return { r: 239, g: 68,  b: 68  };  // red
            default:          return { r: 0,   g: 217, b: 255 };  // cyan idle
        }
    }

    _animate() {
        this.time += 0.016;
        // Smooth intensity transition
        this.intensity += (this.targetIntensity - this.intensity) * 0.05;

        const ctx = this.ctx;
        const rect = this.canvas.getBoundingClientRect();

        // Clear
        ctx.clearRect(0, 0, rect.width, rect.height);

        const color = this._getColor();
        const colorStr = (a) => `rgba(${color.r}, ${color.g}, ${color.b}, ${a})`;

        // ---- Pulsing waves (rings around orb) ----
        const waveCount = this.state === 'idle' ? 2 : 4;
        for (let i = 0; i < waveCount; i++) {
            const phase = (this.time * (0.3 + i * 0.1)) % 1;
            const waveRadius = this.radius * (1 + phase * 0.4);
            const opacity = (1 - phase) * 0.3 * this.intensity;

            ctx.beginPath();
            ctx.arc(this.cx, this.cy, waveRadius, 0, Math.PI * 2);
            ctx.strokeStyle = colorStr(opacity);
            ctx.lineWidth = 1.5;
            ctx.stroke();
        }

        // ---- Outer glow ----
        const glowGradient = ctx.createRadialGradient(
            this.cx, this.cy, this.radius * 0.5,
            this.cx, this.cy, this.radius * 1.5
        );
        glowGradient.addColorStop(0, colorStr(0.3 * this.intensity));
        glowGradient.addColorStop(1, colorStr(0));
        ctx.fillStyle = glowGradient;
        ctx.fillRect(0, 0, rect.width, rect.height);

        // ---- Main orb (breathing) ----
        const breathe = Math.sin(this.time * 1.5) * 0.05 + 1;
        const orbRadius = this.radius * 0.7 * breathe;

        // Orb gradient
        const orbGradient = ctx.createRadialGradient(
            this.cx, this.cy, 0,
            this.cx, this.cy, orbRadius
        );
        orbGradient.addColorStop(0, colorStr(0.9 * this.intensity));
        orbGradient.addColorStop(0.5, colorStr(0.4 * this.intensity));
        orbGradient.addColorStop(1, colorStr(0.1 * this.intensity));

        ctx.beginPath();
        ctx.arc(this.cx, this.cy, orbRadius, 0, Math.PI * 2);
        ctx.fillStyle = orbGradient;
        ctx.fill();

        // ---- Inner core (bright center) ----
        const coreRadius = orbRadius * 0.3;
        const coreGradient = ctx.createRadialGradient(
            this.cx, this.cy, 0,
            this.cx, this.cy, coreRadius
        );
        coreGradient.addColorStop(0, `rgba(255, 255, 255, ${0.9 * this.intensity})`);
        coreGradient.addColorStop(0.5, colorStr(0.6 * this.intensity));
        coreGradient.addColorStop(1, colorStr(0));

        ctx.beginPath();
        ctx.arc(this.cx, this.cy, coreRadius, 0, Math.PI * 2);
        ctx.fillStyle = coreGradient;
        ctx.fill();

        // ---- Rotating outer ring ----
        const ringRadius = this.radius * 0.95;
        const segments = 60;
        const rotation = this.time * 0.5;

        for (let i = 0; i < segments; i++) {
            const angle = (i / segments) * Math.PI * 2 + rotation;
            const variation = Math.sin(angle * 3 + this.time * 2) * 0.5 + 0.5;
            const x = this.cx + Math.cos(angle) * ringRadius;
            const y = this.cy + Math.sin(angle) * ringRadius;
            const size = 1 + variation * 2;

            ctx.beginPath();
            ctx.arc(x, y, size, 0, Math.PI * 2);
            ctx.fillStyle = colorStr(variation * 0.8 * this.intensity);
            ctx.fill();
        }

        // ---- Floating particles ----
        for (const p of this.particles) {
            p.angle += p.speed;
            const x = this.cx + Math.cos(p.angle) * p.distance;
            const y = this.cy + Math.sin(p.angle) * p.distance;

            ctx.beginPath();
            ctx.arc(x, y, p.size, 0, Math.PI * 2);
            ctx.fillStyle = colorStr(p.opacity * this.intensity);
            ctx.fill();
        }

        // ---- State-specific overlays ----
        if (this.state === 'thinking') {
            // Faster spinning ring on thinking
            this._drawThinkingIndicator(ctx, colorStr);
        } else if (this.state === 'listening') {
            // Soundwave-like bars
            this._drawListeningBars(ctx, colorStr);
        }

        requestAnimationFrame(() => this._animate());
    }

    _drawThinkingIndicator(ctx, colorStr) {
        const segments = 8;
        for (let i = 0; i < segments; i++) {
            const angle = (i / segments) * Math.PI * 2 + this.time * 3;
            const r1 = this.radius * 1.1;
            const r2 = this.radius * 1.2;
            const x1 = this.cx + Math.cos(angle) * r1;
            const y1 = this.cy + Math.sin(angle) * r1;
            const x2 = this.cx + Math.cos(angle) * r2;
            const y2 = this.cy + Math.sin(angle) * r2;

            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y2);
            ctx.strokeStyle = colorStr((i / segments) * this.intensity);
            ctx.lineWidth = 3;
            ctx.lineCap = 'round';
            ctx.stroke();
        }
    }

    _drawListeningBars(ctx, colorStr) {
        const bars = 16;
        for (let i = 0; i < bars; i++) {
            const angle = (i / bars) * Math.PI * 2;
            const wave = Math.sin(this.time * 5 + i * 0.5) * 0.5 + 0.5;
            const r1 = this.radius * 1.05;
            const r2 = this.radius * (1.05 + wave * 0.15);
            const x1 = this.cx + Math.cos(angle) * r1;
            const y1 = this.cy + Math.sin(angle) * r1;
            const x2 = this.cx + Math.cos(angle) * r2;
            const y2 = this.cy + Math.sin(angle) * r2;

            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y2);
            ctx.strokeStyle = colorStr(wave * this.intensity);
            ctx.lineWidth = 2;
            ctx.lineCap = 'round';
            ctx.stroke();
        }
    }
}

// Initialize globally
let orb;
document.addEventListener('DOMContentLoaded', () => {
    orb = new AyyatOrb('orbCanvas');
    window.orb = orb;
});