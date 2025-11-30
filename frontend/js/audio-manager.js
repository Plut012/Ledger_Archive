/**
 * AudioManager - Simple audio system for Chain of Truth
 *
 * Handles all game sound effects with graceful degradation.
 * No dependencies - uses native Web Audio API.
 */

const AudioManager = {
    sounds: {},
    enabled: true,
    volume: 0.5,
    initialized: false,

    /**
     * Initialize audio system (call after user interaction to avoid autoplay blocking)
     */
    init() {
        if (this.initialized) return;

        this.loadSounds();
        this.initialized = true;
        console.log('[AudioManager] Initialized with', Object.keys(this.sounds).length, 'sounds');
    },

    /**
     * Load all sound files
     *
     * Sound files should be placed in /assets/sounds/
     * Files are optional - system will work without them
     */
    loadSounds() {
        const soundFiles = {
            // Boot sequence - Electronic hum building (2-3 seconds)
            // Suggested: Low synth pad with rising frequency
            boot: 'boot.mp3',

            // Block validation - Satisfying lock/confirm tone
            // Suggested: Clean digital beep, pitched up slightly
            blockValidate: 'block-validate.mp3',

            // Transaction propagation - Soft pulse traveling
            // Suggested: Gentle whoosh, subtle echo
            txPropagation: 'tx-propagation.mp3',

            // Station death - Electrical failure, distant
            // Suggested: Power-down sound, fading out
            stationDeath: 'station-death.mp3',

            // Witness message - Subtle static, whisper
            // Suggested: Soft white noise burst, organic feel
            witnessMessage: 'witness-message.mp3',

            // ARCHIVIST speaking - Clean, synthetic, cold
            // Suggested: Digital chime, precise and clinical
            archivistSpeak: 'archivist-speak.mp3',

            // Reconstruction - Data parsing sounds, fragments
            // Suggested: Digital processing, glitchy textures
            reconstruction: 'reconstruction.mp3',

            // Graveyard block click - Low, somber tone
            // Suggested: Deep bass note, reverberant
            graveyardClick: 'graveyard-click.mp3',

            // Final choice - Silence, then deep hum
            // Suggested: Sub-bass rumble, ominous
            finalChoice: 'final-choice.mp3',

            // Terminal typing - Optional typing sound
            // Suggested: Mechanical keyboard click
            terminalType: 'terminal-type.mp3'
        };

        for (const [name, file] of Object.entries(soundFiles)) {
            try {
                this.sounds[name] = new Audio(`/assets/sounds/${file}`);
                this.sounds[name].volume = this.volume;

                // Preload audio file
                this.sounds[name].load();

                // Handle load errors gracefully
                this.sounds[name].addEventListener('error', () => {
                    console.log(`[AudioManager] Sound file not found: ${file} (this is OK - sounds are optional)`);
                });
            } catch (err) {
                console.log(`[AudioManager] Failed to load ${name}:`, err.message);
            }
        }
    },

    /**
     * Play a sound by name
     * @param {string} soundName - Name of the sound to play
     * @param {number} volumeMultiplier - Optional volume multiplier (0-1)
     */
    play(soundName, volumeMultiplier = 1.0) {
        if (!this.enabled) return;
        if (!this.initialized) this.init();

        const sound = this.sounds[soundName];
        if (!sound) {
            console.log(`[AudioManager] Sound not found: ${soundName}`);
            return;
        }

        try {
            // Reset to start and apply volume
            sound.currentTime = 0;
            sound.volume = this.volume * volumeMultiplier;

            // Play with error handling (catches autoplay blocking)
            sound.play().catch(err => {
                // Autoplay blocked - this is expected on first load
                if (err.name === 'NotAllowedError') {
                    console.log('[AudioManager] Autoplay blocked - audio will work after user interaction');
                } else {
                    console.log('[AudioManager] Play failed:', err.message);
                }
            });
        } catch (err) {
            console.log(`[AudioManager] Error playing ${soundName}:`, err.message);
        }
    },

    /**
     * Set master volume (0-1)
     */
    setVolume(volume) {
        this.volume = Math.max(0, Math.min(1, volume));

        // Update all loaded sounds
        for (const sound of Object.values(this.sounds)) {
            if (sound) {
                sound.volume = this.volume;
            }
        }
    },

    /**
     * Enable/disable all audio
     */
    setEnabled(enabled) {
        this.enabled = enabled;
        console.log(`[AudioManager] Audio ${enabled ? 'enabled' : 'disabled'}`);
    },

    /**
     * Stop all currently playing sounds
     */
    stopAll() {
        for (const sound of Object.values(this.sounds)) {
            if (sound) {
                sound.pause();
                sound.currentTime = 0;
            }
        }
    }
};
