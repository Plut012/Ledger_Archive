// Chain Viewer Module

const ChainViewer = {
    blocks: [],
    selectedBlock: null,
    tamperedBlock: null,  // Track tampered block data

    // Infinite chain state
    viewWindow: { start: 0, end: 20 },  // Current visible window
    zoomLevel: 1,  // 1=blocks, 2=segments, 3=eras
    totalBlocks: 850000,  // Simulated Imperium history
    proceduralBlocks: new Map(),  // Cache for procedural blocks

    init(container) {
        this.render(container);
        this.fetchChain();
        this.setupEventListeners();

        // Listen for new blocks
        WebSocketClient.on('block_mined', () => this.fetchChain());
    },

    render(container) {
        container.innerHTML = `
            <div class="module-header">CHAIN</div>

            <div class="module-section">
                <div class="section-title">[NAVIGATION]</div>
                <div style="display: flex; gap: 8px; align-items: center; margin-bottom: var(--spacing-unit);">
                    <button id="btn-zoom-out" title="Zoom out">−</button>
                    <button id="btn-zoom-in" title="Zoom in">+</button>
                    <span style="color: var(--color-dim); margin: 0 8px;">|</span>
                    <button id="btn-scroll-left" title="Earlier blocks">←</button>
                    <button id="btn-scroll-right" title="Later blocks">→</button>
                    <button id="btn-jump-present" title="Jump to latest">⊙ Present</button>
                    <span id="chain-position" style="margin-left: auto; color: var(--color-dim); font-size: 12px;"></span>
                </div>
                <div id="chain-minimap" style="height: 20px; background: rgba(0,255,100,0.1); border: 1px solid var(--color-dim); position: relative; margin-bottom: var(--spacing-unit);">
                    <div id="minimap-indicator" style="position: absolute; height: 100%; background: rgba(0,255,100,0.3); border: 1px solid var(--color-primary);"></div>
                </div>
            </div>

            <div class="module-section">
                <div class="section-title">[CHAIN VISUALIZATION]</div>
                <div id="chain-viz" class="chain-container">
                    <!-- Blocks rendered here -->
                </div>
            </div>

            <div class="module-section">
                <div class="section-title">[BLOCK DETAILS]</div>
                <div id="block-details" class="block-details">
                    <div>Select a block to view details</div>
                </div>
            </div>

            <div class="module-section">
                <div class="section-title">[MINING CONTROLS]</div>
                <div style="margin-bottom: var(--spacing-unit);">
                    <label style="display: block; margin-bottom: 4px; color: var(--color-dim);">Miner Address (rewards recipient):</label>
                    <input type="text" id="miner-address" placeholder="Enter address or leave empty for DEFAULT_MINER" style="width: 100%; padding: 8px; background: rgba(0,255,100,0.05); border: 1px solid var(--color-dim); color: var(--color-text); font-family: 'Courier New', monospace;">
                </div>
                <div class="action-buttons">
                    <button id="btn-mine">Mine New Block</button>
                    <button id="btn-validate">Validate Chain</button>
                    <button id="btn-refresh">Refresh</button>
                </div>
            </div>
        `;
    },

    setupEventListeners() {
        document.getElementById('btn-mine')?.addEventListener('click', () => this.mineBlock());
        document.getElementById('btn-validate')?.addEventListener('click', () => this.validateChain());
        document.getElementById('btn-refresh')?.addEventListener('click', () => this.fetchChain());

        // Navigation controls
        document.getElementById('btn-zoom-in')?.addEventListener('click', () => this.zoomIn());
        document.getElementById('btn-zoom-out')?.addEventListener('click', () => this.zoomOut());
        document.getElementById('btn-scroll-left')?.addEventListener('click', () => this.scrollLeft());
        document.getElementById('btn-scroll-right')?.addEventListener('click', () => this.scrollRight());
        document.getElementById('btn-jump-present')?.addEventListener('click', () => this.jumpToPresent());
    },

    async fetchChain() {
        try {
            const response = await fetch('/api/chain');
            const data = await response.json();
            this.blocks = data.chain;
            this.renderChain();
        } catch (error) {
            console.error('Failed to fetch chain:', error);
            App.log('Error: Failed to fetch blockchain');
        }
    },

    async renderChain() {
        const container = document.getElementById('chain-viz');
        if (!container) return;

        container.innerHTML = '';

        // Render based on zoom level
        switch (this.zoomLevel) {
            case 1:
                await this.renderBlockView(container);
                break;
            case 2:
                this.renderSegmentView(container);
                break;
            case 3:
                this.renderEraView(container);
                break;
        }

        this.updateMinimap();
    },

    async renderBlockView(container) {
        // Show individual blocks within the view window
        const blocksToShow = Math.min(20, this.viewWindow.end - this.viewWindow.start);

        for (let i = 0; i < blocksToShow; i++) {
            const blockIndex = this.viewWindow.start + i;
            if (blockIndex >= this.totalBlocks) break;

            const block = await this.getBlockForDisplay(blockIndex);
            const isTampered = this.tamperedBlock && this.tamperedBlock.index === block.index;
            const isProcedural = block.is_procedural;
            const isGraveyard = block.isGraveyard || (blockIndex >= 50000 && blockIndex <= 75000);

            // Create block element
            const blockEl = document.createElement('div');
            let className = 'block-item';
            if (isTampered) className += ' tampered';
            if (isProcedural) className += ' procedural';
            if (isGraveyard) className += ' graveyard-block';

            blockEl.className = className;
            blockEl.textContent = `#${block.index}`;
            blockEl.dataset.index = blockIndex;

            let titleText = isProcedural ? 'Historical (procedural)' : 'Real block';
            if (isGraveyard) titleText += ' [GRAVEYARD]';
            blockEl.title = titleText;

            blockEl.addEventListener('click', () => this.selectBlock(blockIndex));

            container.appendChild(blockEl);

            // Add arrow if not last block
            if (i < blocksToShow - 1) {
                const arrow = document.createElement('div');
                arrow.className = 'block-arrow' + (isTampered ? ' broken' : '');
                arrow.textContent = isTampered ? '✗' : '→';
                container.appendChild(arrow);
            }
        }
    },

    renderSegmentView(container) {
        // Show clusters of 100 blocks
        const segmentsToShow = 20;
        const segmentSize = 100;

        for (let i = 0; i < segmentsToShow; i++) {
            const segmentStart = this.viewWindow.start + (i * segmentSize);
            if (segmentStart >= this.totalBlocks) break;

            const segmentEl = document.createElement('div');
            segmentEl.className = 'block-item segment';
            segmentEl.textContent = `#${segmentStart}-${segmentStart + segmentSize - 1}`;
            segmentEl.dataset.index = segmentStart;
            segmentEl.title = `100 blocks starting at #${segmentStart}`;

            segmentEl.addEventListener('click', () => {
                // Zoom into this segment
                this.viewWindow.start = segmentStart;
                this.viewWindow.end = segmentStart + segmentSize;
                this.zoomLevel = 1;
                App.log(`Zoomed into segment #${segmentStart}`);
                this.renderChain();
            });

            container.appendChild(segmentEl);

            if (i < segmentsToShow - 1 && segmentStart + segmentSize < this.totalBlocks) {
                const arrow = document.createElement('div');
                arrow.className = 'block-arrow';
                arrow.textContent = '→';
                container.appendChild(arrow);
            }
        }
    },

    renderEraView(container) {
        // Show eras of 10,000 blocks
        const erasToShow = 20;
        const eraSize = 10000;

        for (let i = 0; i < erasToShow; i++) {
            const eraStart = this.viewWindow.start + (i * eraSize);
            if (eraStart >= this.totalBlocks) break;

            const eraEl = document.createElement('div');
            eraEl.className = 'block-item era';
            eraEl.textContent = `ERA ${Math.floor(eraStart / eraSize)}`;
            eraEl.dataset.index = eraStart;
            eraEl.title = `10,000 blocks: #${eraStart.toLocaleString()} - #${(eraStart + eraSize - 1).toLocaleString()}`;

            eraEl.addEventListener('click', () => {
                // Zoom into this era
                this.viewWindow.start = eraStart;
                this.viewWindow.end = eraStart + eraSize;
                this.zoomLevel = 2;
                App.log(`Zoomed into Era ${Math.floor(eraStart / eraSize)}`);
                this.renderChain();
            });

            container.appendChild(eraEl);

            if (i < erasToShow - 1 && eraStart + eraSize < this.totalBlocks) {
                const arrow = document.createElement('div');
                arrow.className = 'block-arrow';
                arrow.textContent = '→';
                container.appendChild(arrow);
            }
        }
    },

    async selectBlock(index) {
        this.selectedBlock = index;
        const block = await this.getBlockForDisplay(index);

        // Play sound based on block range
        if (index >= 50000 && index <= 75000) {
            // Graveyard block - somber tone
            AudioManager.play('graveyardClick');
        } else {
            // Normal block - validation sound
            AudioManager.play('blockValidate');
        }

        // Update global state for tutorial validation
        window.selectedBlockIndex = index;

        // Update UI - match by dataset.index instead of position
        document.querySelectorAll('.block-item').forEach((el) => {
            el.classList.toggle('selected', parseInt(el.dataset.index) === index);
        });

        this.renderBlockDetails(block);
    },

    renderBlockDetails(block) {
        const container = document.getElementById('block-details');
        if (!container) return;

        // Check if this block has been tampered with
        const isTampered = this.tamperedBlock && this.tamperedBlock.index === block.index;
        const displayBlock = isTampered ? this.tamperedBlock : block;
        const isGraveyard = displayBlock.isGraveyard || (displayBlock.index >= 50000 && displayBlock.index <= 75000);

        // Calculate current hash and check if it matches
        let calculatedHash = displayBlock.hash;
        let hashMismatch = false;

        if (isTampered) {
            calculatedHash = this.calculateBlockHash(displayBlock);
            hashMismatch = calculatedHash !== block.hash;
        }

        const difficulty = displayBlock.hash.match(/^0*/)[0].length;
        const difficultyBar = Terminal.createProgressBar((difficulty / 10) * 100);

        // Render transactions with memo decoding and reconstruction
        const txListHtml = displayBlock.transactions.length > 0
            ? displayBlock.transactions.map((tx, i) => {
                const isCoinbase = tx.is_coinbase || tx.sender === 'COINBASE';
                const isArchive = tx.type === 'archive';
                const hasEncodedMemo = tx.memo && tx.memo.length > 0;

                let icon = isCoinbase ? '*' : '→';
                let style = isCoinbase ? 'color: var(--color-primary); font-weight: bold;' : '';
                let label = isCoinbase ? 'COINBASE' : 'TX';

                if (isArchive) {
                    icon = '✦';
                    style = 'color: var(--color-accent); font-weight: bold;';
                    label = 'ARCHIVE';
                }

                let memoHtml = '';
                if (hasEncodedMemo) {
                    memoHtml = `
                        <div style="margin-left: calc(var(--spacing-unit) * 3); margin-top: 4px;">
                            <span style="color: var(--color-dim);">Memo:</span>
                            <code style="background: rgba(0,255,100,0.1); padding: 2px 4px; font-size: 12px;">${tx.memo.substring(0, 40)}...</code>
                            <button onclick="ChainViewer.decodeMemo('${tx.memo}')" style="margin-left: 8px; padding: 2px 8px; font-size: 12px;">Decode</button>
                            ${isArchive ? `<button onclick="ChainViewer.reconstructConsciousness(${displayBlock.index}, ${i})" style="margin-left: 4px; padding: 2px 8px; font-size: 12px; background: var(--color-accent); border-color: var(--color-accent);">⚠ Reconstruct</button>` : ''}
                        </div>
                    `;
                }

                return `
                    <div class="detail-line" style="${style}; margin-left: calc(var(--spacing-unit) * 2);">
                        ${icon} ${label} #${i}: ${Terminal.truncateHash(tx.sender, 8)} → ${Terminal.truncateHash(tx.recipient || tx.receiver, 8)} (${tx.amount} ${tx.type === 'archive' ? 'UNITS' : 'CREDITS'})
                        ${memoHtml}
                    </div>
                `;
            }).join('')
            : '<div style="margin-left: calc(var(--spacing-unit) * 2); color: var(--color-dim);">No transactions</div>';

        // Show tamper button if tutorial is active and block is selected
        const tamperButton = (window.tutorialActive && !isTampered && block.index > 0)
            ? `<button id="btn-tamper-block" style="margin-top: var(--spacing-unit);">Tamper with Block</button>`
            : '';

        const restoreButton = isTampered
            ? `<button id="btn-restore-block" style="margin-top: var(--spacing-unit);">↺ Restore Original Data</button>`
            : '';

        // Hash mismatch warning
        const mismatchWarning = hashMismatch
            ? `<div style="margin-top: var(--spacing-unit); padding: var(--spacing-unit); border: 2px solid var(--color-accent); background: rgba(255,107,53,0.1);">
                <div style="color: var(--color-accent); font-weight: bold;">⚠ CHAIN INTEGRITY VIOLATION</div>
                <div style="margin-top: 4px; font-size: 14px;">Block hash has changed. Chain is broken.</div>
               </div>`
            : '';

        const timestampField = isTampered
            ? `<input type="text" id="tamper-timestamp" value="${displayBlock.timestamp}"
                      style="width: 100%; background: rgba(255,107,53,0.2); border: 1px solid var(--color-accent);
                             color: var(--color-primary); padding: 4px; font-family: var(--font-main);">`
            : displayBlock.timestamp;

        const graveyardLabel = isGraveyard ? `
            <div style="background: rgba(255,107,53,0.2); border: 1px solid var(--color-accent); padding: 8px; margin-bottom: var(--spacing-unit); color: var(--color-accent); font-weight: bold;">
                ⚠ GRAVEYARD BLOCK - Consciousness Archive Records
            </div>
        ` : '';

        container.innerHTML = `
            ${graveyardLabel}
            <div class="detail-line">
                <span class="detail-label">Index:</span>
                <span class="detail-value">#${displayBlock.index}</span>
            </div>
            <div class="detail-line">
                <span class="detail-label">Hash:</span>
                <span class="detail-value" style="${hashMismatch ? 'color: var(--color-accent);' : ''}">${calculatedHash}</span>
            </div>
            <div class="detail-line">
                <span class="detail-label">Previous Hash:</span>
                <span class="detail-value">${displayBlock.previous_hash}</span>
            </div>
            <div class="detail-line">
                <span class="detail-label">Expected Hash:</span>
                <span class="detail-value" style="${hashMismatch ? 'color: var(--color-dim);' : 'display: none;'}">${block.hash}</span>
            </div>
            <div class="detail-line">
                <span class="detail-label">Timestamp:</span>
                <span class="detail-value">${timestampField}</span>
            </div>
            <div class="detail-line">
                <span class="detail-label">Nonce:</span>
                <span class="detail-value">${displayBlock.nonce}</span>
            </div>
            <div class="detail-line">
                <span class="detail-label">Difficulty:</span>
                <span class="detail-value">${difficultyBar} (${difficulty})</span>
            </div>
            <div class="detail-line">
                <span class="detail-label">Transactions:</span>
                <span class="detail-value">${displayBlock.transactions.length}</span>
            </div>
            ${txListHtml}
            ${mismatchWarning}
            ${tamperButton}
            ${restoreButton}
        `;

        // Setup event listeners for tamper/restore buttons
        if (isTampered) {
            document.getElementById('tamper-timestamp')?.addEventListener('input', (e) => {
                this.tamperedBlock.timestamp = e.target.value;
                this.renderBlockDetails(block);
            });
            document.getElementById('btn-restore-block')?.addEventListener('click', () => {
                this.restoreBlock();
            });
        } else {
            document.getElementById('btn-tamper-block')?.addEventListener('click', () => {
                this.tamperWithBlock(block);
            });
        }
    },

    tamperWithBlock(block) {
        // Create a copy of the block for tampering
        this.tamperedBlock = JSON.parse(JSON.stringify(block));

        // Set global flag for tutorial validation
        window.blockTampered = true;

        App.log('⚠ Tampering with block data...');

        // Re-render chain to show visual break
        this.renderChain();
        this.renderBlockDetails(block);
    },

    restoreBlock() {
        const block = this.blocks[this.selectedBlock];
        this.tamperedBlock = null;
        window.blockTampered = false;

        App.log('✓ Block data restored to original');

        // Re-render chain to remove visual break
        this.renderChain();
        this.renderBlockDetails(block);
    },

    calculateBlockHash(block) {
        // Replicate the backend hash calculation logic
        const blockData = {
            index: block.index,
            timestamp: block.timestamp,
            transactions: block.transactions,
            previous_hash: block.previous_hash,
            nonce: block.nonce
        };

        // Sort keys to match Python's json.dumps(sort_keys=True)
        const sortedKeys = Object.keys(blockData).sort();
        const sortedData = {};
        sortedKeys.forEach(key => {
            sortedData[key] = blockData[key];
        });

        const blockString = JSON.stringify(sortedData);

        // Use sync hash function for immediate display
        return sha256Sync(blockString);
    },

    async mineBlock() {
        // Get miner address from input
        const minerInput = document.getElementById('miner-address');
        const minerAddress = minerInput?.value.trim() || 'DEFAULT_MINER';

        App.log(`Mining new block for ${minerAddress}...`);

        try {
            const response = await fetch('/api/mine', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ miner_address: minerAddress })
            });
            const data = await response.json();

            if (data.status === 'success') {
                App.log(`✓ Block #${data.block.index} mined successfully!`);

                if (data.coinbase) {
                    App.log(`* Mining reward: ${data.coinbase.reward} CREDITS → ${Terminal.truncateHash(data.coinbase.recipient, 16)}`);
                }

                // Update global state for tutorial validation
                window.lastMinedBlock = data.block;

                this.fetchChain();
            } else {
                App.log('Failed to mine block');
            }
        } catch (error) {
            console.error('Mining error:', error);
            App.log('Error: Mining failed');
        }
    },

    async validateChain() {
        try {
            const response = await fetch('/api/state');
            const data = await response.json();

            if (data.is_valid) {
                App.log('✓ Blockchain is valid');
            } else {
                App.log('✗ Blockchain validation failed');
            }
        } catch (error) {
            console.error('Validation error:', error);
            App.log('Error: Validation failed');
        }
    },

    // Navigation methods
    zoomIn() {
        if (this.zoomLevel > 1) {
            this.zoomLevel--;
            App.log(`Zoom: ${this.getZoomLevelName()}`);
            this.renderChain();
            this.updateMinimap();
        }
    },

    zoomOut() {
        if (this.zoomLevel < 3) {
            this.zoomLevel++;
            App.log(`Zoom: ${this.getZoomLevelName()}`);
            this.renderChain();
            this.updateMinimap();
        }
    },

    scrollLeft() {
        const step = this.getScrollStep();
        if (this.viewWindow.start > 0) {
            this.viewWindow.start = Math.max(0, this.viewWindow.start - step);
            this.viewWindow.end = this.viewWindow.start + step;
            this.renderChain();
            this.updateMinimap();
        }
    },

    scrollRight() {
        const step = this.getScrollStep();
        const maxStart = this.totalBlocks - step;
        if (this.viewWindow.start < maxStart) {
            this.viewWindow.start = Math.min(maxStart, this.viewWindow.start + step);
            this.viewWindow.end = this.viewWindow.start + step;
            this.renderChain();
            this.updateMinimap();
        }
    },

    jumpToPresent() {
        // Jump to the actual blockchain (not procedural)
        const realChainLength = this.blocks.length;
        this.viewWindow.start = Math.max(0, realChainLength - 20);
        this.viewWindow.end = realChainLength;
        this.zoomLevel = 1; // Reset to block view
        App.log('Jumped to present chain');
        this.renderChain();
        this.updateMinimap();
    },

    getScrollStep() {
        // How many blocks to scroll based on zoom level
        switch (this.zoomLevel) {
            case 1: return 20;      // Block view
            case 2: return 100;     // Segment view
            case 3: return 10000;   // Era view
            default: return 20;
        }
    },

    getZoomLevelName() {
        switch (this.zoomLevel) {
            case 1: return 'Block View';
            case 2: return 'Segment View (×100)';
            case 3: return 'Era View (×10,000)';
            default: return 'Unknown';
        }
    },

    updateMinimap() {
        const indicator = document.getElementById('minimap-indicator');
        const position = document.getElementById('chain-position');

        if (indicator && position) {
            // Calculate position as percentage of total chain
            const startPercent = (this.viewWindow.start / this.totalBlocks) * 100;
            const widthPercent = ((this.viewWindow.end - this.viewWindow.start) / this.totalBlocks) * 100;

            indicator.style.left = startPercent + '%';
            indicator.style.width = widthPercent + '%';

            // Update position text
            position.textContent = `Blocks ${this.viewWindow.start.toLocaleString()} - ${this.viewWindow.end.toLocaleString()} / ${this.totalBlocks.toLocaleString()}`;
        }
    },

    async getBlockForDisplay(index) {
        // Return real block if it exists
        if (index < this.blocks.length) {
            return this.blocks[index];
        }

        // Check cache first
        if (this.proceduralBlocks.has(index)) {
            return this.proceduralBlocks.get(index);
        }

        // Fetch from backend API (which uses deterministic generation)
        try {
            const response = await fetch(`/api/blockchain/block/${index}`);
            const block = await response.json();

            // Cache the block
            this.proceduralBlocks.set(index, block);

            // Limit cache size to 1000 blocks
            if (this.proceduralBlocks.size > 1000) {
                const firstKey = this.proceduralBlocks.keys().next().value;
                this.proceduralBlocks.delete(firstKey);
            }

            return block;
        } catch (error) {
            console.error('Failed to fetch block:', error);
            // Fallback to local procedural generation
            const block = ProceduralChain.generateBlock(index);
            this.proceduralBlocks.set(index, block);
            return block;
        }
    },

    decodeMemo(encodedMemo) {
        try {
            const decoded = atob(encodedMemo);
            App.log('Decoded memo:');
            App.log(decoded);
        } catch (error) {
            App.log('Error: Failed to decode memo');
        }
    },

    async reconstructConsciousness(blockIndex, txIndex) {
        App.log(`⚠ WARNING: Initiating consciousness reconstruction...`);
        App.log(`This action is MONITORED by ARCHIVIST systems.`);

        try {
            // Get player ID from state manager if available
            const playerId = window.stateManager?.playerId || 'default';

            const response = await fetch('/api/blockchain/reconstruct', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    blockIndex,
                    txIndex,
                    playerId
                })
            });

            const result = await response.json();

            if (result.error) {
                App.log(`Error: ${result.error}`);
                return;
            }

            // Display reconstruction in a modal or log
            App.log('─'.repeat(64));
            App.log(result.reconstruction);
            App.log('─'.repeat(64));

            // Update state if available
            if (result.stateUpdates && window.stateManager) {
                App.log(`⚠ ARCHIVIST Suspicion: +20 (now ${result.stateUpdates.archivistSuspicion})`);
                App.log(`✓ Witness Trust: +10 (now ${result.stateUpdates.witnessTrust})`);
            }

        } catch (error) {
            console.error('Reconstruction error:', error);
            App.log('Error: Failed to reconstruct consciousness');
        }
    },

    cleanup() {
        // Cleanup when module is unloaded
        this.blocks = [];
        this.selectedBlock = null;
        this.proceduralBlocks.clear();
    }
};
