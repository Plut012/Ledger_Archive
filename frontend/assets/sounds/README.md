# Sound Assets

This directory contains audio files for Chain of Truth atmospheric sound design.

## Required Sound Files

All files are **optional** - the game will work without them. Audio system handles missing files gracefully.

### Sound Specifications

| File | Event | Description | Suggested Characteristics |
|------|-------|-------------|---------------------------|
| `boot.mp3` | Boot sequence | Electronic hum building | 2-3 seconds, low synth pad with rising frequency |
| `block-validate.mp3` | Block validation | Satisfying lock/confirm tone | Clean digital beep, pitched up slightly |
| `tx-propagation.mp3` | Transaction propagation | Soft pulse traveling | Gentle whoosh with subtle echo |
| `station-death.mp3` | Station death | Electrical failure, distant | Power-down sound, fading out |
| `witness-message.mp3` | Witness message | Subtle static, whisper | Soft white noise burst, organic feel |
| `archivist-speak.mp3` | ARCHIVIST speaking | Clean, synthetic, cold | Digital chime, precise and clinical |
| `reconstruction.mp3` | Reconstruction | Data parsing sounds, fragments | Digital processing with glitchy textures |
| `graveyard-click.mp3` | Graveyard block click | Low, somber tone | Deep bass note, reverberant |
| `final-choice.mp3` | Final choice | Silence, then deep hum | Sub-bass rumble, ominous |
| `terminal-type.mp3` | Terminal typing (optional) | Mechanical keyboard click | Single key press, short |

## Audio Guidelines

### Format
- **MP3** format (broad browser support)
- **Sample rate**: 44.1kHz or 48kHz
- **Bit rate**: 128-192 kbps (quality vs file size balance)

### Length
- Most sounds: 0.5-2 seconds
- Boot sequence: 2-3 seconds
- Final choice: 3-5 seconds

### Volume
- Normalize to **-3dB to -6dB** (prevents clipping)
- AudioManager applies 0.5 volume multiplier by default
- Avoid sudden loud sounds - keep atmosphere subtle

### Style
- **Minimalist** and **atmospheric**
- **Sci-fi/digital** aesthetic
- **Subtle** - sounds should enhance, not dominate
- **Cohesive** - all sounds should feel like they're from the same universe

## Creating Placeholder Sounds

If you need quick placeholders for testing:

### Using Web Audio API (Browser Console)
```javascript
// Generate simple beep
const audioCtx = new AudioContext();
const oscillator = audioCtx.createOscillator();
const gainNode = audioCtx.createGain();

oscillator.connect(gainNode);
gainNode.connect(audioCtx.destination);

oscillator.frequency.value = 440; // A4 note
gainNode.gain.value = 0.3;

oscillator.start();
oscillator.stop(audioCtx.currentTime + 0.5);
```

### Using Free Sound Resources
- **freesound.org** - Creative Commons licensed sounds
- **zapsplat.com** - Free sound effects (attribution required for free tier)
- **sonniss.com** - Annual GDC bundles (free, high quality)

### Recommended Search Terms
- "digital beep"
- "synth pad"
- "data processing"
- "power down"
- "computer terminal"
- "sci-fi interface"
- "glitch sound"

## Integration

Sounds are triggered via the AudioManager:

```javascript
import { audioManager } from './audio-manager.js';

// Initialize on user interaction
audioManager.init();

// Play a sound
audioManager.play('blockValidate');

// Adjust volume
audioManager.setVolume(0.7);

// Disable all audio
audioManager.setEnabled(false);
```

## Testing Without Sound Files

The AudioManager handles missing files gracefully:
- No errors thrown if files don't exist
- Console logs indicate which files are missing
- All game functionality works normally
- Add sound files later and they'll work immediately

## License

Ensure all sound files have appropriate licenses for use in this project.
