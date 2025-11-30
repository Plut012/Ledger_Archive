/**
 * Narrative State Manager
 * Handles persistent and session state, IndexedDB storage, and WebSocket sync
 */

export class StateManager {
  constructor(playerId = 'default') {
    this.playerId = playerId;
    this.state = null;
    this.listeners = [];
    this.wsConnection = null;
    this.dbName = 'ChainOfTruth';
    this.storeName = 'gameState';
  }

  /**
   * Initialize state manager
   * Loads from IndexedDB if available, otherwise creates new state from server
   */
  async initialize() {
    // Try to load from IndexedDB first
    const saved = await this.loadFromIndexedDB();

    if (saved && saved.persistent && saved.session) {
      // Import saved state to server
      await this.importToServer(saved);
      this.state = saved;
      console.log('✓ Loaded state from IndexedDB', saved);
    } else {
      // Initialize new state from server
      const response = await fetch('/api/narrative/state/init', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ playerId: this.playerId })
      });

      this.state = await response.json();
      await this.saveToIndexedDB();
      console.log('✓ Initialized new state', this.state);
    }

    return this.state;
  }

  /**
   * Import saved state to server
   */
  async importToServer(state) {
    const response = await fetch('/api/narrative/state/import', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        playerId: this.playerId,
        state: state
      })
    });

    if (!response.ok) {
      console.error('Failed to import state to server');
    }
  }

  /**
   * Update game state with new values
   * Triggers evaluation of story triggers on server
   */
  async update(updates) {
    const response = await fetch('/api/narrative/state/update', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        playerId: this.playerId,
        updates
      })
    });

    const result = await response.json();

    // Check for reset
    if (result.reset) {
      await this.handleReset(result);
      return result;
    }

    this.state = result;
    await this.saveToIndexedDB();
    this.notifyListeners();

    return result;
  }

  /**
   * Handle iteration reset
   */
  async handleReset(resetData) {
    // Show reset cinematic
    await this.showResetSequence(resetData);

    // Clear session storage (localStorage)
    localStorage.clear();

    // Update state with new iteration
    this.state = resetData.state;

    await this.saveToIndexedDB();
    this.notifyListeners({ reset: true, iteration: resetData.iteration });
  }

  /**
   * Show reset sequence UI
   * Instant black screen as per user preference
   */
  async showResetSequence(resetData) {
    return new Promise((resolve) => {
      // Create full-screen overlay
      const overlay = document.createElement('div');
      overlay.id = 'reset-overlay';
      overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: black;
        color: #00ff41;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        font-family: 'Courier New', monospace;
        font-size: 1.2rem;
        line-height: 1.8;
        text-align: center;
      `;

      // Create message container
      const messageDiv = document.createElement('div');
      messageDiv.style.cssText = 'white-space: pre-line; padding: 2rem;';
      messageDiv.textContent = resetData.message;

      overlay.appendChild(messageDiv);
      document.body.appendChild(overlay);

      // Remove after 3 seconds
      setTimeout(() => {
        overlay.remove();
        resolve();
      }, 3000);
    });
  }

  /**
   * Manually trigger iteration reset
   */
  async resetIteration(reason = 'MANUAL_RESET') {
    const response = await fetch('/api/narrative/state/reset', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        playerId: this.playerId,
        reason
      })
    });

    const result = await response.json();
    await this.handleReset(result);
    return result;
  }

  /**
   * Save state to IndexedDB
   */
  async saveToIndexedDB() {
    try {
      const db = await this.openDB();
      const tx = db.transaction([this.storeName], 'readwrite');
      const store = tx.objectStore(this.storeName);

      await store.put({
        id: this.playerId,
        persistent: this.state.persistent,
        session: this.state.session,
        timestamp: Date.now()
      });

      await tx.complete;
    } catch (error) {
      console.error('Failed to save to IndexedDB:', error);
    }
  }

  /**
   * Load state from IndexedDB
   */
  async loadFromIndexedDB() {
    try {
      const db = await this.openDB();
      const tx = db.transaction([this.storeName], 'readonly');
      const store = tx.objectStore(this.storeName);
      const data = await store.get(this.playerId);

      return data || null;
    } catch (error) {
      console.error('Failed to load from IndexedDB:', error);
      return null;
    }
  }

  /**
   * Open IndexedDB database
   */
  openDB() {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(this.dbName, 1);

      request.onerror = () => reject(request.error);
      request.onsuccess = () => resolve(request.result);

      request.onupgradeneeded = (event) => {
        const db = event.target.result;
        if (!db.objectStoreNames.contains(this.storeName)) {
          db.createObjectStore(this.storeName, { keyPath: 'id' });
        }
      };
    });
  }

  /**
   * Setup WebSocket connection for real-time state sync
   */
  setupWebSocket(ws) {
    this.wsConnection = ws;

    // Listen for state updates from server
    ws.addEventListener('message', (event) => {
      try {
        const data = JSON.parse(event.data);

        if (data.type === 'narrative_state_update') {
          this.state = data.state;
          this.saveToIndexedDB();
          this.notifyListeners();
        } else if (data.type === 'narrative_reset') {
          this.handleReset(data);
        }
      } catch (error) {
        console.error('WebSocket message error:', error);
      }
    });
  }

  /**
   * Export state for LLM context
   */
  async exportForLLM() {
    const response = await fetch(
      `/api/narrative/state/llm-context?playerId=${this.playerId}`
    );
    return await response.json();
  }

  /**
   * Get current state
   */
  getState() {
    return this.state;
  }

  /**
   * Get specific state value
   */
  get(path) {
    const parts = path.split('.');
    let value = this.state;

    for (const part of parts) {
      if (value && typeof value === 'object') {
        value = value[part];
      } else {
        return undefined;
      }
    }

    return value;
  }

  /**
   * Subscribe to state changes
   */
  subscribe(listener) {
    this.listeners.push(listener);
    return () => {
      this.listeners = this.listeners.filter(l => l !== listener);
    };
  }

  /**
   * Notify all listeners of state changes
   */
  notifyListeners(data = {}) {
    this.listeners.forEach(listener => {
      try {
        listener({ ...this.state, ...data });
      } catch (error) {
        console.error('Listener error:', error);
      }
    });
  }

  /**
   * Helper: Increment suspicion
   */
  async incrementSuspicion(amount = 1) {
    const current = this.state.session.archivist_suspicion || 0;
    return await this.update({ archivist_suspicion: current + amount });
  }

  /**
   * Helper: Increment trust
   */
  async incrementTrust(amount = 1) {
    const current = this.state.session.witness_trust || 0;
    return await this.update({ witness_trust: current + amount });
  }

  /**
   * Helper: Add puzzle solved
   */
  async addPuzzleSolved(puzzleId) {
    const solved = new Set(this.state.persistent.puzzles_solved || []);
    solved.add(puzzleId);
    return await this.update({ puzzles_solved: Array.from(solved) });
  }

  /**
   * Helper: Add file discovered
   */
  async addFileDiscovered(filePath) {
    const files = new Set(this.state.session.files_discovered || []);
    files.add(filePath);
    return await this.update({ files_discovered: Array.from(files) });
  }

  /**
   * Helper: Add command to history
   */
  async addCommandToHistory(command) {
    const history = [...(this.state.session.command_history || []), command];
    const recent = history.slice(-20); // Keep last 20

    return await this.update({
      command_history: history,
      recent_commands: recent
    });
  }

  /**
   * Helper: Check if file is unlocked
   */
  isFileUnlocked(filePath) {
    const unlocked = this.state.persistent.files_unlocked || [];
    return unlocked.includes(filePath);
  }

  /**
   * Helper: Check if puzzle is solved
   */
  isPuzzleSolved(puzzleId) {
    const solved = this.state.persistent.puzzles_solved || [];
    return solved.includes(puzzleId);
  }
}

// Export singleton instance
export const stateManager = new StateManager();
