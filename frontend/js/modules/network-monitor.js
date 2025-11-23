// Network Monitor Module

const NetworkMonitor = {
    topology: null,
    selectedNode: null,
    canvas: null,
    ctx: null,
    animationFrame: null,
    txAnimations: [],

    async init(container) {
        container.innerHTML = `
            <div class="module-header">NETWORK LATTICE MONITOR</div>

            <div class="module-section">
                <canvas id="network-canvas" width="500" height="400" style="border: 1px solid #00ff00; background: #000;"></canvas>
            </div>

            <div class="module-section">
                <div class="section-header">NODE DETAILS</div>
                <div id="node-details">
                    <div style="color: #666;">Click a node to view details</div>
                </div>
            </div>

            <div class="module-section">
                <div class="section-header">NETWORK ACTIONS</div>
                <button onclick="NetworkMonitor.broadcastTestTransaction()">Broadcast Test TX</button>
                <button onclick="NetworkMonitor.refreshTopology()">Refresh Topology</button>
            </div>

            <div class="module-section">
                <div class="section-header">ACTIVITY LOG</div>
                <div id="network-log" style="max-height: 100px; overflow-y: auto; font-size: 0.85em;"></div>
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
            this.log('Error loading topology: ' + error.message);
        }
    },

    async refreshTopology() {
        this.log('Refreshing network topology...');
        await this.loadTopology();
        this.log('Topology refreshed');
    },

    draw() {
        if (!this.topology) return;

        const ctx = this.ctx;
        ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        // Draw connections first (so they appear behind nodes)
        ctx.strokeStyle = '#00ff00';
        ctx.lineWidth = 1;
        this.topology.connections.forEach(([fromId, toId]) => {
            const fromNode = this.topology.nodes.find(n => n.id === fromId);
            const toNode = this.topology.nodes.find(n => n.id === toId);

            if (fromNode && toNode) {
                ctx.beginPath();
                ctx.moveTo(fromNode.x, fromNode.y);
                ctx.lineTo(toNode.x, toNode.y);
                ctx.stroke();
            }
        });

        // Draw nodes
        this.topology.nodes.forEach(node => {
            const isSelected = this.selectedNode && this.selectedNode.id === node.id;

            // Node circle
            ctx.beginPath();
            ctx.arc(node.x, node.y, isSelected ? 12 : 8, 0, 2 * Math.PI);
            ctx.fillStyle = isSelected ? '#ffff00' : '#00ff00';
            ctx.fill();
            ctx.strokeStyle = '#00ff00';
            ctx.lineWidth = 2;
            ctx.stroke();

            // Node label
            ctx.fillStyle = '#00ff00';
            ctx.font = '12px monospace';
            ctx.textAlign = 'center';
            ctx.fillText(node.label, node.x, node.y - 15);

            // Height indicator
            ctx.font = '10px monospace';
            ctx.fillStyle = '#666';
            ctx.fillText(`#${node.height}`, node.x, node.y + 25);
        });

        // Draw transaction animations
        this.txAnimations.forEach(anim => {
            ctx.beginPath();
            ctx.arc(anim.x, anim.y, 4, 0, 2 * Math.PI);
            ctx.fillStyle = '#ff00ff';
            ctx.fill();
        });
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
                this.log('Error: ' + details.error);
                return;
            }

            this.selectedNode = details;
            this.updateNodeDetails(details);
            this.draw();
            this.log(`Selected node: ${details.label}`);
        } catch (error) {
            this.log('Error fetching node details: ' + error.message);
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

            this.log(`Broadcasting transaction from ${testTx.origin_node}...`);

            const response = await fetch('/api/network/broadcast', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(testTx)
            });

            const result = await response.json();

            if (result.status === 'broadcasted') {
                this.log(`TX ${result.tx_hash.substring(0, 8)}... broadcasted from ${result.origin}`);

                // Update global state for tutorial validation
                window.lastBroadcastPaths = result.propagation_paths;

                this.animatePropagation(result.propagation_paths);
            } else {
                this.log('Broadcast failed: ' + result.message);
            }
        } catch (error) {
            this.log('Error broadcasting transaction: ' + error.message);
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

    log(message) {
        const logDiv = document.getElementById('network-log');
        if (!logDiv) return;

        const timestamp = new Date().toLocaleTimeString();
        const entry = document.createElement('div');
        entry.style.color = '#00ff00';
        entry.textContent = `[${timestamp}] ${message}`;

        logDiv.insertBefore(entry, logDiv.firstChild);

        // Keep only last 10 entries
        while (logDiv.children.length > 10) {
            logDiv.removeChild(logDiv.lastChild);
        }
    },

    cleanup() {
        if (this.animationFrame) {
            cancelAnimationFrame(this.animationFrame);
        }
        this.topology = null;
        this.selectedNode = null;
        this.txAnimations = [];
    }
};
