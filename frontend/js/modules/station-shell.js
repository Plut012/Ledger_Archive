// Station Shell - Enhanced with Backend Filesystem Integration

const StationShell = {
    currentPath: '~',
    commandHistory: [],
    historyIndex: -1,
    stateManager: null,

    init(container, stateManager = null) {
        this.stateManager = stateManager;

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
        await this.print('[INITIALIZING STATION SHELL...]', 'system', 20);
        await this.wait(200);
        await this.print('[FILESYSTEM: MOUNTED]', 'system', 20);
        await this.wait(200);
        await this.print('[NEURAL INTERFACE: CONNECTED]', 'system', 20);
        await this.wait(400);
        await this.print('');
        await this.print("Welcome to LEDGER-ARCHIVE-7 Station Shell", 'dim');
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
        prompt.textContent = `[${this.currentPath}]$ `;
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
            // Tab completion can be added later
        }
    },

    async executeCommand(cmd) {
        // Echo command
        await this.print(`$ ${cmd}`, 'echo');

        // Check for special frontend-only commands
        if (cmd === 'clear' || cmd === '[CLEAR]') {
            this.cmdClear();
            return;
        }

        try {
            // Send command to backend
            const response = await fetch('/api/shell/command', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    command: cmd,
                    playerId: this.stateManager?.playerId || 'default'
                })
            });

            if (!response.ok) {
                const error = await response.json();
                await this.print(`Error: ${error.error || 'Command execution failed'}`, 'error');
                await this.print('');
                return;
            }

            const result = await response.json();

            // Handle special commands
            if (result.output === '[CLEAR]') {
                this.cmdClear();
                return;
            }

            // Handle module navigation
            if (result.output?.startsWith('[NAVIGATE:')) {
                const module = result.output.match(/\[NAVIGATE:(\w+)\]/)[1];
                this.navigateToModule(module);
                return;
            }

            // Display output
            if (result.output) {
                const lines = result.output.split('\n');
                for (const line of lines) {
                    await this.print(line);
                }
            }

            // Update current path
            if (result.cwd) {
                this.currentPath = result.cwd;
                this.updatePrompt();
            }

            // Update state manager if available
            if (this.stateManager && result.narrativeState) {
                // Update local state reference
                if (this.stateManager.state) {
                    Object.assign(this.stateManager.state.session, result.narrativeState);
                }

                // Show warnings if suspicion is high
                if (result.narrativeState.archivistSuspicion > 70) {
                    await this.print('');
                    await this.print('[WARNING: ELEVATED MONITORING DETECTED]', 'warning');
                }

                // Show log mask status
                if (result.narrativeState.logMaskActive) {
                    await this.print('[LOG MASKING: ACTIVE]', 'success');
                }
            }

            await this.print('');

        } catch (error) {
            console.error('Command execution error:', error);
            await this.print(`Error: ${error.message}`, 'error');
            await this.print('');
        }
    },

    cmdClear() {
        document.getElementById('shell-output').innerHTML = '';
    },

    navigateToModule(moduleName) {
        // Trigger module navigation
        const navItem = document.querySelector(`[data-module="${moduleName}"]`);
        if (navItem) {
            navItem.click();
        } else {
            this.print(`Module '${moduleName}' not found`);
        }
    },

    cleanup() {
        // Clean up event listeners if needed
    }
};
