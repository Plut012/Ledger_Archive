// Home Terminal Module - Boot Sequence Interface

const Home = {
    bootComplete: false,

    init(container) {
        this.render(container);
        if (!this.bootComplete) {
            this.runBootSequence();
            this.bootComplete = true;
        } else {
            // Returning to home - show interface immediately
            this.showMainInterface();
        }
    },

    render(container) {
        container.innerHTML = `
            <div class="home-container" style="
                display: flex;
                flex-direction: column;
                height: 100%;
                justify-content: center;
                padding: calc(var(--spacing-unit) * 3);
                background: #000;
                font-family: 'VT323', monospace;
                overflow: hidden;
            ">
                <div id="home-boot-log" style="
                    flex: 1;
                    overflow-y: hidden;
                    color: var(--color-dim);
                    line-height: 1.6;
                    font-size: 18px;
                "></div>

                <div id="home-ascii-logo" style="
                    text-align: center;
                    color: var(--color-primary);
                    margin: calc(var(--spacing-unit) * 2) 0;
                    font-size: 14px;
                    line-height: 1.2;
                    display: none;
                "></div>

                <div id="home-welcome" style="
                    color: var(--color-primary);
                    font-size: 20px;
                    text-align: center;
                    margin: calc(var(--spacing-unit) * 2) 0;
                    display: none;
                "></div>

                <div id="home-stats" style="
                    display: none;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: var(--spacing-unit);
                    margin: calc(var(--spacing-unit) * 2) 0;
                "></div>

                <div id="home-quick-actions" style="
                    display: none;
                    text-align: center;
                    margin-top: calc(var(--spacing-unit) * 2);
                "></div>
            </div>
        `;
    },

    async runBootSequence() {
        const log = document.getElementById('home-boot-log');

        const bootMessages = [
            { text: 'ARCHIVE STATION ALPHA :: TERMINAL INITIALIZATION', delay: 100 },
            { text: '═══════════════════════════════════════════════════', delay: 50 },
            { text: '', delay: 100 },
            { text: 'BIOS v4.7.2347 - Archive Intelligence Core', delay: 80 },
            { text: 'Memory: 2048 TB OK', delay: 60 },
            { text: 'Quantum Storage: ONLINE', delay: 60 },
            { text: 'Neural Interface: CONNECTED', delay: 80 },
            { text: '', delay: 100 },
            { text: 'Loading Archive Kernel...', delay: 150 },
            { text: '[████████████████████████] 100%', delay: 200 },
            { text: '', delay: 100 },
            { text: 'Initializing distributed ledger systems...', delay: 100 },
            { text: '  ✓ Blockchain Core v0.1.0', delay: 70 },
            { text: '  ✓ Cryptographic Vault', delay: 70 },
            { text: '  ✓ Network Mesh (4 nodes active)', delay: 70 },
            { text: '  ✓ Consensus Engine', delay: 70 },
            { text: '', delay: 150 },
            { text: 'Synchronizing stellar chronometer...', delay: 100 },
            { text: `  Current Stardate: ${this.getStardate()}`, delay: 80 },
            { text: '', delay: 150 },
            { text: 'Running system diagnostics...', delay: 100 },
            { text: '  Archive Integrity: [OK]', delay: 70 },
            { text: '  Chain Validation: [OK]', delay: 70 },
            { text: '  Network Status: [OK]', delay: 70 },
            { text: '  Security Protocols: [ACTIVE]', delay: 70 },
            { text: '', delay: 200 },
            { text: '═══════════════════════════════════════════════════', delay: 50 },
            { text: 'SYSTEM READY', delay: 100, color: 'var(--color-accent)' },
            { text: '═══════════════════════════════════════════════════', delay: 50 },
            { text: '', delay: 300 }
        ];

        // Run boot sequence
        for (const msg of bootMessages) {
            await this.bootLog(msg.text, msg.color);
            await this.wait(msg.delay);
        }

        // Show main interface
        this.showMainInterface();
    },

    async bootLog(message, color = 'var(--color-dim)') {
        const log = document.getElementById('home-boot-log');
        const line = document.createElement('div');
        line.textContent = message;
        line.style.color = color;
        log.appendChild(line);
        log.scrollTop = log.scrollHeight;

        // Subtle boot sound
        if (message && Math.random() > 0.5 && typeof AudioSystem !== 'undefined') {
            AudioSystem.sounds.type();
        }
    },

    async showMainInterface() {
        // Fetch stats
        const stats = await this.fetchStats();

        // Show logo
        const logo = document.getElementById('home-ascii-logo');
        logo.innerHTML = `
    ═══════════════════════════════════════════
         INTERSTELLAR ARCHIVE TERMINAL
    ═══════════════════════════════════════════

       "In the vastness of space,
        truth is the only constant.
        The ledger remembers all."
        `;
        logo.style.display = 'block';
        await this.wait(500);

        // Show welcome
        const welcome = document.getElementById('home-welcome');
        welcome.innerHTML = `
            <div style="margin-bottom: var(--spacing-unit);">
                ARCHIVE CAPTAIN
            </div>
            <div style="font-size: 16px; color: var(--color-dim);">
                SHIFT ${Math.floor(Math.random() * 9000) + 1000} :: ACTIVE
            </div>
        `;
        welcome.style.display = 'block';
        await this.wait(300);

        // Show stats
        const statsContainer = document.getElementById('home-stats');
        statsContainer.innerHTML = `
            <div class="stat-card" style="
                background: rgba(0, 255, 159, 0.05);
                border: 1px solid var(--color-primary);
                padding: var(--spacing-unit);
                border-radius: 4px;
            ">
                <div style="color: var(--color-dim); font-size: 14px;">CHAIN HEIGHT</div>
                <div style="color: var(--color-primary); font-size: 28px; margin-top: 4px;">
                    #${stats.height}
                </div>
            </div>

            <div class="stat-card" style="
                background: rgba(255, 215, 0, 0.05);
                border: 1px solid var(--color-accent);
                padding: var(--spacing-unit);
                border-radius: 4px;
            ">
                <div style="color: var(--color-dim); font-size: 14px;">PENDING TX</div>
                <div style="color: var(--color-accent); font-size: 28px; margin-top: 4px;">
                    ${stats.pending}
                </div>
            </div>

            <div class="stat-card" style="
                background: rgba(0, 255, 159, 0.05);
                border: 1px solid var(--color-primary);
                padding: var(--spacing-unit);
                border-radius: 4px;
            ">
                <div style="color: var(--color-dim); font-size: 14px;">NETWORK NODES</div>
                <div style="color: var(--color-primary); font-size: 28px; margin-top: 4px;">
                    4
                </div>
            </div>

            <div class="stat-card" style="
                background: rgba(0, 255, 159, 0.05);
                border: 1px solid ${stats.is_valid ? 'var(--color-primary)' : 'var(--color-error)'};
                padding: var(--spacing-unit);
                border-radius: 4px;
            ">
                <div style="color: var(--color-dim); font-size: 14px;">CHAIN STATUS</div>
                <div style="color: ${stats.is_valid ? 'var(--color-primary)' : 'var(--color-error)'}; font-size: 28px; margin-top: 4px;">
                    ${stats.is_valid ? '✓ VALID' : '✗ INVALID'}
                </div>
            </div>
        `;
        statsContainer.style.display = 'grid';
        await this.wait(300);

        // Show quick actions
        const actions = document.getElementById('home-quick-actions');
        actions.innerHTML = `
            <div style="display: flex; gap: var(--spacing-unit); justify-content: center; flex-wrap: wrap;">
                <button onclick="App.switchModule('chain-viewer')" style="
                    padding: calc(var(--spacing-unit) / 2) var(--spacing-unit);
                    background: transparent;
                    border: 1px solid var(--color-primary);
                    color: var(--color-primary);
                    font-family: 'VT323', monospace;
                    font-size: 18px;
                    cursor: pointer;
                    transition: all 0.2s;
                ">
                    [CHAIN VIEWER]
                </button>

                <button onclick="App.switchModule('crypto-vault')" style="
                    padding: calc(var(--spacing-unit) / 2) var(--spacing-unit);
                    background: transparent;
                    border: 1px solid var(--color-primary);
                    color: var(--color-primary);
                    font-family: 'VT323', monospace;
                    font-size: 18px;
                    cursor: pointer;
                    transition: all 0.2s;
                ">
                    [CRYPTO VAULT]
                </button>

                <button onclick="App.switchModule('network-monitor')" style="
                    padding: calc(var(--spacing-unit) / 2) var(--spacing-unit);
                    background: transparent;
                    border: 1px solid var(--color-primary);
                    color: var(--color-primary);
                    font-family: 'VT323', monospace;
                    font-size: 18px;
                    cursor: pointer;
                    transition: all 0.2s;
                ">
                    [NETWORK MONITOR]
                </button>
            </div>
        `;
        actions.style.display = 'block';

        // Success sound
        if (typeof AudioSystem !== 'undefined') {
            AudioSystem.sounds.success();
        }
    },

    async fetchStats() {
        try {
            const response = await fetch('/api/state');
            const data = await response.json();
            return {
                height: data.height,
                pending: data.pending_transactions,
                is_valid: data.is_valid
            };
        } catch (error) {
            console.error('Failed to fetch stats:', error);
            return {
                height: 0,
                pending: 0,
                is_valid: false
            };
        }
    },

    getStardate() {
        const now = new Date();
        const year = now.getFullYear();
        const dayOfYear = Math.floor((now - new Date(year, 0, 0)) / 86400000);
        return `${year}:${dayOfYear}`;
    },

    wait(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    },

    cleanup() {
        // Module cleanup
    }
};
