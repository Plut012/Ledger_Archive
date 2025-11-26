# Integration Plan: Crypto Vault Story Integration

## Objective
Add keys from previous iterations, encrypted letters to future selves, and integrate vault with narrative progression.

## Complexity: LOW
Extending existing module with story elements.

---

## Implementation Summary

### Keys from Previous Iterations
```javascript
// When player starts Iteration 17, vault already contains keys from iterations 3, 7, 11, 14, 16

class CryptoVault {
  initializeFromPersistentState(persistentState) {
    // Load keys generated in previous iterations
    this.keys = persistentState.keys_generated;

    // Keys show metadata:
    // - Created: Duty Cycle 14
    // - Purpose: [unknown]
    // - Never used by current iteration
  }

  displayKeys() {
    this.keys.forEach(key => {
      console.log(`
        Key ID: ${key.id}
        Public Key: ${key.publicKey.substring(0, 32)}...
        Created: Duty Cycle ${key.iteration}
        ${key.iteration !== currentIteration ? '[FROM PREVIOUS ITERATION]' : ''}
      `);
    });
  }
}
```

### Encrypted Letters
```javascript
// Files encrypted to player's past/future public keys
// Player finds encrypted file: iteration_14_to_future.enc
// Must use corresponding private key from vault

async decryptLetter(encryptedFile, privateKey) {
  const decrypted = await decrypt(encryptedFile, privateKey);

  // Letter content from past self
  return `
    To whoever I become next:

    You won't remember writing this...
    [Letter content from GAMEPLAY_TECH.md]
  `;
}
```

### Puzzle: Matching Keys to Letters
- Player finds 5 encrypted letters
- Vault has 5 old keys from previous iterations
- Must figure out which key decrypts which letter
- Each successful decryption increases Witness trust

**Estimated Effort**: 2-3 days
