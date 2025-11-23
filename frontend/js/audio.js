// Analog synth-style audio system using Web Audio API
// Warm, retro-futuristic sounds for the Archive Terminal

const AudioSystem = {
    audioContext: null,
    masterGain: null,
    enabled: true,

    init() {
        // Create audio context (lazy init on first user interaction)
        this.audioContext = new (window.AudioContext || window.webkitAudioContext)();

        // Master gain for volume control
        this.masterGain = this.audioContext.createGain();
        this.masterGain.gain.value = 0.3; // Subtle volume
        this.masterGain.connect(this.audioContext.destination);

        // Resume context on first user interaction (browser requirement)
        document.addEventListener('click', () => {
            if (this.audioContext.state === 'suspended') {
                this.audioContext.resume();
            }
        }, { once: true });

        console.log('Audio system initialized');
    },

    // Play a warm analog-style tone
    playTone(frequency, duration = 0.15, type = 'sine') {
        if (!this.enabled || !this.audioContext) return;

        const now = this.audioContext.currentTime;

        // Create oscillator for the tone
        const osc = this.audioContext.createOscillator();
        osc.type = type;
        osc.frequency.value = frequency;

        // Create gain envelope for smooth attack/release
        const gain = this.audioContext.createGain();
        gain.gain.value = 0;

        // Subtle attack and release for warmth
        gain.gain.setValueAtTime(0, now);
        gain.gain.linearRampToValueAtTime(0.3, now + 0.02);  // Quick attack
        gain.gain.exponentialRampToValueAtTime(0.01, now + duration);  // Smooth decay

        // Connect audio graph
        osc.connect(gain);
        gain.connect(this.masterGain);

        // Play
        osc.start(now);
        osc.stop(now + duration);
    },

    // Warm chord for important moments
    playChord(frequencies, duration = 0.4) {
        frequencies.forEach((freq, i) => {
            setTimeout(() => this.playTone(freq, duration, 'sine'), i * 30);
        });
    },

    // Sound effects for different events
    sounds: {
        // Typewriter character sound
        type() {
            AudioSystem.playTone(800 + Math.random() * 200, 0.03, 'square');
        },

        // New dialogue line
        dialogueStart() {
            AudioSystem.playChord([220, 330, 440], 0.3);  // Warm A minor chord
        },

        // Interaction complete
        success() {
            AudioSystem.playChord([523.25, 659.25, 783.99], 0.4);  // C major chord
        },

        // Tutorial progression
        progress() {
            AudioSystem.playChord([440, 554.37, 659.25], 0.5);  // A major chord
        },

        // System alert
        alert() {
            AudioSystem.playTone(880, 0.1, 'triangle');
            setTimeout(() => AudioSystem.playTone(1046.5, 0.1, 'triangle'), 100);
        },

        // Error or warning
        error() {
            AudioSystem.playTone(200, 0.3, 'sawtooth');
        },

        // Boot sequence
        boot() {
            const notes = [196, 220, 246.94, 293.66, 329.63];  // G A B D E
            notes.forEach((freq, i) => {
                setTimeout(() => AudioSystem.playTone(freq, 0.15, 'sine'), i * 80);
            });
        },

        // Module activation
        moduleLoad() {
            AudioSystem.playTone(523.25, 0.12, 'sine');
            setTimeout(() => AudioSystem.playTone(659.25, 0.12, 'sine'), 50);
        },

        // Memory fragment restored
        memoryRestore() {
            const sequence = [392, 440, 493.88, 523.25, 587.33, 659.25, 698.46, 783.99];
            sequence.forEach((freq, i) => {
                setTimeout(() => AudioSystem.playTone(freq, 0.08, 'sine'), i * 40);
            });
        },

        // Ambient background pulse (for dramatic moments)
        ambientPulse() {
            const pulse = () => {
                AudioSystem.playTone(55, 1.5, 'sine');  // Deep bass pulse
            };
            pulse();
        }
    },

    // Toggle audio on/off
    toggle() {
        this.enabled = !this.enabled;
        return this.enabled;
    },

    // Set master volume (0-1)
    setVolume(level) {
        if (this.masterGain) {
            this.masterGain.gain.value = Math.max(0, Math.min(1, level));
        }
    }
};

// Auto-initialize on load
window.addEventListener('DOMContentLoaded', () => {
    AudioSystem.init();
});
