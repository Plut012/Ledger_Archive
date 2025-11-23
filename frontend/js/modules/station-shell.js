// Station Shell - Archive Terminal Interface

const StationShell = {
    currentPath: '/archive-alpha',
    commandHistory: [],
    historyIndex: -1,
    inputBuffer: '',

    // Simulated filesystem
    filesystem: {
        '/archive-alpha': {
            type: 'dir',
            contents: {
                'README.txt': {
                    type: 'file',
                    content: `╔════════════════════════════════════════════════╗
║  ARCHIVE STATION ALPHA                        ║
║  Interstellar Ledger Network                  ║
║  Terminal Access System v2.1                  ║
╠════════════════════════════════════════════════╣
║                                                ║
║  CAPTAIN NEURAL INTERFACE: ACTIVE              ║
║  SYSTEM STATUS: OPERATIONAL                    ║
║                                                ║
║  Your workstation terminal is online.          ║
║                                                ║
║  DIRECTORIES:                                  ║
║    protocols/  - Training protocols            ║
║    src/        - Archive system source         ║
║    logs/       - System logs                   ║
║                                                ║
║  Navigate to ~/protocols/ to begin memory      ║
║  restoration sequence.                         ║
║                                                ║
║  Type 'help' for available commands.           ║
║                                                ║
╚════════════════════════════════════════════════╝`
                },
                'protocols': {
                    type: 'dir',
                    contents: {
                        'README.txt': {
                            type: 'file',
                            content: `╔════════════════════════════════════════╗
║  ARCHIVE CAPTAIN TRAINING PROTOCOLS   ║
║  Neural Recovery Sequence             ║
╠════════════════════════════════════════╣
║                                        ║
║  Execute protocols to restore memory   ║
║  fragments. Order suggested but not    ║
║  required.                             ║
║                                        ║
║  SUGGESTED PATH:                       ║
║  01 → 02 → 03 → 04 → 05                ║
║                                        ║
║  Usage: source <protocol>              ║
║  Example: source 01_blocks.protocol    ║
║                                        ║
╚════════════════════════════════════════╝

AVAILABLE PROTOCOLS:

01_blocks.protocol       - Archive Blocks (Foundation)
02_mining.protocol       - Computational Locks (Security)
03_credentials.protocol  - Identity Protocols (Auth)
04_network.protocol      - Distributed Network (Resilience)
05_incident.protocol     - The Incident (Truth)`
                        },
                        '01_blocks.protocol': {
                            type: 'executable',
                            act: 1,
                            description: 'AWAKENING - Archive Blocks\nFoundation layer: Data structures, hashing, immutability'
                        },
                        '02_mining.protocol': {
                            type: 'executable',
                            act: 2,
                            description: 'THE COMPUTATIONAL LOCKS - Proof of Work\nSecurity through computational cost and mining rewards'
                        },
                        '03_credentials.protocol': {
                            type: 'executable',
                            act: 3,
                            description: 'CREDENTIALS - Identity & Signatures\nCryptographic identity, keypairs, digital signatures'
                        },
                        '04_network.protocol': {
                            type: 'executable',
                            act: 4,
                            description: 'THE RELAY STATIONS - Distributed Network\nP2P architecture, broadcast, distributed consensus'
                        },
                        '05_incident.protocol': {
                            type: 'executable',
                            act: 5,
                            description: 'TRUTH PROTOCOL - The Incident\nChain conflicts, longest chain rule, distributed truth'
                        }
                    }
                },
                'src': {
                    type: 'dir',
                    contents: {
                        'blockchain.py': { type: 'file', realPath: '/backend/blockchain.py' },
                        'block.py': { type: 'file', realPath: '/backend/block.py' },
                        'transaction.py': { type: 'file', realPath: '/backend/transaction.py' },
                        'mining.py': { type: 'file', realPath: '/backend/mining.py' },
                        'crypto.py': { type: 'file', realPath: '/backend/crypto.py' },
                        'network.py': { type: 'file', realPath: '/backend/network.py' },
                        'ledger.py': { type: 'file', realPath: '/backend/ledger.py' },
                        'constants.py': { type: 'file', realPath: '/backend/constants.py' },
                        'consensus.py': { type: 'file', realPath: '/backend/consensus.py' }
                    }
                },
                'logs': {
                    type: 'dir',
                    contents: {
                        'captain.log': {
                            type: 'file',
                            content: `[2157-03-14 08:23:41] CAPTAIN NEURAL INTERFACE: CONNECTED
[2157-03-14 08:23:42] BIOMETRIC SCAN: AUTHENTICATED
[2157-03-14 08:23:43] MEMORY FRAGMENTATION DETECTED
[2157-03-14 08:23:45] AXIOM: Initiating recovery protocols
[2157-03-14 08:23:47] SYSTEM: Archive integrity: NOMINAL
[2157-03-14 08:23:50] SYSTEM: Awaiting captain input...`
                        },
                        'system.log': {
                            type: 'file',
                            content: `[2157-03-14 08:20:15] ARCHIVE STATION ALPHA: EMERGENCY BOOT
[2157-03-14 08:20:16] CHECKING LEDGER INTEGRITY... OK
[2157-03-14 08:20:18] NETWORK STATUS: 47 NODES ONLINE
[2157-03-14 08:20:19] CONSENSUS: SYNCHRONIZED
[2157-03-14 08:20:21] PENDING TRANSACTIONS: 3
[2157-03-14 08:20:23] CAPTAIN INTERFACE: WAITING FOR SYNC
[2157-03-14 08:23:41] CAPTAIN NEURAL LINK: ESTABLISHED`
                        }
                    }
                }
            }
        }
    },

    init(container) {
        container.innerHTML = `
            <div class="station-shell">
                <div class="shell-output" id="shell-output"></div>
                <div class="shell-input-line">
                    <span class="shell-prompt" id="shell-prompt"></span>
                    <input type="text"
                           id="shell-input"
                           class="shell-input"
                           autocomplete="off"
                           autocorrect="off"
                           autocapitalize="off"
                           spellcheck="false">
                </div>
            </div>
        `;

        // Boot sequence
        this.boot();

        // Setup input handler
        const input = document.getElementById('shell-input');
        input.addEventListener('keydown', (e) => this.handleKeyDown(e));
        input.focus();

        // Refocus on click
        container.addEventListener('click', () => input.focus());

        // Update prompt
        this.updatePrompt();
    },

    async boot() {
        const output = document.getElementById('shell-output');
        output.innerHTML = '';

        // Boot sequence
        await this.print('ARCHIVE STATION ALPHA :: EMERGENCY BOOT', 'system', 20);
        await this.wait(200);
        await this.print('SYSTEM STATUS: OPERATIONAL', 'system', 20);
        await this.wait(200);
        await this.print('CAPTAIN NEURAL INTERFACE: RECONNECTING...', 'system', 20);
        await this.wait(400);
        await this.print('');
        await this.print('> AXIOM: Your workstation terminal is online.', 'axiom', 15);
        await this.wait(400);
        await this.print('> AXIOM: Navigate to ~/protocols/ to begin memory restoration.', 'axiom', 15);
        await this.wait(300);
        await this.print('');
        await this.print("Type 'help' for available commands.", 'dim');
        await this.print('');

        // Enable input
        document.getElementById('shell-input').disabled = false;
    },

    async print(text, cssClass = '', speed = 0) {
        const output = document.getElementById('shell-output');
        const line = document.createElement('div');
        line.className = `shell-line ${cssClass}`;

        if (speed > 0) {
            // Typewriter effect
            output.appendChild(line);
            for (let char of text) {
                line.textContent += char;
                output.scrollTop = output.scrollHeight;
                await this.wait(speed);
            }
        } else {
            line.textContent = text;
            output.appendChild(line);
        }

        output.scrollTop = output.scrollHeight;
    },

    wait(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    },

    updatePrompt() {
        const prompt = document.getElementById('shell-prompt');
        const shortPath = this.currentPath.replace('/archive-alpha', '~');
        prompt.textContent = `captain@archive-alpha:${shortPath}$ `;
    },

    handleKeyDown(e) {
        const input = e.target;

        if (e.key === 'Enter') {
            const command = input.value.trim();
            if (command) {
                this.commandHistory.push(command);
                this.historyIndex = this.commandHistory.length;
                this.executeCommand(command);
            } else {
                this.print('');
                this.updatePrompt();
            }
            input.value = '';
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            if (this.historyIndex > 0) {
                this.historyIndex--;
                input.value = this.commandHistory[this.historyIndex];
            }
        } else if (e.key === 'ArrowDown') {
            e.preventDefault();
            if (this.historyIndex < this.commandHistory.length - 1) {
                this.historyIndex++;
                input.value = this.commandHistory[this.historyIndex];
            } else {
                this.historyIndex = this.commandHistory.length;
                input.value = '';
            }
        } else if (e.key === 'Tab') {
            e.preventDefault();
            this.handleTabCompletion(input);
        }
    },

    async executeCommand(cmd) {
        // Echo command
        const shortPath = this.currentPath.replace('/archive-alpha', '~');
        await this.print(`captain@archive-alpha:${shortPath}$ ${cmd}`, 'echo');

        const parts = cmd.trim().split(/\s+/);
        const command = parts[0];
        const args = parts.slice(1);

        switch (command) {
            case 'ls':
                this.cmdLs(args);
                break;
            case 'cd':
                this.cmdCd(args[0] || '~');
                break;
            case 'pwd':
                this.cmdPwd();
                break;
            case 'cat':
                await this.cmdCat(args[0]);
                break;
            case 'source':
            case '.':
                await this.cmdSource(args[0]);
                break;
            case 'clear':
                this.cmdClear();
                break;
            case 'help':
                this.cmdHelp();
                break;
            case 'tree':
                this.cmdTree();
                break;
            default:
                if (cmd.startsWith('./')) {
                    await this.cmdSource(cmd.substring(2));
                } else {
                    await this.print(`command not found: ${command}`);
                }
        }

        await this.print('');
    },

    resolvePath(path) {
        if (!path) return this.currentPath;

        if (path === '~') return '/archive-alpha';
        if (path === '..') {
            const parts = this.currentPath.split('/').filter(p => p);
            parts.pop();
            return '/' + parts.join('/');
        }
        if (path === '.') return this.currentPath;
        if (path.startsWith('/')) return path;
        if (path.startsWith('~/')) return '/archive-alpha/' + path.substring(2);

        return this.currentPath + '/' + path;
    },

    getNode(path) {
        const parts = path.split('/').filter(p => p);
        let node = this.filesystem['/archive-alpha'];

        for (let part of parts.slice(1)) { // Skip 'archive-alpha'
            if (node.type !== 'dir' || !node.contents[part]) {
                return null;
            }
            node = node.contents[part];
        }

        return node;
    },

    cmdLs(args) {
        const path = this.resolvePath(args[0]);
        const node = this.getNode(path);

        if (!node) {
            this.print(`ls: cannot access '${args[0]}': No such file or directory`);
            return;
        }

        if (node.type === 'file') {
            this.print(args[0] || path.split('/').pop());
            return;
        }

        const entries = Object.keys(node.contents).sort();
        for (let entry of entries) {
            const item = node.contents[entry];
            let display = entry;

            if (item.type === 'dir') {
                display = entry + '/';
                this.print(display, 'dir');
            } else if (item.type === 'executable') {
                display = entry;
                this.print(display, 'executable');
            } else {
                this.print(display);
            }
        }
    },

    cmdCd(path) {
        const resolved = this.resolvePath(path);
        const node = this.getNode(resolved);

        if (!node) {
            this.print(`cd: ${path}: No such file or directory`);
            return;
        }

        if (node.type !== 'dir') {
            this.print(`cd: ${path}: Not a directory`);
            return;
        }

        this.currentPath = resolved;
        this.updatePrompt();
    },

    cmdPwd() {
        this.print(this.currentPath);
    },

    async cmdCat(filename) {
        if (!filename) {
            this.print('cat: missing file operand');
            return;
        }

        const path = this.resolvePath(filename);
        const node = this.getNode(path);

        if (!node) {
            this.print(`cat: ${filename}: No such file or directory`);
            return;
        }

        if (node.type === 'dir') {
            this.print(`cat: ${filename}: Is a directory`);
            return;
        }

        if (node.type === 'executable') {
            await this.print(node.description);
            await this.print('');
            await this.print(`Execute with: source ${filename}`);
            return;
        }

        // Regular file
        if (node.content) {
            await this.print(node.content);
        } else if (node.realPath) {
            // Fetch actual source code
            await this.fetchAndDisplay(node.realPath);
        }
    },

    async fetchAndDisplay(realPath) {
        try {
            const response = await fetch(realPath);
            if (response.ok) {
                const content = await response.text();
                const lines = content.split('\n');

                // Display with line numbers
                for (let i = 0; i < lines.length; i++) {
                    const lineNum = String(i + 1).padStart(4, ' ');
                    await this.print(`${lineNum} │ ${lines[i]}`, 'code');
                }
            } else {
                await this.print(`Error: Could not fetch file`);
            }
        } catch (e) {
            await this.print(`Error reading file: ${e.message}`);
        }
    },

    async cmdSource(filename) {
        if (!filename) {
            this.print('source: missing file operand');
            return;
        }

        const path = this.resolvePath(filename);
        const node = this.getNode(path);

        if (!node) {
            this.print(`source: ${filename}: No such file or directory`);
            return;
        }

        if (node.type !== 'executable') {
            this.print(`source: ${filename}: Not an executable protocol`);
            return;
        }

        // Execute protocol
        await this.print(`> Loading memory fragment: ${node.description.split('\n')[0].split(' - ')[1]}`);
        await this.print(`> Initiating neural restoration sequence...`);
        await this.print('');
        await this.wait(1000);

        // Trigger the act in Learning Guide
        LearningGuide.playAct(node.act);
    },

    cmdClear() {
        document.getElementById('shell-output').innerHTML = '';
    },

    cmdHelp() {
        this.print('Available commands:');
        this.print('');
        this.print('  ls [path]           - list directory contents');
        this.print('  cd <path>           - change directory');
        this.print('  pwd                 - print working directory');
        this.print('  cat <file>          - display file contents');
        this.print('  source <protocol>   - execute training protocol');
        this.print('  . <protocol>        - execute training protocol (alias)');
        this.print('  clear               - clear terminal');
        this.print('  help                - show this help');
        this.print('  tree                - show directory tree');
        this.print('');
        this.print('Special paths:');
        this.print('  ~                   - home directory (/archive-alpha)');
        this.print('  ..                  - parent directory');
        this.print('  .                   - current directory (when used alone)');
        this.print('');
        this.print('Tips:');
        this.print('  - Press TAB to autocomplete filenames');
        this.print('  - Press UP/DOWN to navigate command history');
    },

    cmdTree() {
        this.print('/archive-alpha');
        this.print('├── README.txt');
        this.print('├── protocols/');
        this.print('│   ├── README.txt');
        this.print('│   ├── 01_blocks.protocol');
        this.print('│   ├── 02_mining.protocol');
        this.print('│   ├── 03_credentials.protocol');
        this.print('│   ├── 04_network.protocol');
        this.print('│   └── 05_incident.protocol');
        this.print('├── src/');
        this.print('│   ├── blockchain.py');
        this.print('│   ├── block.py');
        this.print('│   ├── transaction.py');
        this.print('│   ├── mining.py');
        this.print('│   ├── crypto.py');
        this.print('│   ├── network.py');
        this.print('│   ├── ledger.py');
        this.print('│   ├── constants.py');
        this.print('│   └── consensus.py');
        this.print('└── logs/');
        this.print('    ├── captain.log');
        this.print('    └── system.log');
    },

    handleTabCompletion(input) {
        const value = input.value;
        const parts = value.split(' ');
        const lastPart = parts[parts.length - 1];

        // Get current directory contents
        const node = this.getNode(this.currentPath);
        if (!node || node.type !== 'dir') return;

        const entries = Object.keys(node.contents);

        // Find matches
        const matches = entries.filter(entry => entry.startsWith(lastPart));

        if (matches.length === 0) {
            // No matches, do nothing
            return;
        } else if (matches.length === 1) {
            // Single match - complete it
            const match = matches[0];
            const matchNode = node.contents[match];

            // Add trailing slash for directories
            const completion = matchNode.type === 'dir' ? match + '/' : match;

            // Replace last part with completion
            parts[parts.length - 1] = completion;
            input.value = parts.join(' ');
        } else {
            // Multiple matches - show them
            this.print('');
            const shortPath = this.currentPath.replace('/archive-alpha', '~');
            this.print(`captain@archive-alpha:${shortPath}$ ${value}`, 'echo');

            // Display matches in columns
            let line = '';
            matches.forEach((match, index) => {
                const matchNode = node.contents[match];
                const display = matchNode.type === 'dir' ? match + '/' : match;
                line += display.padEnd(25);

                if ((index + 1) % 3 === 0) {
                    this.print(line);
                    line = '';
                }
            });
            if (line) this.print(line);

            // Find common prefix
            let commonPrefix = matches[0];
            for (let match of matches) {
                while (!match.startsWith(commonPrefix)) {
                    commonPrefix = commonPrefix.slice(0, -1);
                }
            }

            // Complete to common prefix
            if (commonPrefix.length > lastPart.length) {
                parts[parts.length - 1] = commonPrefix;
                input.value = parts.join(' ');
            }

            this.print('');
        }
    },

    cleanup() {
        // Clean up event listeners
        document.removeEventListener('keydown', this.handleKeyDown);
    }
};
