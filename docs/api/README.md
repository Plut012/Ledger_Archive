# API Reference

Quick reference guides for all Chain of Truth systems.

---

## Overview

This directory contains API quick references for each major system. Each document provides:
- API endpoint documentation
- Request/response examples
- Key functions and usage
- Integration examples

---

## API Documentation by System

### Narrative State System
**File**: [narrative-state.md](narrative-state.md)

**Key Endpoints**:
- `POST /api/narrative/state/init` - Initialize player state
- `POST /api/narrative/state/update` - Update state values
- `POST /api/narrative/state/reset` - Trigger iteration reset
- `GET /api/narrative/state/export` - Export for persistence
- `GET /api/narrative/state/llm-context` - Get LLM context

**WebSocket**: `/ws/narrative` - Real-time state updates

---

### Shell & Filesystem
**File**: [shell-filesystem.md](shell-filesystem.md)

**Key Endpoints**:
- `POST /api/shell/execute` - Execute terminal commands

**Commands**: ls, cd, cat, pwd, tree, clear, hash, verify, sign, decrypt, search, trace

---

### Chain Integration (Graveyard)
**File**: [chain-integration.md](chain-integration.md)

**Key Endpoints**:
- `GET /api/blockchain/block/{index}` - Get block by index
- `POST /api/blockchain/reconstruct` - Reconstruct testimony from graveyard

**Features**: Procedural generation, graveyard blocks (50K-75K), testimony parsing

---

### Network Collapse
**File**: [network-collapse.md](network-collapse.md)

**Key Endpoints**:
- `GET /api/network/status` - Current network state
- `GET /api/network/deaths` - Recent station deaths
- `POST /api/network/advance-time` - Progress game time

**Features**: Station death scheduling, weight calculation, critical thresholds

---

### Stealth Mechanics
**File**: [stealth-mechanics.md](stealth-mechanics.md)

**Key Endpoints**:
- `POST /api/stealth/check` - Check command detection
- `POST /api/stealth/distract` - Start ARCHIVIST distraction
- `POST /api/stealth/validation-start` - Begin validation window
- `GET /api/stealth/suggestions` - Get evasion recommendations

**Features**: Keyword monitoring, act-based escalation, 4 evasion methods

---

### Crypto Vault
**File**: [crypto-vault.md](crypto-vault.md)

**Key Endpoints**:
- `GET /api/vault/letters` - List available letters
- `POST /api/vault/decrypt-letter` - Decrypt specific letter
- `GET /api/vault/keys` - List keys from all iterations

**Features**: RSA-4096 encryption, 5 encrypted letters, trust-based unlocking

---

### Protocol Engine (Smart Contracts)
**File**: [protocol-engine.md](protocol-engine.md)

**Key Endpoints**:
- `GET /api/contracts/list` - List contracts with unlock status
- `GET /api/contracts/{id}` - Get contract code
- `POST /api/contracts/execute` - Execute contract function
- `POST /api/contracts/deploy` - Deploy testimony (Act VI)
- `GET /api/contracts/execution-log` - Execution history

**Features**: 5 smart contracts, syntax highlighting, horror reveal

---

### Home Dashboard
**File**: [home-dashboard.md](home-dashboard.md)

**Frontend Module**: `home.js`

**Features**: Act-based boot sequences, progressive glitch effects, color atmosphere shifts

---

### Audio & Visual
**File**: [audio-visual.md](audio-visual.md)

**Frontend Module**: `audio-manager.js`

**Features**: 10 sound effect hooks, graveyard particle effects, graceful degradation

---

## Common Patterns

### WebSocket Communication
```javascript
// Connect to WebSocket
const ws = new WebSocket('ws://localhost:8000/ws/narrative');

// Listen for state updates
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.type === 'narrative_state_update') {
    // Handle state change
  }
};
```

### State Management
```javascript
// Initialize narrative state
const response = await fetch('/api/narrative/state/init', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ player_id: 'default' })
});

// Update state
await fetch('/api/narrative/state/update', {
  method: 'POST',
  body: JSON.stringify({
    player_id: 'default',
    updates: { witness_trust: 45 }
  })
});
```

### Terminal Commands
```javascript
// Execute shell command
const response = await fetch('/api/shell/execute', {
  method: 'POST',
  body: JSON.stringify({
    player_id: 'default',
    command: 'ls -a'
  })
});
```

---

## API Server

**Base URL**: `http://localhost:8000`
**Interactive Docs**: `http://localhost:8000/docs` (Swagger UI)
**Health Check**: `http://localhost:8000/health`

---

## Related Documentation

- **Phase Implementation**: [../phases/](../phases/) - Detailed implementation docs
- **Integration Plans**: [../integration_plans/](../integration_plans/) - Original plans
- **System Architecture**: [../integration_plans/SYSTEM_ARCHITECTURE.md](../integration_plans/SYSTEM_ARCHITECTURE.md)

---

**For complete endpoint details, see individual API reference files above.**
