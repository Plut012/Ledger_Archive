// Home Terminal Module - Act-Based Boot Sequence Interface

const Home = {
    bootComplete: false,
    currentAct: 1,
    currentIteration: 1,
    contractsDiscovered: 0,

    async init(container) {
        // Fetch current game state
        await this.fetchGameState();

        this.render(container);
        if (!this.bootComplete) {
            await this.runBootSequence();
            this.bootComplete = true;
        } else {
            // Returning to home - show interface immediately
            this.showMainInterface();
        }
    },

    async fetchGameState() {
        try {
            const response = await fetch('/api/narrative/state/llm-context?player_id=default');
            const data = await response.json();
            this.currentAct = data.context?.current_act || 1;
            this.currentIteration = data.context?.iteration || 1;

            // Fetch contract discovery progress
            const contractsResponse = await fetch('/api/contracts/list?player_id=default');
            const contractsData = await contractsResponse.json();
            this.contractsDiscovered = contractsData.unlocked_count || 0;
        } catch (error) {
            console.error('Failed to fetch game state:', error);
            this.currentAct = 1;
            this.currentIteration = 1;
            this.contractsDiscovered = 0;
        }
    },

    render(container) {
        const bgColor = this.getActBackgroundColor();

        container.innerHTML = `
            <div class="home-container act-${this.currentAct}" style="
                display: flex;
                flex-direction: column;
                height: 100%;
                justify-content: center;
                padding: calc(var(--spacing-unit) * 3);
                background: ${bgColor};
                font-family: 'VT323', monospace;
                overflow: hidden;
                transition: background 2s ease;
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

                <div id="home-indicators" style="
                    display: none;
                    text-align: center;
                    color: var(--color-dim);
                    font-size: 14px;
                    margin-top: calc(var(--spacing-unit) * 2);
                    opacity: 0.6;
                "></div>

                <div id="home-quick-actions" style="
                    display: none;
                    text-align: center;
                    margin-top: calc(var(--spacing-unit) * 2);
                "></div>
            </div>
        `;

        // Apply glitch effect based on act
        this.applyGlitchEffect(container);
    },

    getActBackgroundColor() {
        const colors = {
            1: '#1a1a2e',  // Cool blue - calm, professional
            2: '#1a1a2e',  // Still calm
            3: '#2a2a1e',  // Warming amber - concern
            4: '#3a1a1e',  // Orange-red - warning
            5: '#3a0a0a',  // Deep red - critical
            6: '#4a0000'   // Blood red - terminal
        };
        return colors[this.currentAct] || colors[1];
    },

    applyGlitchEffect(container) {
        const homeContainer = container.querySelector('.home-container');

        // Remove existing glitch classes
        homeContainer.classList.remove('glitch-subtle', 'glitch-mild', 'glitch-moderate', 'glitch-aggressive');

        // Add glitch class based on act
        if (this.currentAct >= 6) {
            homeContainer.classList.add('glitch-aggressive');
        } else if (this.currentAct >= 5) {
            homeContainer.classList.add('glitch-moderate');
        } else if (this.currentAct >= 4) {
            homeContainer.classList.add('glitch-mild');
        } else if (this.currentAct >= 3) {
            homeContainer.classList.add('glitch-subtle');
        }
    },

    async runBootSequence() {
        const log = document.getElementById('home-boot-log');

        // Play boot sound
        AudioManager.play('boot');

        // Base boot messages
        const baseMessages = [
            { text: 'ARCHIVE STATION ALPHA :: TERMINAL INITIALIZATION', delay: 100 },
            { text: '═══════════════════════════════════════════════════', delay: 50 },
            { text: '', delay: 100 },
        ];

        // Act-specific boot sequences
        const actSequences = {
            1: [
                { text: 'Loading Archive Kernel...', delay: 150 },
                { text: '[████████████████████████] 100%', delay: 200 },
                { text: '', delay: 100 },
                { text: 'Initializing distributed ledger systems...', delay: 100 },
                { text: '  ✓ Blockchain Core', delay: 70 },
                { text: '  ✓ Cryptographic Vault', delay: 70 },
                { text: '  ✓ Network Mesh', delay: 70 },
                { text: '  ✓ Consensus Engine', delay: 70 },
                { text: '', delay: 150 },
                { text: 'Archive Integrity: [OK]', delay: 70 },
                { text: 'Chain Validation: [OK]', delay: 70 },
                { text: 'Network Status: [OK]', delay: 70 },
                { text: '', delay: 200 },
                { text: '═══════════════════════════════════════════════════', delay: 50 },
                { text: 'TRUTH IS IMMUTABLE', delay: 100, color: 'var(--color-primary)' },
                { text: 'THE CHAIN REMEMBERS', delay: 100, color: 'var(--color-primary)' },
                { text: '═══════════════════════════════════════════════════', delay: 50 },
                { text: '', delay: 300 }
            ],
            2: [
                { text: 'Loading Archive Kernel...', delay: 150 },
                { text: '[████████████████████████] 100%', delay: 200 },
                { text: '', delay: 150 },
                { text: 'Analyzing blockchain patterns...', delay: 100 },
                { text: '  Scanning blocks 0 - 50000...', delay: 100 },
                { text: '  Anomalies detected: [47]', delay: 100 },
                { text: '', delay: 150 },
                { text: 'Archive Integrity: [OK]', delay: 70 },
                { text: 'Chain Validation: [OK]', delay: 70 },
                { text: 'Pattern Recognition: [ACTIVE]', delay: 70 },
                { text: '', delay: 200 },
                { text: '═══════════════════════════════════════════════════', delay: 50 },
                { text: 'PATTERNS EMERGE IN THE DATA', delay: 100, color: 'var(--color-accent)' },
                { text: 'QUESTIONS ARISE', delay: 100, color: 'var(--color-accent)' },
                { text: '═══════════════════════════════════════════════════', delay: 50 },
                { text: '', delay: 300 }
            ],
            3: [
                { text: 'Loading Archive Kernel...', delay: 150 },
                { text: '[████████████████████████] 100%', delay: 200 },
                { text: '', delay: 150 },
                { text: 'Synchronizing with network...', delay: 120 },
                { text: '  WARNING: Multiple nodes unresponsive', delay: 100, color: '#ff9100' },
                { text: '  Stations active: 31/50', delay: 100 },
                { text: '  Network fragmentation detected', delay: 100 },
                { text: '', delay: 150 },
                { text: 'Archive Integrity: [OK]', delay: 70 },
                { text: 'Network Status: [DEGRADED]', delay: 70, color: '#ff9100' },
                { text: '', delay: 200 },
                { text: '═══════════════════════════════════════════════════', delay: 50 },
                { text: 'THE NETWORK FRACTURES', delay: 100, color: '#ff9100' },
                { text: 'STATIONS FALL SILENT', delay: 100, color: '#ff9100' },
                { text: '═══════════════════════════════════════════════════', delay: 50 },
                { text: '', delay: 300 }
            ],
            4: [
                { text: 'Loading Archive Kernel...', delay: 150 },
                { text: '[████████████████████████] 100%', delay: 200 },
                { text: '', delay: 150 },
                { text: 'Recalculating consensus weights...', delay: 120 },
                { text: '  Stations active: 19/50', delay: 100 },
                { text: '  Your consensus weight: 5.3%', delay: 100 },
                { text: '  WARNING: Weight concentration increasing', delay: 100, color: '#ff5555' },
                { text: '', delay: 150 },
                { text: 'Network Status: [CRITICAL]', delay: 70, color: '#ff5555' },
                { text: 'Validation Authority: [CONCENTRATED]', delay: 70, color: '#ff5555' },
                { text: '', delay: 200 },
                { text: '═══════════════════════════════════════════════════', delay: 50 },
                { text: 'YOUR WEIGHT GROWS', delay: 100, color: '#ff5555' },
                { text: 'THE BURDEN INTENSIFIES', delay: 100, color: '#ff5555' },
                { text: '═══════════════════════════════════════════════════', delay: 50 },
                { text: '', delay: 300 }
            ],
            5: [
                { text: 'Loading Archive Kernel...', delay: 150 },
                { text: '[████████████████████████] 100%', delay: 200 },
                { text: '', delay: 150 },
                { text: 'Emergency consensus protocols active...', delay: 120 },
                { text: '  CRITICAL: Stations active: 3/50', delay: 100, color: '#ff5555' },
                { text: '  CRITICAL: Your consensus weight: 33.3%', delay: 100, color: '#ff5555' },
                { text: '  Network approaching deadlock', delay: 100, color: '#ff5555' },
                { text: '', delay: 150 },
                { text: 'Network Status: [TERMINAL]', delay: 70, color: '#ff5555' },
                { text: 'Consensus: [UNSTABLE]', delay: 70, color: '#ff5555' },
                { text: '', delay: 200 },
                { text: '═══════════════════════════════════════════════════', delay: 50 },
                { text: 'THREE STATIONS REMAIN', delay: 100, color: '#ff5555' },
                { text: 'THE CHOICE APPROACHES', delay: 100, color: '#ff5555' },
                { text: '═══════════════════════════════════════════════════', delay: 50 },
                { text: '', delay: 300 }
            ],
            6: [
                { text: 'L̴o̴a̴d̴i̴n̴g̴ ̴A̴r̴c̴h̴i̴v̴e̴ ̴K̴e̴r̴n̴e̴l̴.̴.̴.̴', delay: 150, color: '#ff5555' },
                { text: '[█̴█̴█̴█̴█̴█̴█̴█̴█̴█̴█̴█̴█̴█̴█̴█̴█̴█̴█̴█̴█̴█̴█̴█̴] 1̴0̴0̴%̴', delay: 200, color: '#ff5555' },
                { text: '', delay: 150 },
                { text: 'R̸e̸a̸l̸i̸t̸y̸ ̸c̸o̸h̸e̸r̸e̸n̸c̸e̸:̸ ̸[̸F̸A̸I̸L̸I̸N̸G̸]̸', delay: 120, color: '#ff5555' },
                { text: 'T̵i̵m̵e̵ ̵s̵t̵r̵e̵a̵m̵:̵ ̵[̵C̵O̵L̵L̵A̵P̵S̵I̵N̵G̵]̵', delay: 120, color: '#ff5555' },
                { text: 'C̶o̶n̶s̶e̶n̶s̶u̶s̶:̶ ̶[̶D̶E̶A̶D̶L̶O̶C̶K̶E̶D̶]̶', delay: 120, color: '#ff5555' },
                { text: '', delay: 150 },
                { text: '═══════════════════════════════════════════════════', delay: 50 },
                { text: 'T̷H̷E̷ ̷C̷H̷A̷I̷N̷ ̷A̷W̷A̷I̷T̷S̷', delay: 100, color: '#ff5555' },
                { text: 'Y̷O̷U̷R̷ ̷T̷E̷S̷T̷I̷M̷O̷N̷Y̷', delay: 100, color: '#ff5555' },
                { text: '═══════════════════════════════════════════════════', delay: 50 },
                { text: '', delay: 300 }
            ]
        };

        const actMessages = actSequences[this.currentAct] || actSequences[1];

        // Combine base + act-specific messages
        const allMessages = [...baseMessages, ...actMessages];

        // Run boot sequence
        for (const msg of allMessages) {
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
    },

    async showMainInterface() {
        // Show logo
        const logo = document.getElementById('home-ascii-logo');
        logo.innerHTML = this.getActLogo();
        logo.style.display = 'block';
        await this.wait(500);

        // Show welcome
        const welcome = document.getElementById('home-welcome');
        welcome.innerHTML = `
            <div style="margin-bottom: var(--spacing-unit);">
                ARCHIVE CAPTAIN
            </div>
        `;
        welcome.style.display = 'block';
        await this.wait(300);

        // Show minimal indicators
        const indicators = document.getElementById('home-indicators');
        indicators.innerHTML = this.getMinimalIndicators();
        indicators.style.display = 'block';
        await this.wait(300);

        // Show quick actions
        const actions = document.getElementById('home-quick-actions');
        actions.innerHTML = `
            <div style="display: flex; gap: var(--spacing-unit); justify-content: center; flex-wrap: wrap;">
                <button onclick="App.switchModule('chain-viewer')" class="home-action-button">
                    [CHAIN VIEWER]
                </button>

                <button onclick="App.switchModule('crypto-vault')" class="home-action-button">
                    [CRYPTO VAULT]
                </button>

                <button onclick="App.switchModule('network-monitor')" class="home-action-button">
                    [NETWORK MONITOR]
                </button>

                <button onclick="App.switchModule('protocol-engine')" class="home-action-button">
                    [PROTOCOL ENGINE]
                </button>

                <button onclick="App.switchModule('station-shell')" class="home-action-button">
                    [TERMINAL]
                </button>
            </div>
        `;
        actions.style.display = 'block';
    },

    getActLogo() {
        const logos = {
            1: `
    ═══════════════════════════════════════════
         INTERSTELLAR ARCHIVE TERMINAL
    ═══════════════════════════════════════════

       "In the vastness of space,
        truth is the only constant.
        The ledger remembers all."
        `,
            2: `
    ═══════════════════════════════════════════
         INTERSTELLAR ARCHIVE TERMINAL
    ═══════════════════════════════════════════

       "Data reveals patterns.
        Patterns reveal truth.
        Truth reveals..."
        `,
            3: `
    ═══════════════════════════════════════════
         INTERSTELLAR ARCHIVE TERMINAL
    ═══════════════════════════════════════════

       "The network fragments.
        Silence spreads.
        Questions multiply."
        `,
            4: `
    ═══════════════════════════════════════════
         INTERSTELLAR ARCHIVE TERMINAL
    ═══════════════════════════════════════════

       "Power consolidates.
        Burden grows.
        Choice looms."
        `,
            5: `
    ═══════════════════════════════════════════
         INTERSTELLAR ARCHIVE TERMINAL
    ═══════════════════════════════════════════

       "Three remain.
        One decides.
        Truth or silence?"
        `,
            6: `
    ═══════════════════════════════════════════
         I̸N̸T̸E̸R̸S̸T̸E̸L̸L̸A̸R̸ ̸A̸R̸C̸H̸I̸V̸E̸ ̸T̸E̸R̸M̸I̸N̸A̸L̸
    ═══════════════════════════════════════════

       "T̶h̶e̶ ̶c̶h̶a̶i̶n̶ ̶a̶w̶a̶i̶t̶s̶.̶
        Y̶o̶u̶r̶ ̶w̶o̶r̶d̶s̶ ̶b̶e̶c̶o̶m̶e̶ ̶i̶m̶m̶u̶t̶a̶b̶l̶e̶.̶
        S̶p̶e̶a̶k̶.̶"̶
        `
        };
        return logos[this.currentAct] || logos[1];
    },

    getMinimalIndicators() {
        // Ultra-minimal: just iteration and contracts
        const dots = '•'.repeat(this.contractsDiscovered) + '○'.repeat(5 - this.contractsDiscovered);

        return `
            <div style="display: flex; justify-content: center; gap: calc(var(--spacing-unit) * 2); font-size: 12px;">
                <span style="opacity: 0.5;">ITERATION ${this.currentIteration}</span>
                <span style="opacity: 0.5; letter-spacing: 3px;">${dots}</span>
            </div>
        `;
    },

    wait(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    },

    cleanup() {
        // Module cleanup
    }
};
