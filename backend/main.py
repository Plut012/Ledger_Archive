"""FastAPI application entry point."""

from pathlib import Path
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

from state import state
from mining import Miner
from transaction import Transaction
from crypto import Wallet

app = FastAPI(title="Interstellar Archive Terminal API")

# Get the frontend directory path
FRONTEND_DIR = Path(__file__).parent.parent / "frontend"

# Mount static files (CSS, JS, assets)
app.mount("/css", StaticFiles(directory=FRONTEND_DIR / "css"), name="css")
app.mount("/js", StaticFiles(directory=FRONTEND_DIR / "js"), name="js")
app.mount("/assets", StaticFiles(directory=FRONTEND_DIR / "assets"), name="assets")


@app.get("/")
def root():
    """Serve the frontend application."""
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/api/chain")
def get_chain():
    """Return the full blockchain."""
    return {
        "chain": [block.to_dict() for block in state.blockchain.chain],
        "length": len(state.blockchain.chain)
    }


@app.get("/api/chain/block/{block_hash}")
def get_block(block_hash: str):
    """Get a specific block by hash."""
    for block in state.blockchain.chain:
        if block.hash == block_hash:
            return {"block": block.to_dict()}
    return {"error": "Block not found"}


@app.post("/api/mine")
def mine_new_block(request: dict = None):
    """
    Mine a new block with pending transactions.
    Creates a coinbase transaction to reward the miner.
    """
    # Get miner address from request or use default
    miner_address = "DEFAULT_MINER"
    if request and "miner_address" in request:
        miner_address = request["miner_address"]

    miner = Miner(difficulty=4)
    block = miner.mine_block(
        state.blockchain.get_latest_block(),
        state.mempool,
        miner_address=miner_address
    )

    if state.blockchain.add_block(block):
        # Recalculate balances after adding block
        state.ledger.calculate_balances()
        state.mempool.clear()

        # Extract coinbase transaction for response
        coinbase_tx = Transaction.from_dict(block.transactions[0])

        return {
            "status": "success",
            "block": block.to_dict(),
            "coinbase": {
                "recipient": coinbase_tx.recipient,
                "reward": coinbase_tx.amount
            }
        }

    return {"status": "error", "message": "Failed to add block"}


@app.post("/api/transaction")
def create_transaction(tx_data: dict):
    """
    Add a transaction to mempool.
    Validates that sender has sufficient funds.
    """
    tx = Transaction.from_dict(tx_data)

    # Validate transaction with balance checking
    if not tx.is_valid(ledger=state.ledger):
        # Check if it's a balance issue
        sender_balance = state.ledger.get_balance(tx.sender)
        if sender_balance < tx.amount:
            return {
                "status": "invalid",
                "error": "Insufficient funds",
                "available": sender_balance,
                "required": tx.amount
            }
        return {"status": "invalid", "message": "Transaction validation failed"}

    # Add to mempool
    state.mempool.append(tx.to_dict())

    # Return success with balance info
    sender_balance_after = state.ledger.get_balance(tx.sender) - tx.amount

    return {
        "status": "added",
        "tx_hash": tx.calculate_hash(),
        "sender_balance_after": sender_balance_after
    }


@app.get("/api/state")
def get_state():
    """Get current blockchain state."""
    return {
        "height": len(state.blockchain.chain),
        "latest_block": state.blockchain.get_latest_block().to_dict(),
        "pending_transactions": len(state.mempool),
        "is_valid": state.blockchain.is_valid_chain()
    }


@app.get("/api/mempool")
def get_mempool():
    """Get pending transactions from mempool."""
    return {
        "transactions": state.mempool,
        "count": len(state.mempool)
    }


@app.get("/api/balance/{address}")
def get_balance(address: str):
    """Get balance for a specific address."""
    balance = state.ledger.get_balance(address)
    return {
        "address": address,
        "balance": balance
    }


@app.get("/api/balances")
def get_all_balances():
    """Get all non-zero balances and total supply."""
    balances = state.ledger.get_all_balances()
    total_supply = state.ledger.get_total_supply()

    return {
        "balances": balances,
        "total_supply": total_supply,
        "num_accounts": len(balances)
    }


@app.post("/api/wallet/generate")
def generate_wallet():
    """Generate a new wallet with keypair."""
    wallet = Wallet()
    wallet.generate_keypair()

    return {
        "status": "success",
        "wallet": {
            "address": wallet.address,
            "public_key": wallet.get_public_key_pem(),
            "private_key": wallet.get_private_key_pem()
        },
        "warning": "Keep your private key secure! This is for educational purposes only."
    }


@app.get("/api/network/topology")
def get_network_topology():
    """Get network topology with nodes and connections."""
    return state.network.get_topology()


@app.get("/api/network/node/{node_id}")
def get_node_details(node_id: str):
    """Get detailed information about a specific node."""
    details = state.network.get_node_details(node_id)
    if details is None:
        return {"error": "Node not found"}
    return details


@app.post("/api/network/broadcast")
def broadcast_transaction(tx_data: dict):
    """
    Broadcast a transaction through the network.
    Returns propagation paths.
    This is primarily for network visualization - validation is optional.
    """
    # Get origin node (default to first node if not specified)
    origin_node_id = tx_data.get("origin_node", "node_0")

    # For network visualization, we accept the transaction as-is
    # Create a minimal transaction dict for tracking
    tx_dict = {
        "sender": tx_data.get("sender", "unknown"),
        "recipient": tx_data.get("recipient", "unknown"),
        "amount": tx_data.get("amount", 0),
        "timestamp": tx_data.get("timestamp", 0),
        "signature": tx_data.get("signature", "")
    }

    # Broadcast through network
    paths = state.network.broadcast_transaction(tx_dict, origin_node_id)

    # Also add to main mempool (optional)
    state.mempool.append(tx_dict)

    # Calculate hash for tracking
    tx = Transaction.from_dict(tx_dict)
    tx_hash = tx.calculate_hash()

    return {
        "status": "broadcasted",
        "tx_hash": tx_hash,
        "origin": origin_node_id,
        "propagation_paths": paths
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time updates."""
    await websocket.accept()

    try:
        while True:
            # Send periodic state updates
            await websocket.send_json({
                "type": "state_update",
                "height": len(state.blockchain.chain),
                "pending": len(state.mempool)
            })

            # Receive and process messages
            data = await websocket.receive_json()
            # TODO: Handle WebSocket messages

    except Exception as e:
        print(f"WebSocket error: {e}")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
