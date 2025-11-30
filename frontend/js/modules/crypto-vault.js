// Crypto Vault Module

const CryptoVault = {
    wallet: null,
    transactions: [],
    balance: 0,
    letters: [],
    keys: [],
    selectedLetter: null,

    init(container) {
        this.render(container);
        this.setupEventListeners();
        this.fetchTransactions();
        this.fetchBalance();
        this.fetchLetters();
        this.fetchKeys();

        // Refresh transactions and balance periodically
        this.refreshInterval = setInterval(() => {
            this.fetchTransactions();
            this.fetchBalance();
            this.fetchLetters();
            this.fetchKeys();
        }, 5000);
    },

    render(container) {
        container.innerHTML = `
            <div class="module-header">CRYPTOGRAPHIC VAULT</div>

            ${this.letters.length > 0 ? `
            <div class="module-section" style="background: rgba(255, 100, 0, 0.05); border-left: 3px solid #ff6400;">
                <div class="section-title">[ENCRYPTED LETTERS FROM PAST ITERATIONS]</div>
                <div id="letters-display">
                    ${this.renderLettersSection()}
                </div>
            </div>
            ` : ''}

            ${this.keys.length > 0 ? `
            <div class="module-section" style="background: rgba(0, 200, 255, 0.05); border-left: 3px solid #00c8ff;">
                <div class="section-title">[ENCRYPTION KEYS]</div>
                <div id="keys-display">
                    ${this.renderKeysSection()}
                </div>
            </div>
            ` : ''}

            ${this.wallet ? `
            <div class="module-section" style="background: rgba(0, 255, 100, 0.05); border-left: 3px solid var(--color-primary);">
                <div class="section-title">[ACCOUNT BALANCE]</div>
                <div id="balance-display" style="font-size: 1.5em; color: var(--color-primary); padding: var(--spacing-unit); font-family: 'Courier New', monospace;">
                    💰 ${this.balance.toFixed(2)} CREDITS
                </div>
            </div>
            ` : ''}

            <div class="module-section">
                <div class="section-title">[KEY MANAGEMENT]</div>
                <div id="wallet-display">
                    ${this.renderWalletSection()}
                </div>
            </div>

            <div class="module-section">
                <div class="section-title">[TRANSACTION BUILDER]</div>
                <div id="transaction-builder">
                    ${this.renderTransactionBuilder()}
                </div>
            </div>

            <div class="module-section">
                <div class="section-title">[TRANSACTION HISTORY]</div>
                <div id="transaction-history">
                    ${this.renderTransactionHistory()}
                </div>
            </div>
        `;
    },

    renderWalletSection() {
        if (!this.wallet) {
            return `
                <div class="wallet-empty">
                    <div>No wallet loaded</div>
                    <div class="action-buttons">
                        <button id="btn-generate-wallet">Generate New Keypair</button>
                    </div>
                </div>
            `;
        }

        return `
            <div class="wallet-info">
                <div class="detail-line">
                    <span class="detail-label">Address:</span>
                    <span class="detail-value" title="${this.wallet.address}">${this.wallet.address}</span>
                </div>
                <div class="detail-line">
                    <span class="detail-label">Public Key:</span>
                    <span class="detail-value" title="${this.wallet.public_key}">${Terminal.truncateHash(this.wallet.public_key, 16)}</span>
                </div>
                <div class="detail-line">
                    <span class="detail-label">Private Key:</span>
                    <span class="detail-value">████████████ (secured)</span>
                </div>
            </div>
            <div class="action-buttons">
                <button id="btn-generate-wallet">Generate New Keypair</button>
                <button id="btn-export-keys">Export Keys</button>
            </div>
        `;
    },

    renderTransactionBuilder() {
        if (!this.wallet) {
            return `<div class="builder-disabled">Generate a wallet first to create transactions</div>`;
        }

        return `
            <div class="transaction-form">
                <div class="form-group">
                    <label>From:</label>
                    <input type="text" id="tx-from" value="${Terminal.truncateHash(this.wallet.address, 16)}" disabled>
                </div>
                <div class="form-group">
                    <label>To:</label>
                    <input type="text" id="tx-to" placeholder="Recipient address">
                </div>
                <div class="form-group">
                    <label>Amount:</label>
                    <input type="number" id="tx-amount" placeholder="0.0" step="0.01" min="0.01" max="${this.balance}">
                    <span style="color: var(--color-dim); font-size: 0.9em;">CREDITS (Max: ${this.balance.toFixed(2)})</span>
                </div>
                <div id="balance-warning" style="color: var(--color-error); margin-top: var(--spacing-unit); display: none;">
                    ⚠️ Insufficient funds! You only have ${this.balance.toFixed(2)} CREDITS.
                </div>
                <div class="action-buttons">
                    <button id="btn-sign-broadcast">Sign & Broadcast</button>
                    <button id="btn-clear-form">Clear</button>
                </div>
            </div>
        `;
    },

    renderTransactionHistory() {
        if (this.transactions.length === 0) {
            return `<div class="history-empty">No transactions yet</div>`;
        }

        let html = '<div class="transaction-list">';

        this.transactions.forEach((tx, index) => {
            const statusIcon = tx.status === 'confirmed' ? '◉' : '◐';
            const statusClass = tx.status === 'confirmed' ? 'confirmed' : 'pending';

            html += `
                <div class="transaction-item ${statusClass}">
                    <span class="tx-hash">#${index + 1} ${Terminal.truncateHash(tx.hash, 8)}</span>
                    <span class="tx-arrow">→</span>
                    <span class="tx-recipient">${Terminal.truncateHash(tx.recipient, 8)}</span>
                    <span class="tx-amount">${tx.amount} ARC</span>
                    <span class="tx-status">${statusIcon} ${tx.status.toUpperCase()}</span>
                </div>
            `;
        });

        html += '</div>';
        return html;
    },

    setupEventListeners() {
        // Use event delegation since DOM might not be ready
        document.addEventListener('click', (e) => {
            if (e.target.id === 'btn-generate-wallet') {
                this.generateWallet();
            } else if (e.target.id === 'btn-export-keys') {
                this.exportKeys();
            } else if (e.target.id === 'btn-sign-broadcast') {
                this.signAndBroadcast();
            } else if (e.target.id === 'btn-clear-form') {
                this.clearForm();
            } else if (e.target.classList.contains('btn-decrypt-letter')) {
                const letterId = e.target.getAttribute('data-letter-id');
                // For now, we'll decrypt using the matching key automatically
                // In a more complex version, player could choose which key to try
                this.decryptLetter(letterId, 0);
            } else if (e.target.classList.contains('btn-view-letter')) {
                const letterId = e.target.getAttribute('data-letter-id');
                this.viewLetter(letterId);
            }
        });
    },

    async generateWallet() {
        try {
            App.log('Generating new wallet keypair...');

            const response = await fetch('/api/wallet/generate', {
                method: 'POST'
            });
            const data = await response.json();

            if (data.status === 'success') {
                this.wallet = data.wallet;
                App.log(`Wallet generated: ${Terminal.truncateHash(this.wallet.address, 16)}`);
                App.log('⚠️  Private key stored in memory - export to save!');

                // Update global state for tutorial validation
                window.walletAddress = this.wallet.address;

                // Fetch balance for new wallet
                await this.fetchBalance();

                // Re-render entire module to show balance section and new wallet
                const container = document.getElementById('module-container');
                if (container) {
                    this.render(container);
                }
            } else {
                App.log('Error: Failed to generate wallet');
            }
        } catch (error) {
            console.error('Wallet generation error:', error);
            App.log('Error: Wallet generation failed');
        }
    },

    exportKeys() {
        if (!this.wallet) return;

        const exportData = {
            address: this.wallet.address,
            public_key: this.wallet.public_key,
            private_key: this.wallet.private_key,
            warning: 'KEEP YOUR PRIVATE KEY SECURE! Never share it with anyone.'
        };

        const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `wallet-${this.wallet.address.substring(0, 8)}.json`;
        a.click();
        URL.revokeObjectURL(url);

        App.log('Wallet keys exported to file');
        App.log('⚠️  Keep this file secure - it contains your private key!');
    },

    clearForm() {
        document.getElementById('tx-to').value = '';
        document.getElementById('tx-amount').value = '';
    },

    async signAndBroadcast() {
        if (!this.wallet) {
            App.log('Error: No wallet available');
            return;
        }

        const recipient = document.getElementById('tx-to').value.trim();
        const amount = parseFloat(document.getElementById('tx-amount').value);

        // Validate inputs
        if (!recipient) {
            App.log('Error: Recipient address required');
            return;
        }

        if (isNaN(amount) || amount <= 0) {
            App.log('Error: Amount must be greater than 0');
            return;
        }

        // Check balance
        if (amount > this.balance) {
            App.log(`Error: Insufficient funds (have ${this.balance.toFixed(2)}, need ${amount.toFixed(2)})`);
            const warningEl = document.getElementById('balance-warning');
            if (warningEl) {
                warningEl.style.display = 'block';
                setTimeout(() => warningEl.style.display = 'none', 5000);
            }
            return;
        }

        try {
            App.log('Creating and signing transaction...');

            // Create transaction object
            const transaction = {
                sender: this.wallet.public_key,
                recipient: recipient,
                amount: amount,
                timestamp: new Date().toISOString(),
                signature: ''
            };

            // Sign the transaction using the wallet's sign method
            // We need to calculate the hash client-side to sign it
            const txHash = await this.calculateTransactionHash(transaction);
            const signature = await this.signMessage(txHash);
            transaction.signature = signature;

            // Broadcast to blockchain
            const response = await fetch('/api/transaction', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(transaction)
            });

            const result = await response.json();

            if (result.status === 'added') {
                App.log(`Transaction broadcast: ${Terminal.truncateHash(result.tx_hash, 16)}`);
                App.log('Status: PENDING (waiting for mining)');
                if (result.sender_balance_after !== undefined) {
                    App.log(`Balance after: ${result.sender_balance_after.toFixed(2)} CREDITS`);
                }

                // Clear form
                this.clearForm();

                // Refresh transaction history and balance
                setTimeout(() => {
                    this.fetchTransactions();
                    this.fetchBalance();
                }, 500);
            } else if (result.error === 'Insufficient funds') {
                App.log(`Error: Insufficient funds!`);
                App.log(`  Available: ${result.available.toFixed(2)} CREDITS`);
                App.log(`  Required: ${result.required.toFixed(2)} CREDITS`);
            } else {
                App.log(`Error: ${result.message || result.error || 'Transaction failed'}`);
            }
        } catch (error) {
            console.error('Transaction error:', error);
            App.log('Error: Transaction failed');
        }
    },

    async calculateTransactionHash(tx) {
        // Calculate hash the same way the backend does
        const txData = {
            sender: tx.sender,
            recipient: tx.recipient,
            amount: tx.amount,
            timestamp: tx.timestamp
        };
        const txString = JSON.stringify(txData, Object.keys(txData).sort());

        // Use Web Crypto API to calculate SHA-256
        const msgBuffer = new TextEncoder().encode(txString);
        const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    },

    async signMessage(message) {
        // Simplified signing on client side
        // Hash: message_hash + private_key + public_key
        const signatureInput = message + this.wallet.private_key + this.wallet.public_key;

        const msgBuffer = new TextEncoder().encode(signatureInput);
        const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    },

    async fetchTransactions() {
        if (!this.wallet) {
            this.transactions = [];
            return;
        }

        try {
            // Get transactions from blockchain and mempool
            const [chainResponse, mempoolResponse] = await Promise.all([
                fetch('/api/chain'),
                fetch('/api/mempool')
            ]);

            const chainData = await chainResponse.json();
            const mempoolData = await mempoolResponse.json();

            // Extract transactions involving this wallet
            const txList = [];
            const walletKey = this.wallet.public_key;

            // Get confirmed transactions from blocks
            if (chainData.chain) {
                chainData.chain.forEach(block => {
                    if (block.transactions) {
                        block.transactions.forEach(tx => {
                            if (tx.sender === walletKey || tx.recipient === walletKey) {
                                txList.push({
                                    hash: this.calculateTxHashSync(tx),
                                    sender: tx.sender,
                                    recipient: tx.recipient,
                                    amount: tx.amount,
                                    status: 'confirmed'
                                });
                            }
                        });
                    }
                });
            }

            // Get pending transactions from mempool
            if (mempoolData.transactions) {
                mempoolData.transactions.forEach(tx => {
                    if (tx.sender === walletKey || tx.recipient === walletKey) {
                        txList.push({
                            hash: this.calculateTxHashSync(tx),
                            sender: tx.sender,
                            recipient: tx.recipient,
                            amount: tx.amount,
                            status: 'pending'
                        });
                    }
                });
            }

            this.transactions = txList;

            // Update display
            const historyEl = document.getElementById('transaction-history');
            if (historyEl) {
                historyEl.innerHTML = this.renderTransactionHistory();
            }
        } catch (error) {
            console.error('Failed to fetch transactions:', error);
        }
    },

    async fetchBalance() {
        if (!this.wallet) {
            this.balance = 0;
            return;
        }

        try {
            const response = await fetch(`/api/balance/${this.wallet.public_key}`);
            const data = await response.json();

            this.balance = data.balance || 0;

            // Update balance display if it exists
            const balanceEl = document.getElementById('balance-display');
            if (balanceEl) {
                balanceEl.innerHTML = `💰 ${this.balance.toFixed(2)} CREDITS`;
            }

            // Update the transaction builder max amount
            const amountInput = document.getElementById('tx-amount');
            if (amountInput) {
                amountInput.max = this.balance;
            }
        } catch (error) {
            console.error('Failed to fetch balance:', error);
            this.balance = 0;
        }
    },

    calculateTxHashSync(tx) {
        // Simple hash for display purposes (not cryptographically computed)
        const str = `${tx.sender}${tx.recipient}${tx.amount}${tx.timestamp}`;
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            const char = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash;
        }
        return Math.abs(hash).toString(16);
    },

    cleanup() {
        // Clear interval when module is unloaded
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
        }

        // Note: We intentionally keep wallet in memory in case user switches back
        // In production, you might want to clear it for security
    },

    renderLettersSection() {
        if (!this.letters || this.letters.length === 0) {
            return '<div class="history-empty">No letters found</div>';
        }

        const decryptedCount = this.letters.filter(l => l.decrypted).length;
        const totalCount = this.letters.length;

        let html = `
            <div style="padding: var(--spacing-unit); color: var(--color-dim); margin-bottom: var(--spacing-unit);">
                Decrypted: ${decryptedCount}/${totalCount}
            </div>
            <div class="letter-list">
        `;

        this.letters.forEach(letter => {
            const statusIcon = letter.decrypted ? '✓' : '🔒';
            const statusClass = letter.decrypted ? 'decrypted' : 'encrypted';

            html += `
                <div class="letter-item ${statusClass}" data-letter-id="${letter.id}">
                    <div class="letter-header">
                        <span class="letter-icon">${statusIcon}</span>
                        <span class="letter-title">Iteration ${letter.from_iteration}</span>
                        <span class="letter-timestamp">${letter.timestamp}</span>
                    </div>
                    <div class="letter-preview">${letter.preview}</div>
                    ${!letter.decrypted ? `
                        <button class="btn-decrypt-letter" data-letter-id="${letter.id}">
                            Decrypt
                        </button>
                    ` : `
                        <button class="btn-view-letter" data-letter-id="${letter.id}">
                            View Full Letter
                        </button>
                    `}
                </div>
            `;
        });

        html += '</div>';
        return html;
    },

    renderKeysSection() {
        if (!this.keys || this.keys.length === 0) {
            return '<div class="history-empty">No encryption keys found</div>';
        }

        let html = `
            <div style="padding: var(--spacing-unit); color: var(--color-dim); margin-bottom: var(--spacing-unit);">
                Total Keys: ${this.keys.length}
            </div>
            <div class="key-list">
        `;

        this.keys.forEach(key => {
            const fromPast = key.from_past;
            const badge = fromPast ? '[FROM PAST ITERATION]' : '[CURRENT]';
            const badgeColor = fromPast ? '#ff6400' : 'var(--color-primary)';

            html += `
                <div class="key-item" data-key-index="${key.index}">
                    <div class="key-header">
                        <span class="key-iteration">Iteration ${key.iteration}</span>
                        <span class="key-badge" style="color: ${badgeColor};">${badge}</span>
                    </div>
                    <div class="key-preview" title="${key.public_key_preview}">
                        ${key.public_key_preview}
                    </div>
                    <div class="key-timestamp">${key.timestamp}</div>
                </div>
            `;
        });

        html += '</div>';
        return html;
    },

    async fetchLetters() {
        try {
            const response = await fetch('/api/vault/letters?player_id=default');
            const data = await response.json();

            if (data.letters) {
                this.letters = data.letters;

                // Update display if container exists
                const lettersEl = document.getElementById('letters-display');
                if (lettersEl) {
                    lettersEl.innerHTML = this.renderLettersSection();
                }
            }
        } catch (error) {
            console.error('Failed to fetch letters:', error);
            this.letters = [];
        }
    },

    async fetchKeys() {
        try {
            const response = await fetch('/api/vault/keys?player_id=default');
            const data = await response.json();

            if (data.keys) {
                this.keys = data.keys;

                // Update display if container exists
                const keysEl = document.getElementById('keys-display');
                if (keysEl) {
                    keysEl.innerHTML = this.renderKeysSection();
                }
            }
        } catch (error) {
            console.error('Failed to fetch keys:', error);
            this.keys = [];
        }
    },

    async decryptLetter(letterId, keyIndex) {
        try {
            App.log(`Attempting to decrypt letter from iteration ${letterId}...`);

            const response = await fetch('/api/vault/decrypt', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    playerId: 'default',
                    letterId: letterId,
                    keyIndex: keyIndex
                })
            });

            const data = await response.json();

            if (data.status === 'success') {
                App.log(`Letter decrypted successfully!`);
                App.log(`Witness trust increased by +${data.trust_increase}`);
                App.log(`---`);
                App.log(data.decrypted_content);
                App.log(`---`);

                // Refresh letters display
                await this.fetchLetters();
            } else if (data.status === 'already_decrypted') {
                App.log(`This letter has already been decrypted.`);
            } else {
                App.log(`Decryption failed: ${data.message || data.error}`);
            }
        } catch (error) {
            console.error('Decryption error:', error);
            App.log('Error: Failed to decrypt letter');
        }
    },

    async viewLetter(letterId) {
        // Find the decrypted letter content
        try {
            // Letter content is stored in messages_to_future after decryption
            const response = await fetch('/api/narrative/state/export?player_id=default');
            const stateData = await response.json();

            if (stateData.persistent && stateData.persistent.messages_to_future) {
                const letter = stateData.persistent.messages_to_future.find(m => m.id === letterId);
                if (letter) {
                    App.log('---');
                    App.log(letter.content);
                    App.log('---');
                } else {
                    App.log('Letter content not found');
                }
            }
        } catch (error) {
            console.error('Error viewing letter:', error);
            App.log('Error: Failed to retrieve letter content');
        }
    }
};
