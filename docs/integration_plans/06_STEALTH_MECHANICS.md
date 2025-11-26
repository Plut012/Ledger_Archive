# Integration Plan: Stealth Mechanics

## Objective
Implement ARCHIVIST command monitoring, aliased commands, log masking, and distraction mechanics.

## Complexity: MEDIUM
Real-time monitoring, timing mechanics, conversation-based distraction.

---

## Implementation Summary

### Monitored Keywords
```python
MONITORED = ["reconstruct", "witness", "testimony", "upload", "graveyard", "iteration", "reset"]
```

### Evasion Methods

**1. Aliased Commands**
```bash
# Instead of:
$ reconstruct block_74221

# Use:
$ chain.parse --deep --memo --block=74221
```

**2. Log Masking**
```bash
$ source ~/archive/.witness/logmask.sh
[LOG MASKING ACTIVE - 30 seconds]
$ reconstruct block_74221
[No suspicion increase for 30 seconds]
```

**3. Conversation Distraction**
```javascript
// While ARCHIVIST is generating long response to complex question
// Player can run monitored commands in background with reduced detection
engageARCHIVIST("Explain Merkle trees in detail")
  .then(() => {
    // ARCHIVIST "attention" is occupied
    runMonitoredCommand("reconstruct 74221"); // Lower detection chance
  });
```

**4. Validation Window**
```javascript
// During active block validation, ARCHIVIST attention is split
if (isValidatingBlock()) {
  detectionChance = 0.3; // 30% instead of 100%
}
```

### Escalation by Act
- **Act I-II**: ARCHIVIST barely notices
- **Act III**: Direct commands trigger warnings, aliases work
- **Act IV**: Even aliases flagged, must chain methods
- **Act V**: Full awareness, stealth no longer matters

**Estimated Effort**: 3-4 days
