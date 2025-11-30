# Phase 05: Network Collapse - Quick Reference

## 🎯 What It Does

Progressive station death system that creates escalating tension as the network collapses across Acts III-V, increasing player's consensus weight toward critical 51% threshold.

## 🚀 Quick Start

### Backend Test
```bash
cd backend
python demo_collapse.py
```

### Unit Tests
```bash
pytest test_network_collapse.py -v
```

### Frontend Integration
```javascript
// When Act V begins
await NetworkMonitor.startCollapseSequence();

// Manual check (or automatic via polling)
await NetworkMonitor.checkForStationDeaths();

// Stop collapse
NetworkMonitor.stopCollapseSequence();
```

## 📊 Death Schedule

| Act | Days | Deaths | Rate | Result |
|-----|------|--------|------|--------|
| III | 10-20 | ~14 | 1-2/day | 36 alive |
| IV | 20-25 | ~17 | 3-5/day | 19 alive |
| V | 25-28 | ~16 | Rapid | 3 alive |

**Trigger**: Iteration ≥15 OR Witness trust ≥90

## 🎨 Visual States

```
Normal:     ●  (green, glowing)
Flickering: ● → ○ → ● (1 sec)
Dead:       ◌  (dark red/gray, no connections)
```

## 📈 Weight Display

```
2.0% - 14.9%  → Green (normal)
15% - 29.9%   → Orange (elevated)
30% - 100%    → Red, pulsing (CRITICAL)
```

## 🔌 API Endpoints

```bash
# Get death schedule
GET /api/network/collapse/schedule

# Check for deaths at current time
POST /api/network/collapse/check
{"playerId": "default"}

# Advance time (testing)
POST /api/network/collapse/advance-time
{"playerId": "default", "increment": 0.5}

# Get current status
GET /api/network/collapse/status?player_id=default
```

## 📁 Key Files

```
backend/
  network/collapse.py          - Scheduler logic
  test_network_collapse.py     - Unit tests
  demo_collapse.py             - Interactive demo

frontend/
  js/modules/network-monitor.js  - Death animations
  css/modules.css                - Death styling

docs/
  PHASE_05_COMPLETE.md         - Full documentation
  integration_plans/05_*.md    - Planning docs
```

## 🔧 Configuration

```python
# backend/network/collapse.py
ACT_3_DEATHS_PER_DAY = (1, 2)    # Slow
ACT_4_DEATHS_PER_DAY = (3, 5)    # Fast
FINAL_STATIONS_ALIVE = 3         # Endgame
CRITICAL_WEIGHT = 30.0           # Warning threshold (%)
```

```javascript
// frontend/js/modules/network-monitor.js
COLLAPSE_POLL_INTERVAL = 2000    // ms between checks
FLICKER_DURATION = 1000          // ms flicker before death
```

## 🎮 Integration Hooks

### Start Collapse (in narrative trigger)
```python
# backend/narrative/triggers.py
def _begin_collapse(state):
    state.session.collapse_begun = True
    state.persistent.current_act = 5
    state.session.game_time = 25.0
    return state
```

### Frontend Polling (in network monitor)
```javascript
// Starts automatically when collapse_begun = true
this.collapseInterval = setInterval(() => {
    this.checkForStationDeaths();
}, 2000);
```

## 🧪 Testing

```bash
# Run all tests
pytest test_network_collapse.py -v

# Run demo
python demo_collapse.py

# Test determinism
python -c "
from network.collapse import NetworkCollapseScheduler
s1 = NetworkCollapseScheduler(seed=42).generate_death_schedule()
s2 = NetworkCollapseScheduler(seed=42).generate_death_schedule()
assert s1[0].station_id == s2[0].station_id
print('✓ Deterministic')
"
```

## 📝 Example Usage

```javascript
// Complete integration example
async function handleActTransition(newAct) {
  if (newAct === 5) {
    // Begin collapse
    await NetworkMonitor.startCollapseSequence();

    // Collapse will now automatically:
    // 1. Poll server every 2 seconds
    // 2. Animate any new deaths
    // 3. Update weight display
    // 4. Show critical warnings

    // When only 3 stations remain:
    // - Act VI trigger fires
    // - Player presented with final choice
  }
}
```

## 🐛 Troubleshooting

**Deaths not triggering?**
- Check `collapse_begun` flag is true
- Verify `game_time` is advancing
- Ensure `current_act` is 3+ for early deaths, 5 for rapid collapse

**Weight not updating?**
- Check `recalculateWeights()` is called after deaths
- Verify `deadStations` Set is being populated

**Animations stuttering?**
- Check browser FPS (should be 60)
- Verify `draw()` loop is running
- Check for JavaScript errors in console

## 📊 Success Criteria

- ✅ 12 unit tests passing
- ✅ Death schedule is deterministic
- ✅ Animations play smoothly (60 FPS)
- ✅ Weight calculations are accurate
- ✅ Critical warnings appear at 30%+
- ✅ 47 stations die, 3 survive

## 🔗 Related Phases

- **Phase 02**: Provides `GameState` and trigger system
- **Phase 04**: Graveyard blocks (deaths in past)
- **Phase 06**: Stealth mechanics (log masking during collapse)
- **Phase 09**: Home dashboard (shows collapse status)
- **Phase 10**: Audio (death sound effects)

## 📚 Documentation

- **Complete**: `PHASE_05_COMPLETE.md`
- **Implementation**: `docs/integration_plans/05_IMPLEMENTATION_SUMMARY.md`
- **Planning**: `docs/integration_plans/05_NETWORK_COLLAPSE.md`

---

**Status**: ✅ COMPLETE
**Last Updated**: 2025-11-29
