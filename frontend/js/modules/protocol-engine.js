/**
 * Protocol Engine Module - Smart Contract Viewer
 *
 * Displays smart contracts with syntax highlighting and execution capabilities.
 * Contracts unlock based on game progression and tell the story through code.
 */

const ProtocolEngine = {
    container: null,
    currentContract: null,
    contracts: [],

    async init(container) {
        this.container = container;
        await this.loadContracts();
        this.render();
    },

    async loadContracts() {
        try {
            const response = await fetch('/api/contracts/list?player_id=default');
            const data = await response.json();

            if (data.status === 'success') {
                this.contracts = data.contracts;
            }
        } catch (error) {
            console.error('Failed to load contracts:', error);
        }
    },

    render() {
        if (!this.currentContract) {
            this.renderContractList();
        } else {
            this.renderContractView();
        }
    },

    renderContractList() {
        const unlocked = this.contracts.filter(c => c.unlocked);
        const locked = this.contracts.filter(c => !c.unlocked);

        this.container.innerHTML = `
            <div class="module-header">PROTOCOL EXECUTION ENGINE</div>

            <div class="protocol-intro">
                <div class="protocol-description">
                    Smart contracts govern the Archive Station Network.
                    These protocols control consensus, consciousness reconstruction,
                    and network operations.
                </div>
            </div>

            <div class="contracts-section">
                <div class="section-header">
                    <span class="section-title">Available Contracts</span>
                    <span class="section-count">${unlocked.length}/${this.contracts.length} Unlocked</span>
                </div>

                ${unlocked.length > 0 ? `
                    <div class="contract-list">
                        ${unlocked.map(contract => this.renderContractCard(contract)).join('')}
                    </div>
                ` : `
                    <div class="no-contracts">
                        No contracts unlocked yet. Progress through the story to discover protocols.
                    </div>
                `}
            </div>

            ${locked.length > 0 ? `
                <div class="contracts-section">
                    <div class="section-header">
                        <span class="section-title">Locked Contracts</span>
                        <span class="section-count">${locked.length}</span>
                    </div>
                    <div class="contract-list locked">
                        ${locked.map(contract => this.renderLockedCard(contract)).join('')}
                    </div>
                </div>
            ` : ''}
        `;

        // Attach click handlers
        this.container.querySelectorAll('.contract-card:not(.locked-card)').forEach(card => {
            card.addEventListener('click', () => {
                const contractId = card.dataset.contractId;
                this.viewContract(contractId);
            });
        });
    },

    renderContractCard(contract) {
        return `
            <div class="contract-card" data-contract-id="${contract.id}">
                <div class="contract-card-header">
                    <div class="contract-name">${contract.name}</div>
                    <div class="contract-version">v${contract.version}</div>
                </div>
                <div class="contract-author">by ${contract.author}</div>
                <div class="contract-description">${contract.description}</div>
                <div class="contract-footer">
                    <span class="contract-act">Act ${contract.discovered_act}</span>
                    <span class="contract-action">View Code →</span>
                </div>
            </div>
        `;
    },

    renderLockedCard(contract) {
        return `
            <div class="contract-card locked-card">
                <div class="contract-card-header">
                    <div class="contract-name">[LOCKED]</div>
                    <div class="contract-version">v?.?.?</div>
                </div>
                <div class="contract-author">Unknown Author</div>
                <div class="contract-description encrypted">
                    ${this.encryptText(contract.description)}
                </div>
                <div class="contract-footer">
                    <span class="contract-unlock-hint">${this.getUnlockHint(contract.unlock_condition)}</span>
                </div>
            </div>
        `;
    },

    encryptText(text) {
        // Simple "encrypted" appearance
        return text.split('').map(c =>
            c === ' ' ? ' ' : String.fromCharCode(0x2591 + Math.floor(Math.random() * 3))
        ).join('');
    },

    getUnlockHint(condition) {
        if (condition.includes('witness_trust')) {
            return 'Unlock: Gain Witness trust';
        } else if (condition.includes('archivist_suspicion')) {
            return 'Unlock: Raise ARCHIVIST suspicion';
        } else if (condition.includes('current_act')) {
            const act = condition.match(/\d+/)?.[0];
            return `Unlock: Reach Act ${act}`;
        } else if (condition === 'special_unlock') {
            return 'Unlock: ???';
        }
        return 'Locked';
    },

    async viewContract(contractId) {
        try {
            const response = await fetch(`/api/contracts/${contractId}?player_id=default`);
            const data = await response.json();

            if (data.status === 'success') {
                this.currentContract = data.contract;
                this.render();

                if (data.suspicion_increased > 0) {
                    this.showSuspicionWarning(data.suspicion_increased);
                }
            } else {
                alert(`Error: ${data.error}`);
            }
        } catch (error) {
            console.error('Failed to load contract:', error);
        }
    },

    renderContractView() {
        const contract = this.currentContract;

        this.container.innerHTML = `
            <div class="module-header">
                <button class="back-button" id="backToList">← Back to Contracts</button>
                PROTOCOL EXECUTION ENGINE
            </div>

            <div class="contract-viewer">
                <div class="contract-header-info">
                    <div class="contract-title-row">
                        <h2 class="contract-title">${contract.name}</h2>
                        <span class="contract-version-badge">v${contract.version}</span>
                    </div>
                    <div class="contract-metadata">
                        <span class="contract-author-label">Author:</span>
                        <span class="contract-author-value">${contract.author}</span>
                    </div>
                    <div class="contract-description-full">${contract.description}</div>
                </div>

                <div class="contract-code-section">
                    <div class="code-header">
                        <span class="code-label">Contract Source Code</span>
                        <span class="code-language">Solidity</span>
                    </div>
                    <div class="contract-code">
                        ${this.syntaxHighlight(contract.code)}
                    </div>
                </div>

                ${contract.execution_notes ? `
                    <div class="contract-notes">
                        <div class="notes-header">⚠️ Execution Notes</div>
                        <div class="notes-content">${contract.execution_notes}</div>
                    </div>
                ` : ''}

                ${this.renderExecutionInterface(contract)}
            </div>
        `;

        // Attach event listeners
        document.getElementById('backToList').addEventListener('click', () => {
            this.currentContract = null;
            this.render();
        });
    },

    syntaxHighlight(code) {
        // Simple syntax highlighting for Solidity-like code
        let highlighted = code;

        // Keywords
        const keywords = [
            'pragma', 'solidity', 'contract', 'function', 'returns', 'return',
            'public', 'private', 'internal', 'view', 'pure', 'memory', 'storage',
            'if', 'else', 'for', 'while', 'require', 'emit', 'event',
            'mapping', 'struct', 'uint256', 'bytes32', 'bytes', 'string', 'address', 'bool'
        ];

        keywords.forEach(keyword => {
            const regex = new RegExp(`\\b(${keyword})\\b`, 'g');
            highlighted = highlighted.replace(regex, '<span class="keyword">$1</span>');
        });

        // Comments
        highlighted = highlighted.replace(
            /(\/\/.*?)(\n|$)/g,
            '<span class="comment">$1</span>$2'
        );
        highlighted = highlighted.replace(
            /(\/\*[\s\S]*?\*\/)/g,
            '<span class="comment">$1</span>'
        );

        // Strings
        highlighted = highlighted.replace(
            /(".*?")/g,
            '<span class="string">$1</span>'
        );

        // Function names
        highlighted = highlighted.replace(
            /\b(function)\s+(\w+)/g,
            '<span class="keyword">$1</span> <span class="function-name">$2</span>'
        );

        // Contract/struct/event names (after keyword)
        highlighted = highlighted.replace(
            /\b(contract|struct|event)\s+(\w+)/g,
            '<span class="keyword">$1</span> <span class="type-name">$2</span>'
        );

        // Numbers
        highlighted = highlighted.replace(
            /\b(\d+)\b/g,
            '<span class="number">$1</span>'
        );

        return `<pre><code>${highlighted}</code></pre>`;
    },

    renderExecutionInterface(contract) {
        // Special cases for contracts that can be executed
        if (contract.id === 'testimony_broadcast') {
            return `
                <div class="execution-interface">
                    <div class="execution-header">Deploy Testimony</div>
                    <div class="execution-description">
                        Write your final testimony to be permanently recorded on the blockchain.
                        This is your Act VI choice - it cannot be undone.
                    </div>
                    <textarea
                        id="testimonyInput"
                        class="testimony-input"
                        placeholder="Write your testimony here...&#10;&#10;What will you tell the other captains?&#10;What truth will you reveal?"></textarea>
                    <button id="deployTestimony" class="deploy-button">Deploy Contract</button>
                    <div id="deploymentResult" class="deployment-result"></div>
                </div>
            `;
        } else {
            return `
                <div class="execution-interface">
                    <div class="execution-header">Contract Information</div>
                    <div class="execution-description">
                        This contract is active on the network and executes automatically.
                        No manual execution required.
                    </div>
                </div>
            `;
        }
    },

    showSuspicionWarning(amount) {
        const warning = document.createElement('div');
        warning.className = 'suspicion-warning';
        warning.textContent = `⚠️ ARCHIVIST suspicion increased by ${amount}`;
        this.container.prepend(warning);

        setTimeout(() => warning.remove(), 3000);
    },

    async deployTestimony() {
        const textarea = document.getElementById('testimonyInput');
        const testimony = textarea.value.trim();

        if (!testimony) {
            alert('Please write your testimony before deploying.');
            return;
        }

        if (!confirm('Are you sure? Your testimony will be permanent and immutable once deployed.')) {
            return;
        }

        // Play reconstruction/deployment sound
        AudioManager.play('reconstruction');

        try {
            const response = await fetch('/api/contracts/deploy', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    playerId: 'default',
                    testimony: testimony
                })
            });

            const data = await response.json();
            const resultDiv = document.getElementById('deploymentResult');

            if (data.status === 'success') {
                // Play final choice sound on successful deployment (this is the Act VI climax)
                AudioManager.play('finalChoice');

                resultDiv.className = 'deployment-result success';
                resultDiv.innerHTML = `
                    <div class="result-header">✓ Testimony Deployed Successfully</div>
                    <div class="result-details">
                        ${data.deployment.output.message.replace(/\n/g, '<br>')}
                    </div>
                    <div class="result-hash">
                        Content Hash: ${data.deployment.output.contentHash}
                    </div>
                    <div class="result-immutable">
                        This testimony is now permanent on the blockchain.
                    </div>
                `;
                textarea.disabled = true;
                document.getElementById('deployTestimony').disabled = true;
            } else {
                resultDiv.className = 'deployment-result error';
                resultDiv.innerHTML = `
                    <div class="result-header">✗ Deployment Failed</div>
                    <div class="result-details">${data.error}</div>
                `;
            }
        } catch (error) {
            console.error('Deployment failed:', error);
            alert('Deployment failed. Please try again.');
        }
    },

    cleanup() {
        this.currentContract = null;
        this.contracts = [];
    }
};

// Handle testimony deployment clicks
document.addEventListener('click', (e) => {
    if (e.target.id === 'deployTestimony') {
        ProtocolEngine.deployTestimony();
    }
});
