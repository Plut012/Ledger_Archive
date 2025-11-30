// Network Monitor Module

const NetworkMonitor = {
    topology: null,
    selectedNode: null,
    canvas: null,
    ctx: null,
    animationFrame: null,
    txAnimations: [],
    deadStations: new Set(),
    collapseActive: false,
    playerWeight: 2.0,
    stationsActive: 50,
    deathAnimations: [], // { stationId, phase, progress }

    async init(container) {
        container.innerHTML = `
            <div class="module-header">NETWORK</div>

            <div style="display: flex; gap: calc(var(--spacing-unit) * 2);">
                <!-- Left sidebar with controls -->
                <div style="flex: 0 0 220px;">
                    <div class="module-section">
                        <div class="section-title">[NETWORK ACTIONS]</div>
                        <button onclick="NetworkMonitor.broadcastTestTransaction()" style="width: 100%; margin-bottom: 8px;">Broadcast Test TX</button>
                        <button onclick="NetworkMonitor.refreshTopology()" style="width: 100%;">Refresh Topology</button>
                    </div>

                    <div class="module-section" id="consensus-weight-panel">
                        <div class="section-title">[CONSENSUS WEIGHT]</div>
                        <div id="weight-display">
                            <div style="font-size: 24px; color: #00ff00; margin-bottom: 8px;" id="player-weight">2.0%</div>
                            <div style="font-size: 12px; color: #666;" id="stations-active">50/50 Stations Online</div>
                            <div id="weight-warning" style="display: none; margin-top: 8px; padding: 8px; background: rgba(255, 107, 53, 0.2); border: 1px solid var(--color-accent); color: var(--color-accent); font-size: 11px;">
                                WARNING: APPROACHING CRITICAL CONSENSUS THRESHOLD
                            </div>
                        </div>
                    </div>

                    <div class="module-section">
                        <div class="section-title">[NODE DETAILS]</div>
                        <div id="node-details">
                            <div style="color: #666; font-size: 14px;">Click a node to view details</div>
                        </div>
                    </div>
                </div>

                <!-- Main canvas area -->
                <div style="flex: 1; display: flex; align-items: center; justify-content: center;">
                    <div class="module-section" style="margin: 0;">
                        <div class="section-title" style="text-align: center; margin-bottom: var(--spacing-unit);" id="topology-header">[IMPERIUM TOPOLOGY - 50 NODES]</div>
                        <canvas id="network-canvas" width="1000" height="600" style="border: 1px solid #00ff00; background: #000; display: block;"></canvas>
                    </div>
                </div>
            </div>
        `;

        this.canvas = document.getElementById('network-canvas');
        this.ctx = this.canvas.getContext('2d');

        // Add click handler for node selection
        this.canvas.addEventListener('click', (e) => this.handleCanvasClick(e));

        // Load initial topology
        await this.loadTopology();
        this.startAnimation();
    },

    async loadTopology() {
        try {
            const response = await fetch('/api/network/topology');
            this.topology = await response.json();
            this.draw();
        } catch (error) {
            console.error('Error loading topology:', error);
            App.log('Error loading network topology');
        }
    },

    async refreshTopology() {
        App.log('Refreshing network topology...');
        await this.loadTopology();
        App.log('Topology refreshed');
    },

    draw() {
        if (!this.topology) return;

        const ctx = this.ctx;
        ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        // Sort nodes by layer (background to foreground) for proper rendering
        const sortedNodes = [...this.topology.nodes].sort((a, b) => b.layer - a.layer);

        // Draw connections grouped by layer
        for (let layer = 3; layer >= 1; layer--) {
            this.drawConnectionsForLayer(ctx, layer);
        }

        // Draw nodes from back to front
        sortedNodes.forEach(node => {
            this.drawNode(ctx, node);
        });

        // Draw transaction animations (always on top)
        this.txAnimations.forEach(anim => {
            ctx.beginPath();
            ctx.arc(anim.x, anim.y, 4, 0, 2 * Math.PI);
            ctx.fillStyle = '#ff00ff';
            ctx.fill();
        });
    },

    drawConnectionsForLayer(ctx, layer) {
        const layerProps = this.getLayerProperties(layer);

        this.topology.connections.forEach(([fromId, toId]) => {
            const fromNode = this.topology.nodes.find(n => n.id === fromId);
            const toNode = this.topology.nodes.find(n => n.id === toId);

            // Skip connections to dead stations
            const fromDead = this.deadStations.has(fromId);
            const toDead = this.deadStations.has(toId);

            if (fromDead || toDead) {
                return; // Don't draw connections to/from dead nodes
            }

            // Only draw if at least one node is in this layer
            if (fromNode && toNode && (fromNode.layer === layer || toNode.layer === layer)) {
                ctx.beginPath();
                ctx.moveTo(fromNode.x, fromNode.y);
                ctx.lineTo(toNode.x, toNode.y);
                ctx.strokeStyle = layerProps.connectionColor;
                ctx.lineWidth = layerProps.connectionWidth;
                ctx.globalAlpha = layerProps.alpha;
                ctx.stroke();
                ctx.globalAlpha = 1.0;
            }
        });
    },

    drawNode(ctx, node) {
        const isSelected = this.selectedNode && this.selectedNode.id === node.id;
        const isDead = this.deadStations.has(node.id);
        const isFlickering = node.flickering;
        const layerProps = this.getLayerProperties(node.layer);

        // Skip drawing if flickering and in "off" state
        if (isFlickering) {
            return;
        }

        // Dead node styling
        if (isDead) {
            // Draw dead node (dark, no glow)
            ctx.beginPath();
            ctx.arc(node.x, node.y, layerProps.size, 0, 2 * Math.PI);
            ctx.fillStyle = '#330000';
            ctx.globalAlpha = 0.3;
            ctx.fill();
            ctx.strokeStyle = '#660000';
            ctx.lineWidth = 1;
            ctx.stroke();
            ctx.globalAlpha = 1.0;

            // Dead label
            if (node.layer <= 2 || isSelected) {
                ctx.fillStyle = '#660000';
                ctx.font = `${layerProps.fontSize}px monospace`;
                ctx.textAlign = 'center';
                ctx.globalAlpha = 0.4;
                ctx.fillText('[DEAD]', node.x, node.y - layerProps.size - 5);
                ctx.globalAlpha = 1.0;
            }

            return;
        }

        // Normal node rendering (alive)
        // Node glow effect (for foreground nodes)
        if (node.layer === 1 && !isSelected) {
            ctx.beginPath();
            ctx.arc(node.x, node.y, layerProps.size + 4, 0, 2 * Math.PI);
            ctx.fillStyle = layerProps.glowColor;
            ctx.globalAlpha = 0.3;
            ctx.fill();
            ctx.globalAlpha = 1.0;
        }

        // Node circle
        ctx.beginPath();
        ctx.arc(node.x, node.y, isSelected ? layerProps.size + 4 : layerProps.size, 0, 2 * Math.PI);
        ctx.fillStyle = isSelected ? '#ffff00' : layerProps.color;
        ctx.globalAlpha = layerProps.alpha;
        ctx.fill();
        ctx.strokeStyle = layerProps.borderColor;
        ctx.lineWidth = isSelected ? 2 : 1;
        ctx.stroke();
        ctx.globalAlpha = 1.0;

        // Node label (only show for layer 1 and 2, or if selected)
        if (node.layer <= 2 || isSelected) {
            ctx.fillStyle = layerProps.textColor;
            ctx.font = `${layerProps.fontSize}px monospace`;
            ctx.textAlign = 'center';
            ctx.globalAlpha = layerProps.alpha;
            ctx.fillText(node.label, node.x, node.y - layerProps.size - 5);
            ctx.globalAlpha = 1.0;
        }

        // Height indicator (only for selected or layer 1)
        if (isSelected || node.layer === 1) {
            ctx.font = '9px monospace';
            ctx.fillStyle = '#666';
            ctx.fillText(`#${node.height}`, node.x, node.y + layerProps.size + 12);
        }
    },

    getLayerProperties(layer) {
        // Layer-based visual properties for 2.5D effect
        const props = {
            1: {  // Foreground - Core Archives
                size: 10,
                color: '#00ff00',
                borderColor: '#00ff00',
                glowColor: 'rgba(0, 255, 100, 0.5)',
                textColor: '#00ff00',
                connectionColor: 'rgba(0, 255, 100, 0.8)',
                connectionWidth: 2,
                fontSize: 11,
                alpha: 1.0
            },
            2: {  // Mid - Sector Hubs
                size: 7,
                color: '#00cc66',
                borderColor: '#00cc66',
                glowColor: 'rgba(0, 204, 102, 0.3)',
                textColor: '#00cc66',
                connectionColor: 'rgba(0, 204, 102, 0.5)',
                connectionWidth: 1.5,
                fontSize: 10,
                alpha: 0.7
            },
            3: {  // Background - Frontier Stations
                size: 5,
                color: '#009944',
                borderColor: '#009944',
                glowColor: 'rgba(0, 153, 68, 0.2)',
                textColor: '#009944',
                connectionColor: 'rgba(0, 153, 68, 0.3)',
                connectionWidth: 1,
                fontSize: 9,
                alpha: 0.5
            }
        };

        return props[layer] || props[1];
    },

    handleCanvasClick(event) {
        if (!this.topology) return;

        const rect = this.canvas.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;

        // Find clicked node
        for (const node of this.topology.nodes) {
            const dx = x - node.x;
            const dy = y - node.y;
            const distance = Math.sqrt(dx * dx + dy * dy);

            if (distance <= 12) {
                this.selectNode(node.id);
                return;
            }
        }
    },

    async selectNode(nodeId) {
        try {
            const response = await fetch(`/api/network/node/${nodeId}`);
            const details = await response.json();

            if (details.error) {
                App.log('Error: ' + details.error);
                return;
            }

            this.selectedNode = details;
            this.updateNodeDetails(details);
            this.draw();
            App.log(`Selected: ${details.label}`);
        } catch (error) {
            console.error('Error fetching node details:', error);
            App.log('Error fetching node details');
        }
    },

    updateNodeDetails(details) {
        const detailsDiv = document.getElementById('node-details');
        const statusIcon = details.status === 'synced' ? '◉' : '○';

        detailsDiv.innerHTML = `
            <div style="line-height: 1.6;">
                <strong>Selected:</strong> ${details.label}<br>
                <strong>Node ID:</strong> ${details.id}<br>
                <strong>Address:</strong> ${details.address}<br>
                <strong>Status:</strong> ${statusIcon} ${details.status.toUpperCase()}<br>
                <strong>Height:</strong> #${details.height}<br>
                <strong>Peers:</strong> ${details.peers.join(', ')}<br>
                <strong>Mempool:</strong> ${details.mempool_size} tx
            </div>
        `;
    },

    async broadcastTestTransaction() {
        try {
            // Create a simple test transaction
            const testTx = {
                sender: 'test_sender',
                recipient: 'test_recipient',
                amount: Math.floor(Math.random() * 100) + 1,
                timestamp: Date.now(),
                signature: 'test_signature_' + Math.random().toString(36).substr(2, 9),
                origin_node: this.selectedNode ? this.selectedNode.id : 'node_0'
            };

            const originLabel = this.selectedNode ? this.selectedNode.label : 'node_0';
            App.log(`Broadcasting TX from ${originLabel}...`);

            const response = await fetch('/api/network/broadcast', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(testTx)
            });

            const result = await response.json();

            if (result.status === 'broadcasted') {
                App.log(`TX ${result.tx_hash.substring(0, 8)}... propagated to network`);

                // Update global state for tutorial validation
                window.lastBroadcastPaths = result.propagation_paths;

                this.animatePropagation(result.propagation_paths);
            } else {
                App.log('Broadcast failed');
            }
        } catch (error) {
            console.error('Error broadcasting transaction:', error);
            App.log('Error broadcasting transaction');
        }
    },

    animatePropagation(paths) {
        if (!paths || paths.length === 0) return;

        // Create animations for each propagation path
        paths.forEach((path, index) => {
            setTimeout(() => {
                this.animatePath(path);
            }, index * 100); // Stagger the animations
        });
    },

    animatePath(path) {
        if (path.length < 2) return;

        let currentSegment = 0;
        let progress = 0;
        const speed = 0.02; // Progress per frame

        const animate = () => {
            if (currentSegment >= path.length - 1) {
                // Animation complete - flash the destination node
                this.flashNode(path[path.length - 1]);
                return;
            }

            const fromId = path[currentSegment];
            const toId = path[currentSegment + 1];

            const fromNode = this.topology.nodes.find(n => n.id === fromId);
            const toNode = this.topology.nodes.find(n => n.id === toId);

            if (fromNode && toNode) {
                const x = fromNode.x + (toNode.x - fromNode.x) * progress;
                const y = fromNode.y + (toNode.y - fromNode.y) * progress;

                // Update or create animation
                const animId = `${fromId}-${toId}`;
                let anim = this.txAnimations.find(a => a.id === animId);

                if (!anim) {
                    anim = { id: animId, x, y };
                    this.txAnimations.push(anim);
                } else {
                    anim.x = x;
                    anim.y = y;
                }

                progress += speed;

                if (progress >= 1.0) {
                    // Move to next segment
                    progress = 0;
                    currentSegment++;
                    this.flashNode(toId);

                    // Remove completed animation
                    this.txAnimations = this.txAnimations.filter(a => a.id !== animId);
                }

                requestAnimationFrame(animate);
            }
        };

        animate();
    },

    flashNode(nodeId) {
        // Visual feedback when tx reaches a node
        const node = this.topology.nodes.find(n => n.id === nodeId);
        if (node) {
            const ctx = this.ctx;
            ctx.beginPath();
            ctx.arc(node.x, node.y, 15, 0, 2 * Math.PI);
            ctx.strokeStyle = '#ff00ff';
            ctx.lineWidth = 3;
            ctx.stroke();

            setTimeout(() => this.draw(), 200);
        }
    },

    startAnimation() {
        const animate = () => {
            this.draw();
            this.animationFrame = requestAnimationFrame(animate);
        };
        animate();
    },

    // ========================================================================
    // Network Collapse Methods
    // ========================================================================

    async checkForStationDeaths() {
        /**
         * Poll the server for station deaths and update the UI.
         * Called periodically or on act transitions.
         */
        try {
            const response = await fetch('/api/network/collapse/check', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    playerId: 'default'
                })
            });

            const result = await response.json();

            // Process any new deaths
            if (result.deaths && result.deaths.length > 0) {
                for (const death of result.deaths) {
                    await this.killStation(death.station_id, death.reason, death.final_message);
                }
            }

            // Update weight display
            this.updateWeightDisplay(result.stations_active, result.player_weight, result.is_critical);

        } catch (error) {
            console.error('Error checking station deaths:', error);
        }
    },

    async killStation(stationId, reason, finalMessage) {
        /**
         * Animate the death of a station.
         *
         * Animation phases:
         * 1. Flicker (1000ms)
         * 2. Connections snap
         * 3. Node goes dark
         */
        const node = this.topology?.nodes.find(n => n.id === stationId);
        if (!node) return;

        App.log(`⚠ STATION DEATH: ${stationId} - ${reason}`);
        if (finalMessage) {
            App.log(`> "${finalMessage}"`);
        }

        // Play station death sound
        AudioManager.play('stationDeath');

        // Start death animation
        this.deathAnimations.push({
            stationId,
            phase: 'flicker',
            progress: 0,
            startTime: Date.now()
        });

        // Phase 1: Flicker for 1 second
        await this.flickerNode(node, 1000);

        // Phase 2: Snap connections and mark as dead
        setTimeout(() => {
            this.deadStations.add(stationId);

            // Update animation state
            const anim = this.deathAnimations.find(a => a.stationId === stationId);
            if (anim) {
                anim.phase = 'dead';
            }

            // Recalculate weights
            this.recalculateWeights();

            this.draw();
        }, 1200);
    },

    async flickerNode(node, duration) {
        /**
         * Make a node flicker before dying.
         */
        const startTime = Date.now();
        const flicker = () => {
            const elapsed = Date.now() - startTime;
            if (elapsed < duration) {
                // Random visibility
                node.flickering = Math.random() > 0.5;
                this.draw();
                setTimeout(flicker, 100);
            } else {
                node.flickering = false;
            }
        };
        flicker();
    },

    recalculateWeights() {
        /**
         * Recalculate player weight based on remaining stations.
         */
        if (!this.topology) return;

        const activeNodes = this.topology.nodes.filter(n => !this.deadStations.has(n.id));
        this.stationsActive = activeNodes.length;

        // Equal weight distribution
        this.playerWeight = this.stationsActive > 0 ? (100 / this.stationsActive) : 100;

        this.updateWeightDisplay(this.stationsActive, this.playerWeight, this.playerWeight >= 30);
    },

    updateWeightDisplay(stationsActive, playerWeight, isCritical) {
        /**
         * Update the consensus weight panel.
         */
        this.stationsActive = stationsActive;
        this.playerWeight = playerWeight;

        const weightEl = document.getElementById('player-weight');
        const stationsEl = document.getElementById('stations-active');
        const warningEl = document.getElementById('weight-warning');
        const headerEl = document.getElementById('topology-header');

        if (weightEl) {
            weightEl.textContent = `${playerWeight.toFixed(1)}%`;

            // Change color based on weight
            if (isCritical) {
                weightEl.style.color = '#ff6b35';
                weightEl.style.textShadow = '0 0 10px rgba(255, 107, 53, 0.8)';
            } else if (playerWeight >= 15) {
                weightEl.style.color = '#ffaa00';
            } else {
                weightEl.style.color = '#00ff00';
                weightEl.style.textShadow = 'none';
            }
        }

        if (stationsEl) {
            stationsEl.textContent = `${stationsActive}/50 Stations Online`;
        }

        if (warningEl) {
            warningEl.style.display = isCritical ? 'block' : 'none';
        }

        if (headerEl) {
            headerEl.textContent = `[IMPERIUM TOPOLOGY - ${stationsActive} NODES]`;
        }
    },

    async startCollapseSequence() {
        /**
         * Begin the network collapse sequence.
         * Stations will start dying according to the schedule.
         */
        this.collapseActive = true;
        App.log('⚠ NETWORK COLLAPSE INITIATED');

        // Poll for deaths every 2 seconds
        this.collapseInterval = setInterval(() => {
            this.checkForStationDeaths();
        }, 2000);
    },

    stopCollapseSequence() {
        /**
         * Stop the collapse sequence.
         */
        this.collapseActive = false;
        if (this.collapseInterval) {
            clearInterval(this.collapseInterval);
            this.collapseInterval = null;
        }
    },

    cleanup() {
        if (this.animationFrame) {
            cancelAnimationFrame(this.animationFrame);
        }
        this.stopCollapseSequence();
        this.topology = null;
        this.selectedNode = null;
        this.txAnimations = [];
        this.deadStations.clear();
        this.deathAnimations = [];
    }
};
