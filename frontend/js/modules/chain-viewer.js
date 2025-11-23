// Chain Viewer Module

const ChainViewer = {
    blocks: [],
    selectedBlock: null,
    tamperedBlock: null,  // Track tampered block data

    init(container) {
        this.render(container);
        this.fetchChain();
        this.setupEventListeners();

        // Listen for new blocks
        WebSocketClient.on('block_mined', () => this.fetchChain());
    },

    render(container) {
        container.innerHTML = `
            <div class="module-header">ARCHIVE CHAIN VIEWER</div>

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

    renderChain() {
        const container = document.getElementById('chain-viz');
        if (!container) return;

        container.innerHTML = '';

        this.blocks.forEach((block, index) => {
            // Check if this block is tampered
            const isTampered = this.tamperedBlock && this.tamperedBlock.index === block.index;

            // Create block element
            const blockEl = document.createElement('div');
            blockEl.className = 'block-item' + (isTampered ? ' tampered' : '');
            blockEl.textContent = `#${block.index}`;
            blockEl.dataset.index = index;

            blockEl.addEventListener('click', () => this.selectBlock(index));

            container.appendChild(blockEl);

            // Add arrow if not last block
            if (index < this.blocks.length - 1) {
                const arrow = document.createElement('div');
                arrow.className = 'block-arrow' + (isTampered ? ' broken' : '');
                arrow.textContent = isTampered ? '✗' : '→';
                container.appendChild(arrow);
            }
        });

        // Select latest block by default
        if (this.blocks.length > 0 && this.selectedBlock === null) {
            this.selectBlock(this.blocks.length - 1);
        }
    },

    selectBlock(index) {
        this.selectedBlock = index;
        const block = this.blocks[index];

        // Update global state for tutorial validation
        window.selectedBlockIndex = index;

        // Update UI
        document.querySelectorAll('.block-item').forEach((el, i) => {
            el.classList.toggle('selected', i === index);
        });

        this.renderBlockDetails(block);
    },

    renderBlockDetails(block) {
        const container = document.getElementById('block-details');
        if (!container) return;

        // Check if this block has been tampered with
        const isTampered = this.tamperedBlock && this.tamperedBlock.index === block.index;
        const displayBlock = isTampered ? this.tamperedBlock : block;

        // Calculate current hash and check if it matches
        let calculatedHash = displayBlock.hash;
        let hashMismatch = false;

        if (isTampered) {
            calculatedHash = this.calculateBlockHash(displayBlock);
            hashMismatch = calculatedHash !== block.hash;
        }

        const difficulty = displayBlock.hash.match(/^0*/)[0].length;
        const difficultyBar = Terminal.createProgressBar((difficulty / 10) * 100);

        // Render transactions
        const txListHtml = displayBlock.transactions.length > 0
            ? displayBlock.transactions.map((tx, i) => {
                const isCoinbase = tx.is_coinbase || tx.sender === 'COINBASE';
                const icon = isCoinbase ? '*' : '→';
                const style = isCoinbase ? 'color: var(--color-primary); font-weight: bold;' : '';
                const label = isCoinbase ? 'COINBASE' : 'TX';

                return `
                    <div class="detail-line" style="${style}; margin-left: calc(var(--spacing-unit) * 2);">
                        ${icon} ${label} #${i}: ${Terminal.truncateHash(tx.sender, 8)} → ${Terminal.truncateHash(tx.recipient, 8)} (${tx.amount} CREDITS)
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

        container.innerHTML = `
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

    cleanup() {
        // Cleanup when module is unloaded
        this.blocks = [];
        this.selectedBlock = null;
    }
};
