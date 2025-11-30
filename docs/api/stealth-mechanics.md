# Phase 06: Stealth Mechanics - Quick Reference

**Status**: ✅ COMPLETE | **Tests**: 23/23 PASSING | **Date**: 2025-11-29

---

## 🎯 What It Does

Allows players to evade ARCHIVIST monitoring when running restricted commands using multiple stealth techniques that become increasingly necessary as the game progresses.

---

## 🔑 Key Features

### Monitored Keywords
```
reconstruct, witness, testimony, upload, graveyard, iteration, reset
```

### Detection by Act
- **Act I-II**: 10% (MINIMAL - barely notices)
- **Act III**: 50% (ELEVATED - watching carefully)
- **Act IV**: 85% (HIGH - suspicious)
- **Act V+**: 100% (MAXIMUM - full awareness)

### Evasion Methods
1. **Log Masking**: 100% protection for 30 seconds
2. **Aliased Commands**: 50% reduction
3. **Conversation Distraction**: 70% reduction
4. **Validation Window**: 70% reduction
5. **Combined**: Methods stack multiplicatively

---

## 💻 API Endpoints

```bash
# Get monitoring status
GET /api/stealth/monitoring/status?player_id=default

# Mark ARCHIVIST busy (distraction)
POST /api/stealth/archivist/busy
{"durationSeconds": 5}

# Set validation active
POST /api/stealth/validation/active
{"active": true}

# Check command detection
POST /api/stealth/command/check
{"command": "reconstruct 74221", "playerId": "default"}

# Get evasion methods
GET /api/stealth/evasion/methods?player_id=default
```

---

## 🎮 Usage Examples

### In-Game Commands

**Log Masking:**
```bash
$ source ~/archive/.witness/logmask.sh
[LOG MASKING ACTIVE - 30 seconds]
$ reconstruct 74221  # Safe!
```

**Aliased Command:**
```bash
# Instead of: reconstruct 74221
$ chain.parse --deep --memo --block=74221
```

### Frontend Integration

**Check Before Running:**
```javascript
const check = await fetch('/api/stealth/command/check', {
  method: 'POST',
  body: JSON.stringify({command: "reconstruct 74221", playerId: "default"})
}).then(r => r.json());

if (check.suggestion) {
  console.log(`Try: ${check.suggestion}`);
}
```

**Mark Distraction:**
```javascript
// When player asks ARCHIVIST a question
await fetch('/api/stealth/archivist/busy', {
  method: 'POST',
  body: JSON.stringify({durationSeconds: 5})
});
```

**During Validation:**
```javascript
await fetch('/api/stealth/validation/active', {
  method: 'POST',
  body: JSON.stringify({active: true})
});

// ... validate block ...

await fetch('/api/stealth/validation/active', {
  method: 'POST',
  body: JSON.stringify({active: false})
});
```

---

## 📊 Evasion Effectiveness

### Act III Example
```
Direct: reconstruct 74221          → 50% detection
Alias: chain.parse --deep --memo   → 25% detection
+ Distraction                       → 7.5% detection
+ Validation                        → 2.25% detection
+ Log Mask                          → 0% detection
```

### Act IV Example
```
Direct: reconstruct 74221          → 85% detection
+ All methods (no log mask)         → 3.8% detection
+ Log mask                          → 0% detection
```

---

## 🗂️ Files

**Created:**
- `backend/stealth/monitor.py` - Core stealth system
- `backend/test_stealth_mechanics.py` - 23 unit tests
- `docs/integration_plans/06_IMPLEMENTATION_SUMMARY.md` - Full docs

**Modified:**
- `backend/main.py` - Added 4 API endpoints
- `backend/filesystem/commands.py` - Integrated StealthMonitor

---

## 🧪 Testing

```bash
# Run tests
python -m pytest test_stealth_mechanics.py -v

# Expected: 23 passed
```

---

## ⚡ Quick Start

### Backend (already integrated)
```python
from stealth.monitor import StealthMonitor

monitor = StealthMonitor()
result = monitor.check_command("reconstruct 74221", game_state)

if result.detected:
    suspicion += result.suspicion_increase
```

### Frontend (to implement)
```javascript
// 1. Check monitoring status before dangerous actions
// 2. Mark ARCHIVIST busy during conversations
// 3. Set validation active during block validation
// 4. Display detection chances in UI
```

---

## 📚 Key Classes

**StealthMonitor**
- `check_command(cmd, state)` → MonitoringResult
- `set_archivist_busy(seconds)` → None
- `set_validation_active(bool)` → None
- `get_evasion_suggestion(cmd)` → str | None
- `get_monitoring_status(state)` → dict

**MonitoringResult**
- `detected: bool` - Was detection triggered?
- `suspicion_increase: int` - How much to increase
- `detection_chance: float` - Probability (0.0-1.0)
- `reason: str` - Why detected

---

## 🎯 Integration Checklist

- ✅ Backend system complete
- ✅ API endpoints ready
- ✅ Tests passing
- ⏳ Frontend UI for monitoring status
- ⏳ Frontend hint system for aliases
- ⏳ Frontend distraction timing
- ⏳ Frontend validation hooks

---

## 💡 Design Notes

- Log masking provides "escape hatch" - always reliable
- Aliases feel like clever tricks players discover
- Distraction adds strategic timing element
- Late game requires combining multiple methods
- System creates tension without being punishing
- All detection chances are transparent to player

---

**For Full Details**: See `docs/integration_plans/06_IMPLEMENTATION_SUMMARY.md`
**For Completion**: See `PHASE_06_COMPLETE.md`
