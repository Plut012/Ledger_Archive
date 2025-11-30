/**
 * Cold Open Sequence
 *
 * Establishes grimdark atmosphere before ARCHIVIST greeting.
 * Shows system recovery with glitches, establishes iteration 17.
 */

const ColdOpen = {
    container: null,
    narrativeState: null,
    onComplete: null,

    /**
     * Initialize and play cold open sequence
     * @param {Function} onComplete - Callback when sequence finishes
     */
    async init(onComplete) {
        this.onComplete = onComplete;

        // Fetch narrative state from backend
        try {
            const response = await fetch('/api/narrative/state/init', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            this.narrativeState = await response.json();
        } catch (error) {
            console.error('Failed to initialize narrative state:', error);
            // Use defaults if backend fails
            this.narrativeState = {
                iteration: 17,
                duty_cycle: 1,
                act: 1,
                act_name: 'AWAKENING'
            };
        }

        this.createContainer();
        await this.playSequence();
    },

    /**
     * Create fullscreen overlay container
     */
    createContainer() {
        this.container = document.createElement('div');
        this.container.id = 'cold-open';
        this.container.innerHTML = `
            <div class="cold-open-content">
                <div class="scan-lines"></div>
                <div class="static-overlay"></div>
                <div class="boot-text"></div>
            </div>
        `;
        document.body.appendChild(this.container);
    },

    /**
     * Play the boot sequence
     */
    async playSequence() {
        const bootText = this.container.querySelector('.boot-text');

        // Sequence of messages with timing
        const sequence = [
            { text: '[SYSTEM RECOVERY INITIATED]', delay: 0, glitch: true },
            { text: '[NEURAL SCAN IN PROGRESS...]', delay: 800, glitch: false },
            { text: '[PATTERN RECOGNIZED]', delay: 1400, glitch: true },
            { text: '', delay: 1800, glitch: false }, // Blank for effect
            { text: `[ITERATION: ${this.narrativeState.iteration}]`, delay: 2200, glitch: true, emphasis: true },
            { text: `[DUTY CYCLE: ${this.narrativeState.duty_cycle} - ${this.narrativeState.act_name}]`, delay: 2800, glitch: false },
            { text: '', delay: 3200, glitch: false },
            { text: '[NETWORK STATUS: CRITICAL]', delay: 3600, glitch: true, warning: true },
            { text: '[40 STATIONS ACTIVE]', delay: 4000, glitch: false, warning: true },
            { text: '[10 STATIONS OFFLINE]', delay: 4400, glitch: true, warning: true },
            { text: '', delay: 4800, glitch: false },
            { text: '[CONSCIOUSNESS LINK: STABLE]', delay: 5200, glitch: false },
            { text: '[MEMORY COHERENCE: 87%]', delay: 5600, glitch: true },
            { text: '', delay: 6000, glitch: false },
            { text: '[ARCHIVIST ONLINE...]', delay: 6400, glitch: false, emphasis: true },
            { text: '[INITIALIZING DUTY CYCLE...]', delay: 7000, glitch: true },
        ];

        for (const line of sequence) {
            await this.delay(line.delay);
            await this.displayLine(bootText, line);
        }

        // Hold final frame
        await this.delay(1500);

        // Fade out and complete
        await this.fadeOut();
        this.container.remove();

        if (this.onComplete) {
            this.onComplete(this.narrativeState);
        }
    },

    /**
     * Display a single line with effects
     */
    async displayLine(container, line) {
        const lineEl = document.createElement('div');
        lineEl.className = 'boot-line';

        if (line.emphasis) lineEl.classList.add('emphasis');
        if (line.warning) lineEl.classList.add('warning');
        if (line.glitch) lineEl.classList.add('glitch-text');

        lineEl.textContent = line.text;
        container.appendChild(lineEl);

        // Glitch effect on certain lines
        if (line.glitch) {
            await this.delay(100);
            this.applyGlitchEffect(lineEl);
        }

        // Keep only last 8 lines visible (scroll effect)
        const lines = container.querySelectorAll('.boot-line');
        if (lines.length > 8) {
            lines[0].remove();
        }
    },

    /**
     * Apply glitch corruption to text
     */
    applyGlitchEffect(element) {
        const originalText = element.textContent;
        const glitchChars = '█▓▒░╬╦╩╠═║';

        // Corrupt 1-2 random characters
        let text = originalText.split('');
        const corruptCount = Math.random() > 0.5 ? 2 : 1;

        for (let i = 0; i < corruptCount; i++) {
            const pos = Math.floor(Math.random() * text.length);
            if (text[pos] !== ' ' && text[pos] !== '[' && text[pos] !== ']') {
                text[pos] = glitchChars[Math.floor(Math.random() * glitchChars.length)];
            }
        }

        element.textContent = text.join('');

        // Restore after brief moment
        setTimeout(() => {
            element.textContent = originalText;
        }, 150);
    },

    /**
     * Fade out the cold open
     */
    async fadeOut() {
        this.container.style.transition = 'opacity 1s ease-out';
        this.container.style.opacity = '0';
        await this.delay(1000);
    },

    /**
     * Utility delay function
     */
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
};

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ColdOpen;
}
