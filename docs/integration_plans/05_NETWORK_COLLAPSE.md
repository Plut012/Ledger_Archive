# Integration Plan: Network Collapse System

## Objective
Implement real-time station deaths, player weight calculation, 51% threshold visualization, and the doomsday clock mechanic in the Network Monitor.

## Complexity: MEDIUM
Scheduled events, animation, weight calculation logic.

---

## Implementation Summary

### Backend: Station Death Scheduler
```python
# backend/network/collapse.py
class NetworkCollapseScheduler:
    def __init__(self):
        self.death_schedule = self._generate_death_schedule()

    def _generate_death_schedule(self):
        # Act I-III: Slow decline (1-2 stations per "day")
        # Act IV: Accelerating (3-5 stations per "day")
        # Act V: Rapid collapse (10-15 stations in rapid succession)
        pass

    def check_station_deaths(self, game_state):
        """Check if any stations should die based on act/time"""
        if not game_state.session.collapse_begun:
            return []

        # Return list of station IDs to kill
        pass
```

### Frontend: Death Animations
```javascript
// frontend/modules/network-monitor.js
class NetworkMonitor {
  killStation(stationId, reason, finalMessage) {
    const node = this.nodes.get(stationId);

    // Flicker animation
    this.flicker(node, 1000);

    // Connections snap
    setTimeout(() => {
      this.snapConnections(node);
      node.status = 'DEAD';
      node.lastTransmission = finalMessage;

      // Update player weight
      this.recalculateWeights();

      // Play sound
      this.playSound('station-death');
    }, 1200);
  }

  recalculateWeights() {
    const activeNodes = this.getActiveNodes();
    const totalWeight = 100;

    // Player weight increases as network shrinks
    this.playerWeight = (totalWeight / activeNodes.length);

    // Update UI
    this.updateWeightDisplay();

    // Check 51% threshold
    if (this.playerWeight >= 30) {
      this.showCriticalWarning();
    }
  }
}
```

### Weight Visualization
- Pie chart showing consensus distribution
- Player slice grows as stations die
- Glowing warning at 30%+ (near 51% with 2 other stations)

**Estimated Effort**: 4-5 days
