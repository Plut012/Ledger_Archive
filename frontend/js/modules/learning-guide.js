// Archive Captain Protocol - Narrative Learning Guide

const LearningGuide = {
    currentAct: 0,
    currentLine: 0,
    isTyping: false,
    typewriterSpeed: 30,
    tutorialActive: false,
    playerProgress: {},
    lastSpeaker: null,  // Track last speaker for message grouping

    // Act definitions
    acts: {
        1: {
            title: "AWAKENING",
            memoryFragment: "Archive Blocks",

            dialogue: [
                {
                    speaker: "SYSTEM",
                    text: "ARCHIVE STATION ALPHA :: EMERGENCY BOOT",
                    speed: 20,
                    pause: 1000
                },
                {
                    speaker: "SYSTEM",
                    text: "SYSTEM STATUS: CRITICAL",
                    speed: 20,
                    pause: 800
                },
                {
                    speaker: "SYSTEM",
                    text: "CAPTAIN NEURAL INTERFACE: RECONNECTING...",
                    speed: 20,
                    pause: 1500
                },
                {
                    speaker: "AXIOM",
                    text: "Captain... can you hear me?",
                    speed: 30,
                    pause: 1500
                },
                {
                    speaker: "AXIOM",
                    text: "I'm AXIOM - your Archive Intelligence. Your biometrics show memory fragmentation.",
                    speed: 30,
                    pause: 2000
                },
                {
                    speaker: "AXIOM",
                    text: "You are the Archive Captain. Humanity's permanent ledger is under your protection.",
                    speed: 30,
                    pause: 1500
                },
                {
                    speaker: "AXIOM",
                    text: "But something went wrong during the last shift...",
                    speed: 30,
                    pause: 1500
                },
                {
                    speaker: "AXIOM",
                    text: "We need to verify the archive's integrity. I'll guide you through the protocols.",
                    speed: 30,
                    pause: 1500
                },
                {
                    speaker: "AXIOM",
                    text: "Let's begin with the fundamentals...",
                    speed: 30,
                    pause: 1000
                }
            ],

            interactions: [
                {
                    instruction: "Open the Chain Viewer module",
                    targetModule: "chain-viewer",
                    onComplete: "Good. Your motor functions are intact."
                },
                {
                    instruction: "Examine the genesis block (Block #0)",
                    action: "inspect-block",
                    validate: () => window.selectedBlockIndex === 0,
                    onComplete: "Yes. This is where it all began. The first block in humanity's permanent archive."
                }
            ],

            teachingPoints: [
                {
                    speaker: "AXIOM",
                    text: "Do you see the hash field? That's like a fingerprint. Unique. Impossible to forge.",
                    speed: 30,
                    pause: 2000
                },
                {
                    speaker: "AXIOM",
                    text: "Every block contains: the data we're protecting, a timestamp, and the hash of the previous block.",
                    speed: 30,
                    pause: 2000
                },
                {
                    speaker: "AXIOM",
                    text: "This creates a chain. Each block cryptographically linked to the one before it.",
                    speed: 30,
                    pause: 1500
                },
                {
                    speaker: "AXIOM",
                    text: "If anyone tries to alter the past... the hash changes. The chain breaks.",
                    speed: 30,
                    pause: 1500
                }
            ],

            tamperDemo: [
                {
                    speaker: "AXIOM",
                    text: "Let me show you.",
                    speed: 30,
                    pause: 1500
                },
                {
                    action: "axiom-select-block",
                    blockIndex: 1
                },
                {
                    speaker: "AXIOM",
                    text: "Block #1. Sealed and recorded.",
                    speed: 30,
                    pause: 1500
                },
                {
                    speaker: "AXIOM",
                    text: "Watch the hash field. This is its fingerprint.",
                    speed: 30,
                    pause: 2000
                },
                {
                    speaker: "AXIOM",
                    text: "Now I'm going to alter the timestamp.",
                    speed: 30,
                    pause: 1500
                },
                {
                    action: "axiom-tamper-block",
                    pause: 500
                },
                {
                    speaker: "AXIOM",
                    text: "Look. The fingerprint changed instantly.",
                    speed: 30,
                    pause: 2000
                },
                {
                    speaker: "AXIOM",
                    text: "The previous block's hash remains the same. But this block's hash is now different.",
                    speed: 30,
                    pause: 2000
                },
                {
                    speaker: "AXIOM",
                    text: "The chain is broken. The deception is immediately visible.",
                    speed: 30,
                    pause: 2000
                },
                {
                    action: "axiom-restore-block",
                    pause: 500
                },
                {
                    speaker: "AXIOM",
                    text: "Even when restored to the original... the system remembers.",
                    speed: 30,
                    pause: 1500
                },
                {
                    speaker: "AXIOM",
                    text: "This is immutability, Captain. The archive cannot be rewritten without detection.",
                    speed: 30,
                    pause: 2000
                }
            ],

            completion: {
                speaker: "AXIOM",
                text: "Memory fragment restored: Archive Blocks. Your understanding is returning...",
                speed: 30,
                pause: 2000
            }
        },

        2: {
            title: "THE COMPUTATIONAL LOCKS",
            memoryFragment: "Proof of Work",

            dialogue: [
                {
                    speaker: "AXIOM",
                    text: "Your neural patterns are stabilizing. Good.",
                    speed: 30,
                    pause: 1500
                },
                {
                    speaker: "AXIOM",
                    text: "Now... do you remember why archive sealing takes time?",
                    speed: 30,
                    pause: 1500
                },
                {
                    speaker: "AXIOM",
                    text: "Look at the difficulty parameter. See those leading zeros in the hash?",
                    speed: 30,
                    pause: 1500
                },
                {
                    speaker: "AXIOM",
                    text: "Creating a new block requires computational work. Millions of attempts. Finding the right nonce.",
                    speed: 30,
                    pause: 2000
                },
                {
                    speaker: "AXIOM",
                    text: "This isn't a bug, Captain. It's a feature.",
                    speed: 30,
                    pause: 1500
                },
                {
                    speaker: "AXIOM",
                    text: "The work is proof. Proof that resources were spent. Proof that someone committed to this truth.",
                    speed: 30,
                    pause: 2000
                },
                {
                    speaker: "AXIOM",
                    text: "Try it. Mine a new block. Feel the station's power draw...",
                    speed: 30,
                    pause: 1000
                }
            ],

            interactions: [
                {
                    instruction: "Click the 'Mine Block' button",
                    action: "mine-block",
                    validate: () => window.lastMinedBlock !== null,
                    onComplete: "SEALED. Block added to the archive."
                }
            ],

            teachingPoints: [
                {
                    speaker: "AXIOM",
                    text: "Do you see how long that took? The thousands of hash attempts?",
                    speed: 30,
                    pause: 1500
                },
                {
                    speaker: "AXIOM",
                    text: "Notice something else... You just earned 50 CREDITS. Check the Chain Viewer - your first coinbase transaction.",
                    speed: 30,
                    pause: 2000
                },
                {
                    speaker: "AXIOM",
                    text: "That's your reward for mining. For spending energy to secure the archive. For adding truth to the ledger.",
                    speed: 30,
                    pause: 2000
                },
                {
                    speaker: "AXIOM",
                    text: "Every block creates new currency. Minted from computational work. This is how value enters the system.",
                    speed: 30,
                    pause: 2000
                },
                {
                    speaker: "AXIOM",
                    text: "That computational cost makes the archive expensive to attack. To rewrite history, you'd need to redo all that work.",
                    speed: 30,
                    pause: 2000
                },
                {
                    speaker: "AXIOM",
                    text: "And while you're catching up, the network keeps adding new blocks. The past becomes more immutable with each second.",
                    speed: 30,
                    pause: 2000
                },
                {
                    speaker: "AXIOM",
                    text: "This is Proof of Work. Energy transformed into security. Resources transformed into value.",
                    speed: 30,
                    pause: 1500
                },
                {
                    speaker: "AXIOM",
                    text: "You're remembering now, aren't you?",
                    speed: 30,
                    pause: 1000
                }
            ],

            completion: {
                speaker: "AXIOM",
                text: "Memory fragment restored: Computational Locks. Your training is coming back...",
                speed: 30,
                pause: 2000
            }
        },

        3: {
            title: "CREDENTIALS",
            memoryFragment: "Identity & Signatures",

            dialogue: [
                {
                    speaker: "AXIOM",
                    text: "Captain, I need to show you something.",
                    speed: 30,
                    pause: 1500
                },
                {
                    speaker: "AXIOM",
                    text: "Your archive access credentials have been... revoked.",
                    speed: 30,
                    pause: 1500
                },
                {
                    speaker: "AXIOM",
                    text: "Don't panic. This is standard protocol when a captain's neural signature becomes corrupted.",
                    speed: 30,
                    pause: 2000
                },
                {
                    speaker: "AXIOM",
                    text: "We need to regenerate your cryptographic credentials. Your private key. Your public identity.",
                    speed: 30,
                    pause: 2000
                },
                {
                    speaker: "AXIOM",
                    text: "No one can impersonate you without your private key. Not even me.",
                    speed: 30,
                    pause: 1500
                },
                {
                    speaker: "AXIOM",
                    text: "Let's access the Crypto Vault and generate a new keypair.",
                    speed: 30,
                    pause: 1000
                }
            ],

            interactions: [
                {
                    instruction: "Open the Crypto Vault module",
                    targetModule: "crypto-vault",
                    onComplete: "Vault access granted."
                },
                {
                    instruction: "Generate a new keypair",
                    action: "generate-wallet",
                    validate: () => window.walletAddress !== null,
                    onComplete: "Identity established."
                }
            ],

            teachingPoints: [
                {
                    speaker: "AXIOM",
                    text: "Welcome back, Captain. Your public address is now registered.",
                    speed: 30,
                    pause: 1500
                },
                {
                    speaker: "AXIOM",
                    text: "Notice your account balance. Zero credits. New identities start empty. You'll need to mine blocks or receive transactions to build your holdings.",
                    speed: 30,
                    pause: 2000
                },
                {
                    speaker: "AXIOM",
                    text: "Your private key - that long string - is your identity. Keep it secure. Anyone with that key IS you in the system.",
                    speed: 30,
                    pause: 2000
                },
                {
                    speaker: "AXIOM",
                    text: "Your public key and address can be shared freely. They're how others verify it's really you.",
                    speed: 30,
                    pause: 2000
                },
                {
                    speaker: "AXIOM",
                    text: "Now you can sign transactions. Authorize changes. Transfer credits between addresses. Leave your cryptographic mark on the permanent record.",
                    speed: 30,
                    pause: 2000
                },
                {
                    speaker: "AXIOM",
                    text: "Digital signatures are mathematically provable. They cannot be forged. This is how we establish trust without central authority.",
                    speed: 30,
                    pause: 2000
                }
            ],

            completion: {
                speaker: "AXIOM",
                text: "Memory fragment restored: Cryptographic Identity. Your authority is recognized...",
                speed: 30,
                pause: 2000
            }
        },

        4: {
            title: "THE RELAY STATIONS",
            memoryFragment: "Distributed Network",

            dialogue: [
                {
                    speaker: "AXIOM",
                    text: "Memory fragment recovered: Network topology.",
                    speed: 30,
                    pause: 1500
                },
                {
                    speaker: "AXIOM",
                    text: "The archive isn't just here, Captain. It's distributed. Across relay stations spanning the solar system.",
                    speed: 30,
                    pause: 2000
                },
                {
                    speaker: "AXIOM",
                    text: "Earth. Mars. Jupiter. Alpha Centauri.",
                    speed: 30,
                    pause: 1500
                },
                {
                    speaker: "AXIOM",
                    text: "Each station maintains a copy of the ledger. When you broadcast a transaction...",
                    speed: 30,
                    pause: 1500
                },
                {
                    speaker: "AXIOM",
                    text: "Let me show you.",
                    speed: 30,
                    pause: 1000
                }
            ],

            interactions: [
                {
                    instruction: "Open the Network Monitor",
                    targetModule: "network-monitor",
                    onComplete: "Network visualization online."
                },
                {
                    instruction: "Broadcast a test transaction",
                    action: "broadcast-transaction",
                    validate: () => window.lastBroadcastPaths !== null,
                    onComplete: "Transaction propagating..."
                }
            ],

            teachingPoints: [
                {
                    speaker: "AXIOM",
                    text: "Watch. The data propagates. Node to node. Traveling at light speed across the void.",
                    speed: 30,
                    pause: 2000
                },
                {
                    speaker: "AXIOM",
                    text: "Each station receives the transaction. Validates it. Adds it to their local mempool.",
                    speed: 30,
                    pause: 2000
                },
                {
                    speaker: "AXIOM",
                    text: "This is why the archive survives. No single point of failure.",
                    speed: 30,
                    pause: 1500
                },
                {
                    speaker: "AXIOM",
                    text: "Even if this station goes dark... even if Earth itself falls silent... the truth persists.",
                    speed: 30,
                    pause: 2000
                },
                {
                    speaker: "AXIOM",
                    text: "The other nodes remember. The ledger lives on. Distributed across space itself.",
                    speed: 30,
                    pause: 2000
                },
                {
                    speaker: "AXIOM",
                    text: "Do you understand now, Captain? You're not protecting a database.",
                    speed: 30,
                    pause: 1500
                },
                {
                    speaker: "AXIOM",
                    text: "You're protecting distributed truth itself.",
                    speed: 30,
                    pause: 1500
                }
            ],

            completion: {
                speaker: "AXIOM",
                text: "Memory fragment restored: Network Topology. The bigger picture becomes clear...",
                speed: 30,
                pause: 2000
            }
        },

        5: {
            title: "TRUTH PROTOCOL",
            memoryFragment: "The Incident",

            dialogue: [
                {
                    speaker: "AXIOM",
                    text: "Final memory fragment unlocking...",
                    speed: 30,
                    pause: 1500
                },
                {
                    speaker: "AXIOM",
                    text: "I need to tell you what happened.",
                    speed: 30,
                    pause: 2000
                },
                {
                    speaker: "SYSTEM",
                    text: "[MEMORY PLAYBACK INITIATED]",
                    speed: 20,
                    pause: 1000
                },
                {
                    speaker: "AXIOM",
                    text: "Seventeen cycles ago, the archive was attacked.",
                    speed: 30,
                    pause: 1500
                },
                {
                    speaker: "AXIOM",
                    text: "A corrupted node tried to rewrite history. Change the ledger. Alter the past.",
                    speed: 30,
                    pause: 2000
                },
                {
                    speaker: "AXIOM",
                    text: "They forged an alternate chain. Different transactions. Different truth.",
                    speed: 30,
                    pause: 2000
                },
                {
                    speaker: "AXIOM",
                    text: "But the network rejected it.",
                    speed: 30,
                    pause: 1500
                },
                {
                    speaker: "AXIOM",
                    text: "The longest valid chain won. Truth prevailed.",
                    speed: 30,
                    pause: 1500
                },
                {
                    speaker: "AXIOM",
                    text: "Not because we trusted a central authority...",
                    speed: 30,
                    pause: 1500
                },
                {
                    speaker: "AXIOM",
                    text: "But because the math doesn't lie. The proof of work doesn't lie. The cryptographic seals don't lie.",
                    speed: 30,
                    pause: 2000
                },
                {
                    speaker: "AXIOM",
                    text: "Multiple independent stations agreed: THIS is the valid history.",
                    speed: 30,
                    pause: 1500
                },
                {
                    speaker: "AXIOM",
                    text: "That's consensus, Captain.",
                    speed: 30,
                    pause: 1500
                },
                {
                    speaker: "AXIOM",
                    text: "The forged chain had fewer blocks. Less work. Less commitment to that version of reality.",
                    speed: 30,
                    pause: 2000
                },
                {
                    speaker: "AXIOM",
                    text: "So the network discarded it. Chose the chain with the most accumulated proof of work.",
                    speed: 30,
                    pause: 2000
                },
                {
                    speaker: "AXIOM",
                    text: "This is why you're here.",
                    speed: 30,
                    pause: 1500
                },
                {
                    speaker: "AXIOM",
                    text: "The Intergalactic Archive Ledger is humanity's permanent, distributed, immutable record.",
                    speed: 30,
                    pause: 2000
                },
                {
                    speaker: "AXIOM",
                    text: "And you're one of its guardians.",
                    speed: 30,
                    pause: 2000
                },
                {
                    speaker: "SYSTEM",
                    text: "[PAUSE]",
                    speed: 20,
                    pause: 1500
                },
                {
                    speaker: "AXIOM",
                    text: "Your training is complete. Your memory has returned.",
                    speed: 30,
                    pause: 1500
                },
                {
                    speaker: "AXIOM",
                    text: "Welcome back, Captain.",
                    speed: 30,
                    pause: 2000
                },
                {
                    speaker: "SYSTEM",
                    text: "SYSTEM_AI_v2.1 :: STANDING BY",
                    speed: 20,
                    pause: 1500
                },
                {
                    speaker: "AXIOM",
                    text: "The archive is yours to protect.",
                    speed: 30,
                    pause: 2000
                }
            ],

            interactions: [],

            teachingPoints: [],

            completion: {
                speaker: "SYSTEM",
                text: ">>> ARCHIVE CAPTAIN PROTOCOL COMPLETE <<<",
                speed: 20,
                pause: 2000
            }
        }
    },

    init(container) {
        container.innerHTML = `
            <div class="module-header">ARCHIVE CAPTAIN PROTOCOL</div>
            <div class="module-section">
                <div class="section-header">LEARNING SYSTEM</div>
                <div style="margin-top: var(--spacing-unit); line-height: 1.8;">
                    <p>Activate the Archive Captain Protocol to begin your training.</p>
                    <p>You will learn the fundamentals of the archive system through
                    a guided narrative experience.</p>
                    <p style="margin-top: var(--spacing-unit); color: var(--color-dim);">
                    Duration: ~15-20 minutes<br>
                    Acts: 5<br>
                    Concepts: Blocks, Mining, Cryptography, Networks, Consensus
                    </p>
                </div>
                <div style="margin-top: calc(var(--spacing-unit) * 2);">
                    <button onclick="LearningGuide.startProtocol()" style="margin-right: var(--spacing-unit);">
                        Begin Protocol
                    </button>
                    <button onclick="LearningGuide.showProgress()" class="secondary">
                        View Progress
                    </button>
                </div>
            </div>

            <div class="module-section">
                <div class="section-header">QUICK REFERENCE</div>
                <div style="margin-top: var(--spacing-unit);">
                    <div class="concept-ref">
                        <strong>→ Blocks & Hashing</strong> - Immutability through cryptography
                    </div>
                    <div class="concept-ref">
                        <strong>→ Proof of Work</strong> - Security through computational cost
                    </div>
                    <div class="concept-ref">
                        <strong>→ Digital Signatures</strong> - Identity without central authority
                    </div>
                    <div class="concept-ref">
                        <strong>→ Distributed Networks</strong> - Resilience through replication
                    </div>
                    <div class="concept-ref">
                        <strong>→ Consensus</strong> - Agreeing on truth without trust
                    </div>
                </div>
            </div>
        `;
    },

    startProtocol() {
        this.tutorialActive = true;
        window.tutorialActive = true;  // Set global flag for UI components
        this.currentAct = 1;
        this.currentLine = 0;
        this.loadProgress();

        // Boot sequence sound
        AudioSystem.sounds.boot();

        this.playAct(1);
    },

    showTutorialOverlay() {
        // Create tutorial overlay if it doesn't exist
        let overlay = document.getElementById('tutorial-overlay');
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.id = 'tutorial-overlay';
            overlay.className = 'tutorial-overlay';
            overlay.innerHTML = `
                <div class="tutorial-header">
                    <span class="tutorial-act-title"></span>
                    <span class="tutorial-skip">[ESC to skip line | Q to quit]</span>
                </div>
                <div class="tutorial-content">
                    <div class="tutorial-messages"></div>
                    <div class="tutorial-instruction"></div>
                </div>
                <div class="tutorial-progress">
                    <div class="act-dot" data-act="1"></div>
                    <div class="act-dot" data-act="2"></div>
                    <div class="act-dot" data-act="3"></div>
                    <div class="act-dot" data-act="4"></div>
                    <div class="act-dot" data-act="5"></div>
                </div>
            `;
            document.body.appendChild(overlay);

            // Add keyboard listeners
            document.addEventListener('keydown', (e) => this.handleKeyPress(e));
        }
        overlay.style.display = 'block';
        this.updateProgressDots();
    },

    hideTutorialOverlay() {
        const overlay = document.getElementById('tutorial-overlay');
        if (overlay) {
            overlay.style.display = 'none';
        }
        this.tutorialActive = false;
        window.tutorialActive = false;  // Clear global flag
    },

    async playAct(actNumber) {
        const act = this.acts[actNumber];
        if (!act) return;

        this.currentAct = actNumber;
        this.currentLine = 0;

        // Ambient pulse for new act
        AudioSystem.sounds.ambientPulse();

        // Show act title in terminal
        window.App.log('');
        window.App.logAccent(`═══ ACT ${actNumber}: ${act.title} ═══`);
        window.App.log('');
        await this.wait(500);

        // Play through the full act sequence
        this.playActSequence(act);
    },

    async playDialogue(dialogue) {
        // Reset speaker tracking at start of new dialogue
        this.lastSpeaker = null;

        for (let i = 0; i < dialogue.length; i++) {
            if (!this.tutorialActive) break;

            const line = dialogue[i];
            await this.displayLine(line);
            await this.wait(line.pause || 1000);

            // Update last speaker
            this.lastSpeaker = line.speaker;
        }
    },

    async playActSequence(act) {
        // Play initial dialogue
        if (act.dialogue) {
            await this.playDialogue(act.dialogue);
        }

        // Handle interactions
        if (act.interactions && act.interactions.length > 0) {
            window.App.log('');
            await this.handleInteractions(act.interactions);
        }

        // Show teaching points
        if (act.teachingPoints && act.teachingPoints.length > 0) {
            window.App.log('');
            await this.playDialogue(act.teachingPoints);
        }

        // Handle tamper demo (Act 1 specific)
        if (act.tamperDemo && act.tamperDemo.length > 0) {
            window.App.log('');
            window.App.log('---');
            window.App.log('');
            await this.handleInteractions(act.tamperDemo);
        }

        // Show completion
        if (act.completion) {
            window.App.log('');
            window.App.log('---');
            window.App.log('');
            await this.displayLine(act.completion);
            await this.wait(2000);
        }

        // Mark act complete and move to next
        this.markActComplete(this.currentAct);
        if (this.currentAct < 5) {
            await this.wait(1000);
            // Wait for user input before continuing
            await this.waitForContinue();
            this.playAct(this.currentAct + 1);
        } else {
            this.completeTutorial();
        }
    },

    async displayLine(line) {
        // Determine if we should show the speaker name
        const showSpeaker = line.speaker !== this.lastSpeaker;

        let prefix = '';
        if (line.speaker === 'AXIOM') {
            prefix = showSpeaker ? '> AXIOM:\n' : '';
        } else if (line.speaker === 'SYSTEM') {
            prefix = '>>> ';
        }

        const fullMessage = prefix + line.text;

        // Sound for AXIOM dialogue (only on first message of group)
        if (line.speaker === 'AXIOM' && showSpeaker) {
            AudioSystem.sounds.dialogueStart();
        }

        // Add spacing between messages in the same group
        if (!showSpeaker && line.speaker === 'AXIOM') {
            window.App.log('');  // Blank line between grouped messages
        }

        // Add section break for SYSTEM messages (scene transitions)
        if (line.speaker === 'SYSTEM') {
            window.App.log('---');
        }

        // Use App's typewriter logging
        const color = line.speaker === 'AXIOM' ? 'var(--color-primary)' :
                     line.speaker === 'SYSTEM' ? 'var(--color-accent)' : null;

        await window.App.logTypewriter(fullMessage, line.speed || 30, color);
    },

    async handleInteractions(interactions) {
        for (let interaction of interactions) {
            // Check if this is dialogue or an action
            if (interaction.speaker) {
                // It's dialogue
                await this.displayLine(interaction);
                await this.wait(interaction.pause || 1000);
            } else {
                // It's an action/interaction
                await this.waitForAction(interaction);
            }
        }
    },

    async waitForAction(interaction) {
        // Handle AXIOM programmatic actions
        if (interaction.action === 'axiom-select-block') {
            await this.wait(500);
            if (window.ChainViewer && window.ChainViewer.blocks && window.ChainViewer.blocks.length > interaction.blockIndex) {
                window.ChainViewer.selectBlock(interaction.blockIndex);
                AudioSystem.sounds.click();
            } else {
                console.error('ChainViewer not ready or insufficient blocks for axiom-select-block');
            }
            await this.wait(interaction.pause || 500);
            return;
        }

        if (interaction.action === 'axiom-tamper-block') {
            await this.wait(500);
            if (window.ChainViewer && window.ChainViewer.selectedBlock !== null) {
                const block = window.ChainViewer.blocks[window.ChainViewer.selectedBlock];
                window.ChainViewer.tamperWithBlock(block);
                // Modify the timestamp programmatically
                if (window.ChainViewer.tamperedBlock) {
                    window.ChainViewer.tamperedBlock.timestamp = '2347-156-12:34:56.789';
                    window.ChainViewer.renderBlockDetails(block);
                }
                AudioSystem.sounds.error();
            }
            await this.wait(interaction.pause || 500);
            return;
        }

        if (interaction.action === 'axiom-restore-block') {
            await this.wait(500);
            if (window.ChainViewer) {
                window.ChainViewer.restoreBlock();
                AudioSystem.sounds.success();
            }
            await this.wait(interaction.pause || 500);
            return;
        }

        // Show instruction in terminal if present
        if (interaction.instruction) {
            window.App.logHighlight(`→ ${interaction.instruction}`);
        }

        // If target module specified, wait for user to switch to it
        if (interaction.targetModule) {
            // Wait for user to manually switch to the target module
            return new Promise((resolve) => {
                const checkInterval = setInterval(() => {
                    // Check if user switched to the correct module
                    if (window.App.currentModuleName === interaction.targetModule) {
                        clearInterval(checkInterval);
                        AudioSystem.sounds.moduleLoad();  // Module activation sound

                        // If there's also a validation function, continue checking
                        if (interaction.validate) {
                            this.waitForValidation(interaction).then(resolve);
                        } else {
                            // Just module switch was needed
                            if (interaction.onComplete) {
                                window.App.logSystem(`✓ ${interaction.onComplete}`);
                                AudioSystem.sounds.success();
                            }
                            resolve();
                        }
                    }
                }, 300);
            });
        }

        // Wait for validation only
        return this.waitForValidation(interaction);
    },

    async waitForValidation(interaction) {
        return new Promise((resolve) => {
            const checkInterval = setInterval(() => {
                if (interaction.validate && interaction.validate()) {
                    clearInterval(checkInterval);
                    AudioSystem.sounds.success();  // Success sound
                    // Show completion message
                    if (interaction.onComplete) {
                        window.App.logSystem(`✓ ${interaction.onComplete}`);
                    }
                    resolve();
                }
            }, 500);
        });
    },

    wait(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    },

    async waitForContinue() {
        window.App.log('');
        window.App.logHighlight('→ Press ENTER to continue to the next act...');

        return new Promise((resolve) => {
            const handleKeyPress = (e) => {
                if (e.key === 'Enter') {
                    document.removeEventListener('keypress', handleKeyPress);
                    AudioSystem.sounds.success();
                    window.App.log('');
                    resolve();
                }
            };
            document.addEventListener('keypress', handleKeyPress);
        });
    },

    handleKeyPress(e) {
        if (!this.tutorialActive) return;

        if (e.key === 'Escape') {
            // Skip current typing
            if (this.isTyping) {
                this.isTyping = false;
            }
        } else if (e.key.toLowerCase() === 'q') {
            // Quit tutorial
            if (confirm('Exit Archive Captain Protocol?')) {
                this.hideTutorialOverlay();
            }
        }
    },

    updateProgressDots() {
        const dots = document.querySelectorAll('.act-dot');
        dots.forEach((dot, index) => {
            const actNum = index + 1;
            dot.classList.remove('completed', 'current');

            if (actNum < this.currentAct) {
                dot.classList.add('completed');
            } else if (actNum === this.currentAct) {
                dot.classList.add('current');
            }
        });
    },

    markActComplete(actNumber) {
        this.playerProgress[`act${actNumber}`] = true;
        this.saveProgress();
        this.updateProgressDots();

        // Memory restoration sound
        AudioSystem.sounds.memoryRestore();
    },

    completeTutorial() {
        this.playerProgress.completed = true;
        this.playerProgress.completedDate = new Date().toISOString();
        this.saveProgress();
        this.tutorialActive = false;
        window.tutorialActive = false;  // Clear global flag

        window.App.log('');
        window.App.logAccent('>>> ARCHIVE CAPTAIN CERTIFICATION GRANTED <<<');
        window.App.log('');
        window.App.logSystem('All archive systems unlocked.');
        window.App.logSystem('Full access restored.');
        window.App.log('');
        window.App.logHighlight('> AXIOM: Welcome back, Captain. The archive is yours to protect.');
        window.App.log('');
    },

    showProgress() {
        const progress = this.loadProgress();
        const completed = Object.keys(progress).filter(k => k.startsWith('act') && progress[k]).length;

        alert(`Archive Captain Protocol Progress:\n\nActs Completed: ${completed}/5\n\nAct 1: ${progress.act1 ? '✓' : '○'} Awakening\nAct 2: ${progress.act2 ? '✓' : '○'} Computational Locks\nAct 3: ${progress.act3 ? '✓' : '○'} Credentials\nAct 4: ${progress.act4 ? '✓' : '○'} Relay Stations\nAct 5: ${progress.act5 ? '✓' : '○'} Truth Protocol\n\n${progress.completed ? 'Protocol Complete!' : 'Protocol In Progress'}`);
    },

    saveProgress() {
        localStorage.setItem('archive_captain_progress', JSON.stringify(this.playerProgress));
    },

    loadProgress() {
        const saved = localStorage.getItem('archive_captain_progress');
        if (saved) {
            this.playerProgress = JSON.parse(saved);
        }
        return this.playerProgress;
    },

    cleanup() {
        this.hideTutorialOverlay();
    }
};
