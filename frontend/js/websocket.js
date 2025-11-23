// WebSocket client for real-time updates

const WebSocketClient = {
    ws: null,
    reconnectInterval: 5000,
    handlers: {},

    init() {
        this.connect();
        return this;
    },

    connect() {
        try {
            // Dynamically determine WebSocket URL based on current page
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const host = window.location.host;
            const wsUrl = `${protocol}//${host}/ws`;

            console.log('Connecting to WebSocket:', wsUrl);
            this.ws = new WebSocket(wsUrl);

            this.ws.onopen = () => {
                console.log('WebSocket connected');
            };

            this.ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                this.handleMessage(data);
            };

            this.ws.onerror = (error) => {
                console.error('WebSocket error:', error);
            };

            this.ws.onclose = () => {
                console.log('WebSocket disconnected, reconnecting...');
                setTimeout(() => this.connect(), this.reconnectInterval);
            };
        } catch (error) {
            console.error('Failed to connect WebSocket:', error);
            setTimeout(() => this.connect(), this.reconnectInterval);
        }
    },

    handleMessage(data) {
        // Update UI based on message type
        switch (data.type) {
            case 'state_update':
                this.updateStatus(data);
                break;
            case 'block_mined':
                this.onBlockMined(data);
                break;
            case 'transaction_added':
                this.onTransactionAdded(data);
                break;
            default:
                console.log('Unknown message type:', data.type);
        }

        // Call registered handlers
        if (this.handlers[data.type]) {
            this.handlers[data.type].forEach(handler => handler(data));
        }
    },

    updateStatus(data) {
        const heightEl = document.getElementById('chain-height');
        const pendingEl = document.getElementById('pending-tx');

        if (heightEl) heightEl.textContent = `#${data.height}`;
        if (pendingEl) pendingEl.textContent = data.pending;
    },

    onBlockMined(data) {
        if (App && App.log) {
            App.log(`Block mined: #${data.block.index}`);
        }
    },

    onTransactionAdded(data) {
        if (App && App.log) {
            App.log(`Transaction added to mempool`);
        }
    },

    on(eventType, handler) {
        if (!this.handlers[eventType]) {
            this.handlers[eventType] = [];
        }
        this.handlers[eventType].push(handler);
    },

    send(data) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(data));
        } else {
            console.error('WebSocket not connected');
        }
    }
};
