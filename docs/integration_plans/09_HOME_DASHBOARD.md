# Integration Plan: Home Dashboard Progressive Degradation

## Objective
Update Home module to reflect act progression with visual and data degradation.

## Complexity: LOW
UI updates based on state.

---

## Implementation Summary

### Act-Based Dashboard States

```javascript
const DASHBOARD_STATES = {
  1: {
    chainStatus: 'HEALTHY',
    nodesActive: '47/50',
    consensus: 'NOMINAL',
    playerWeight: '2.1%',
    warnings: [],
    bgColor: '#1a1a2e'
  },
  3: {
    chainStatus: 'DEGRADED',
    nodesActive: '31/50',
    consensus: 'SYNCHRONIZING',
    playerWeight: '3.2%',
    warnings: ['Network fragmentation detected'],
    bgColor: '#2a1a1e'
  },
  5: {
    chainStatus: 'CRITICAL',
    nodesActive: '7/50',
    consensus: 'UNSTABLE',
    playerWeight: '14.3%',
    warnings: [
      'EMERGENCY: Validation authority concentration',
      'Multiple stations offline',
      'Consensus threshold approaching'
    ],
    bgColor: '#3a0a0a'
  },
  6: {
    chainStatus: 'TERMINAL',
    nodesActive: '3/50',
    consensus: 'DEADLOCKED',
    playerWeight: '34%',
    warnings: ['YOUR VOTE DECIDES CANONICAL CHAIN'],
    bgColor: '#4a0000',
    glitch: true
  }
};
```

### Visual Effects
- Progressive color shift (blue → red)
- Glitch effects in Act VI
- Duty Cycle counter prominently displayed
- Network health graph trending downward

**Estimated Effort**: 2-3 days
