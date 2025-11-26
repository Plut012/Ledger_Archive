# Integration Plan: Protocol Engine (Smart Contracts)

## ⚠️ Before You Start

Read [`DEVELOPMENT_PRINCIPLES.md`](DEVELOPMENT_PRINCIPLES.md) - This is a new module. Start with the simplest version!

## Decision Points - Ask First!

1. **Contract language**: Custom DSL, Python-like syntax, or JavaScript-like?
2. **Execution**: Actually execute contracts or simulate with pre-defined outputs?
3. **UI library**: Code editor component (Monaco, CodeMirror) or simple syntax-highlighted pre tags?
4. **Scope**: Full smart contract system or just story-critical contracts for narrative?

## Objective
Build the Protocol Engine module for smart contracts, including Witness reconstruction contracts and Imperial automated systems.

## Complexity: HIGH

**Why**: New module development, contract execution logic, UI for code display.

## Implementation Philosophy

**Start minimal**: Don't build a full smart contract VM. Start with displaying story-critical contracts and simulating their execution. Can expand later if needed.

---

## Implementation Summary

### Contract Types

**1. Reconstruction Contract (Witness)**
```javascript
contract ReconstructionEngine {
  function parseConsciousness(bytes32 blockHash) public returns (Testimony) {
    // Read archive transaction
    // Decode consciousness data
    // Return formatted testimony
  }
}
```

**2. Auto-Upload Contract (Imperial)**
```javascript
contract AutoTranscendence {
  // Automatically triggers upload when conditions met
  function checkConditions(address captain) public {
    if (suspicionLevel[captain] > THRESHOLD) {
      initiateTranscendence(captain);
    }
  }
}
```

### UI Design
- Code editor-style display
- Syntax highlighting
- Read-only for most contracts
- Player can deploy final testimony broadcast contract

### Horror Element
- Player discovers their own consciousness might be stored in a contract
- ARCHIVIST's reset protocol is a smart contract
- The Witness IS a distributed contract across the chain

**Estimated Effort**: 1-1.5 weeks (new module)
