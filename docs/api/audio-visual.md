# Phase 10: Audio & Visual Polish - Quick Reference

## Audio System Usage

### Playing Sounds
```javascript
// Anywhere in the codebase
AudioManager.play('soundName');

// With volume adjustment
AudioManager.play('soundName', 0.5); // 50% volume
```

### Available Sounds
| Sound Name | Use Case |
|------------|----------|
| `boot` | Boot sequence start |
| `blockValidate` | Normal block click |
| `graveyardClick` | Graveyard block click |
| `stationDeath` | Network station dies |
| `reconstruction` | Deploy testimony |
| `finalChoice` | Testimony success |
| `txPropagation` | Transaction broadcast |
| `witnessMessage` | Witness speaks |
| `archivistSpeak` | ARCHIVIST speaks |
| `terminalType` | Terminal typing |

### Volume Control
```javascript
AudioManager.setVolume(0.7);  // 70% volume
AudioManager.setEnabled(false); // Disable all audio
AudioManager.stopAll();         // Stop all playing sounds
```

## Visual Effects

### Graveyard Blocks
Blocks #50,000-75,000 automatically get:
- Dark gradient background
- Inset shadows for depth
- Particle dust overlay
- Floating animation
- Somber tone on click

### Existing Effects (Phase 09)
- Scanlines intensify in Acts V-VI
- Glitch effects escalate by act
- Vignette darkness increases
- Color shifts from blue → red

## Adding Sound Files

1. Create MP3 files (44.1kHz, 128-192 kbps)
2. Place in `/frontend/assets/sounds/`
3. Name according to AudioManager sound map:
   - `boot.mp3`
   - `block-validate.mp3`
   - `graveyard-click.mp3`
   - etc.
4. Sounds load automatically on next page load

See `/frontend/assets/sounds/README.md` for detailed specifications.

## Integration Status

| Module | Integration | Status |
|--------|-------------|--------|
| home.js | Boot sound | ✅ Complete |
| chain-viewer.js | Block + graveyard sounds | ✅ Complete |
| network-monitor.js | Station death sound | ✅ Complete |
| protocol-engine.js | Reconstruction + final choice | ✅ Complete |
| station-shell.js | Character sounds | 🔲 Ready (not hooked) |

## File Locations

```
frontend/
├── js/
│   ├── audio-manager.js          # Audio system
│   └── main.js                   # AudioManager.init()
├── assets/
│   └── sounds/
│       ├── .gitkeep
│       ├── README.md             # Sound specifications
│       └── [sound files].mp3     # Add your sounds here
└── css/
    └── modules.css               # Graveyard visual effects
```

## Testing

1. **Without sound files**: Everything works, no errors
2. **With sound files**: Audio plays on events
3. **Autoplay blocked**: Audio works after first user click
4. **Visual effects**: Graveyard blocks have particles

## Troubleshooting

**No sound playing?**
- Check browser console for autoplay blocking
- Ensure sound files exist in `/assets/sounds/`
- Verify file names match AudioManager sound map
- Click anywhere to unblock autoplay

**Visual effects not showing?**
- Check graveyard blocks (#50K-75K)
- Verify CSS loaded (inspect element)
- Clear browser cache

---

**Phase 10**: Simple, robust, atmospheric. ✨
