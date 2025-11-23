// Main application initialization

// Global state for tutorial validation
window.selectedBlockIndex = null;
window.lastMinedBlock = null;
window.walletAddress = null;
window.lastBroadcastPaths = null;
window.blockTampered = false;

const App = {
    currentModule: null,
    currentModuleName: null,
    ws: null,

    init() {
        console.log('Initializing Interstellar Archive Terminal...');

        // Initialize WebSocket connection
        this.ws = WebSocketClient.init();

        // Setup navigation
        this.setupNavigation();

        // Setup console
        this.setupConsole();

        // Setup footer buttons
        this.setupFooter();

        // Setup transmission modal
        this.setupTransmissionModal();

        // Load initial module
        this.loadModule('station-shell');

        // Show incoming transmission after brief delay
        setTimeout(() => this.showTransmission(), 1000);

        // Update time display
        this.updateStationTime();
        setInterval(() => this.updateStationTime(), 1000);
    },

    setupNavigation() {
        const navItems = document.querySelectorAll('.nav-item');
        navItems.forEach(item => {
            item.addEventListener('click', (e) => {
                const moduleName = e.currentTarget.dataset.module;
                this.loadModule(moduleName);

                // Update active state
                navItems.forEach(i => i.classList.remove('active'));
                e.currentTarget.classList.add('active');
            });
        });
    },

    setupConsole() {
        const input = document.getElementById('command-input');
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const command = input.value.trim();
                if (command) {
                    this.executeCommand(command);
                    input.value = '';
                }
            }
        });
    },

    setupFooter() {
        document.getElementById('btn-help').addEventListener('click', () => {
            this.showHelp();
        });

        document.getElementById('btn-clear').addEventListener('click', () => {
            document.getElementById('console-output').innerHTML = '';
        });

        document.getElementById('btn-reset').addEventListener('click', () => {
            if (confirm('Reset blockchain to genesis block?')) {
                this.resetBlockchain();
            }
        });
    },

    loadModule(moduleName) {
        const container = document.getElementById('module-container');

        // Cleanup current module
        if (this.currentModule && this.currentModule.cleanup) {
            this.currentModule.cleanup();
        }

        // Load new module
        const modules = {
            'station-shell': StationShell,
            'home': Home,
            'chain-viewer': ChainViewer,
            'network-monitor': NetworkMonitor,
            'crypto-vault': CryptoVault,
            'learning-guide': LearningGuide,
            'protocol-engine': ProtocolEngine,
            'econ-simulator': EconSimulator
        };

        this.currentModule = modules[moduleName];
        this.currentModuleName = moduleName;
        if (this.currentModule) {
            this.currentModule.init(container);
        }
    },

    // Method for tutorial to switch modules programmatically
    switchModule(moduleName) {
        // Find and click the nav item
        const navItem = document.querySelector(`.nav-item[data-module="${moduleName}"]`);
        if (navItem) {
            navItem.click();
        }
    },

    setupTransmissionModal() {
        const yesBtn = document.getElementById('btn-rebirth-yes');
        const noBtn = document.getElementById('btn-rebirth-no');

        yesBtn.addEventListener('click', () => {
            this.hideTransmission();
            this.log('> REBIRTH PROTOCOL INITIATED');
            this.log('> Accessing Archive Captain training module...');
            setTimeout(() => {
                if (LearningGuide && LearningGuide.startProtocol) {
                    LearningGuide.startProtocol();
                }
            }, 500);
        });

        noBtn.addEventListener('click', () => {
            this.hideTransmission();
            this.log('> TRANSMISSION ACKNOWLEDGED');
            this.log('> Resuming standard operations...');
            this.log('> Archive Station Alpha online');
            this.log('> All systems nominal');
        });
    },

    showTransmission() {
        const modal = document.getElementById('transmission-modal');
        if (modal) {
            modal.style.display = 'flex';
            // Alert sound for incoming transmission
            if (typeof AudioSystem !== 'undefined') {
                AudioSystem.sounds.alert();
            }
        }
    },

    hideTransmission() {
        const modal = document.getElementById('transmission-modal');
        if (modal) {
            modal.style.display = 'none';
        }
    },

    executeCommand(command) {
        this.log(`> ${command}`);

        // Simple command parser
        const parts = command.toLowerCase().split(' ');
        const cmd = parts[0];
        const args = parts.slice(1);

        switch (cmd) {
            case 'help':
                this.showHelp();
                break;
            case 'clear':
            case 'cls':
                document.getElementById('console-output').innerHTML = '';
                break;
            case 'status':
                this.showStatus();
                break;
            case 'yes':
            case 'y':
                this.log('Initiating Archive Captain Protocol...');
                this.log('Switching to Learning Guide module...');
                setTimeout(() => {
                    this.loadModule('learning-guide');
                    const navItem = document.querySelector('.nav-item[data-module="learning-guide"]');
                    if (!navItem) {
                        // If learning guide nav item doesn't exist, start protocol directly
                        if (LearningGuide && LearningGuide.startProtocol) {
                            LearningGuide.startProtocol();
                        }
                    }
                }, 500);
                break;
            case 'no':
            case 'n':
                this.log('Acknowledged. Proceeding with standard operations.');
                this.log('The archive is under your protection, Captain.');
                this.log('');
                this.log('Type "help" to see available commands.');
                break;
            case 'ls':
                this.listModules();
                break;
            case 'pwd':
                this.log('/archive/station-alpha/terminal');
                break;
            case 'whoami':
                this.log('archive-captain');
                break;
            case 'date':
                const now = new Date();
                this.log(`Stardate: ${now.toISOString()}`);
                break;
            case 'echo':
                this.log(args.join(' '));
                break;
            case 'tutorial':
                this.log('Starting Archive Captain Protocol...');
                if (LearningGuide && LearningGuide.startProtocol) {
                    LearningGuide.startProtocol();
                }
                break;
            default:
                this.log(`Command not found: ${cmd}`);
                this.log(`Type "help" for available commands.`);
        }
    },

    listModules() {
        this.log('Available modules:');
        this.log('  chain-viewer     - View blockchain data');
        this.log('  network-monitor  - Monitor network nodes');
        this.log('  crypto-vault     - Cryptographic operations');
        this.log('  protocol-engine  - Protocol specifications');
        this.log('  econ-simulator   - Economic simulations');
        this.log('');
        this.log('Use navigation panel to switch modules.');
    },

    showHelp() {
        this.log('═══════════════════════════════════════');
        this.log('IMPERIUM TERMINAL - COMMAND REFERENCE');
        this.log('═══════════════════════════════════════');
        this.log('');
        this.log('Archive Commands:');
        this.log('  status     - Show blockchain status');
        this.log('  tutorial   - Start Archive Captain Protocol');
        this.log('');
        this.log('System Commands:');
        this.log('  help       - Show this help message');
        this.log('  clear/cls  - Clear terminal output');
        this.log('  ls         - List available modules');
        this.log('  pwd        - Print working directory');
        this.log('  whoami     - Display current user');
        this.log('  date       - Show current stardate');
        this.log('  echo <msg> - Display a message');
        this.log('');
        this.log('Navigation:');
        this.log('  Use left panel to switch between modules');
        this.log('═══════════════════════════════════════');
    },

    showStatus() {
        fetch('/api/state')
            .then(r => r.json())
            .then(data => {
                this.log(`Chain Height: ${data.height}`);
                this.log(`Pending TX: ${data.pending_transactions}`);
                this.log(`Valid: ${data.is_valid ? 'YES' : 'NO'}`);
            })
            .catch(err => this.log(`Error: ${err.message}`));
    },

    resetBlockchain() {
        // TODO: Implement reset endpoint
        this.log('Reset not yet implemented');
    },

    log(message, color = null) {
        const output = document.getElementById('console-output');
        const line = document.createElement('div');
        line.textContent = message;
        if (color) line.style.color = color;
        output.appendChild(line);
        output.scrollTop = output.scrollHeight;
        return line;
    },

    logHighlight(message) {
        return this.log(message, 'var(--color-highlight)');
    },

    logSystem(message) {
        return this.log(message, 'var(--color-dim)');
    },

    logAccent(message) {
        return this.log(message, 'var(--color-accent)');
    },

    async logTypewriter(message, speed = 30, color = null) {
        const output = document.getElementById('console-output');
        const line = document.createElement('div');
        if (color) line.style.color = color;
        output.appendChild(line);

        for (let i = 0; i < message.length; i++) {
            line.textContent = message.substring(0, i + 1) + '_';
            output.scrollTop = output.scrollHeight;

            // Subtle typing sound every few characters
            if (Math.random() > 0.7 && typeof AudioSystem !== 'undefined') {
                AudioSystem.sounds.type();
            }

            await this.wait(speed);
        }

        line.textContent = message;
        output.scrollTop = output.scrollHeight;
        return line;
    },

    wait(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    },

    updateStationTime() {
        const now = new Date();
        const year = 2347;
        const dayOfYear = Math.floor((now - new Date(now.getFullYear(), 0, 0)) / 1000 / 60 / 60 / 24);
        const time = now.toTimeString().split(' ')[0];
        document.getElementById('station-time').textContent = `${year}:${dayOfYear}:${time}`;
    }
};

// Expose App globally for tutorial integration
window.App = App;

// Start the application when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    App.init();
});
