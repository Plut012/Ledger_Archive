"""FastAPI application entry point."""

from pathlib import Path
from fastapi import FastAPI, WebSocket, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from contextlib import asynccontextmanager
import uvicorn
import os
from datetime import datetime

from state import state
from mining import Miner
from transaction import Transaction
from crypto import Wallet

# Import LLM and character systems
from llm.client import LLMClient
from db.mongo import mongo_client
from db.sessions import SessionManager
from characters.archivist import ArchivistController
from characters.witness import WitnessController

# Import narrative state system
from narrative.state import GameState, PersistentState, SessionState
from narrative.triggers import TriggerEngine
from narrative.loop import LoopManager

# Import filesystem module
from filesystem.vfs import VirtualFileSystem
from filesystem.commands import CommandExecutor

# Import procedural blockchain module
from procedural.generator import BlockGenerator
from procedural.testimony import TestimonyParser

# Import network collapse system
from network.collapse import NetworkCollapseScheduler

# Import stealth mechanics
from stealth.monitor import StealthMonitor

# Import crypto vault story
from vault.letters import LetterManager
from crypto import LetterEncryption, encrypt_letter, decrypt_letter

# Import protocol engine (smart contracts)
from contracts.engine import ContractEngine
from contracts.executor import ContractExecutor


# Global instances
session_manager = None
archivist_controller = None
witness_controller = None

# Narrative state management
# In-memory state storage (for single-player with IndexedDB persistence)
game_states: dict = {}
trigger_engine = TriggerEngine()

# Shell filesystem
vfs = VirtualFileSystem()
stealth_monitor = StealthMonitor()
command_executor = CommandExecutor(vfs, stealth_monitor)

# Blockchain generator
block_generator = BlockGenerator(seed_version="v1")

# Network collapse scheduler
collapse_scheduler = NetworkCollapseScheduler(seed=42)

# Letter manager for crypto vault story
letter_manager = LetterManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    global session_manager, archivist_controller, witness_controller

    # Startup
    await mongo_client.connect()
    session_manager = SessionManager(mongo_client)
    await session_manager.initialize()

    # Initialize LLM client
    llm_client = LLMClient()

    # Initialize character controllers
    archivist_controller = ArchivistController(llm_client, session_manager)
    witness_controller = WitnessController(llm_client, session_manager)

    print("🤖 Character system initialized")

    yield

    # Shutdown
    await mongo_client.disconnect()
    print("👋 Shutting down")


app = FastAPI(
    title="Interstellar Archive Terminal API",
    lifespan=lifespan
)

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


# ============================================================================
# Character Chat Endpoints
# ============================================================================

@app.post("/api/session/create")
async def create_session():
    """Create a new game session."""
    session_id = await session_manager.create_session()
    return {"session_id": session_id}


@app.get("/api/session/{session_id}")
async def get_session_state(session_id: str):
    """Get current session state."""
    session = await session_manager.get_session(session_id)
    if not session:
        return {"error": "Session not found"}

    return {
        "session_id": session_id,
        "game_state": session.get("game_state", {}),
        "created_at": session.get("created_at"),
        "last_activity": session.get("last_activity")
    }


@app.post("/api/session/{session_id}/state")
async def update_session_state(session_id: str, request: Request):
    """Update game state for a session."""
    data = await request.json()
    updates = data.get("updates", {})

    await session_manager.update_game_state(session_id, updates)
    return {"status": "updated"}


@app.post("/api/chat/stream")
async def chat_stream(request: Request):
    """
    Streaming chat endpoint for character conversations.

    Request body:
    {
        "session_id": "uuid",
        "character": "archivist" | "witness",
        "message": "user message",
        "additional_context": {}  // optional
    }

    Returns: Server-Sent Events stream
    """
    data = await request.json()

    session_id = data.get("session_id")
    character = data.get("character", "archivist").lower()
    message = data.get("message")
    additional_context = data.get("additional_context")

    if not session_id or not message:
        return {"error": "session_id and message are required"}

    # Get current game state
    session = await session_manager.get_session(session_id)
    if not session:
        return {"error": "Session not found"}

    game_state = session.get("game_state", {})

    # Select controller
    if character == "archivist":
        controller = archivist_controller
    elif character == "witness":
        controller = witness_controller
    else:
        return {"error": f"Unknown character: {character}"}

    # Stream response
    async def generate():
        """Generate SSE stream."""
        async for chunk_data in controller.respond(
            session_id=session_id,
            user_message=message,
            game_state=game_state,
            additional_context=additional_context
        ):
            # Format as Server-Sent Event
            import json
            yield f"data: {json.dumps(chunk_data)}\n\n"

            # Update game state if provided
            if chunk_data.get("done") and chunk_data.get("stateUpdates"):
                await session_manager.update_game_state(
                    session_id,
                    chunk_data["stateUpdates"]
                )

    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )


@app.post("/api/chat")
async def chat_non_streaming(request: Request):
    """
    Non-streaming chat endpoint (for testing/compatibility).

    Returns complete response at once.
    """
    data = await request.json()

    session_id = data.get("session_id")
    character = data.get("character", "archivist").lower()
    message = data.get("message")
    additional_context = data.get("additional_context")

    if not session_id or not message:
        return {"error": "session_id and message are required"}

    # Get current game state
    session = await session_manager.get_session(session_id)
    if not session:
        return {"error": "Session not found"}

    game_state = session.get("game_state", {})

    # Select controller
    if character == "archivist":
        controller = archivist_controller
    elif character == "witness":
        controller = witness_controller
    else:
        return {"error": f"Unknown character: {character}"}

    # Collect full response
    full_response = ""
    final_data = {}

    async for chunk_data in controller.respond(
        session_id=session_id,
        user_message=message,
        game_state=game_state,
        additional_context=additional_context
    ):
        if chunk_data.get("chunk"):
            full_response += chunk_data["chunk"]

        if chunk_data.get("done"):
            final_data = chunk_data
            # Update game state
            if chunk_data.get("stateUpdates"):
                await session_manager.update_game_state(
                    session_id,
                    chunk_data["stateUpdates"]
                )

    return {
        "response": full_response,
        "character": character,
        "stateUpdates": final_data.get("stateUpdates", {}),
        "error": final_data.get("error", False)
    }


@app.post("/api/conversation/reset")
async def reset_conversation(request: Request):
    """Reset conversation history for a character (loop reset)."""
    data = await request.json()

    session_id = data.get("session_id")
    character = data.get("character", "archivist").lower()

    if not session_id:
        return {"error": "session_id is required"}

    await session_manager.reset_conversation(session_id, character)
    return {"status": "reset", "character": character}


# ============================================================================
# Narrative State Endpoints
# ============================================================================

@app.post("/api/narrative/state/init")
async def init_narrative_state(request: Request):
    """Initialize narrative state for new player."""
    data = await request.json()
    player_id = data.get("playerId", "default")

    # Create new game state
    state = GameState(
        persistent=PersistentState(),
        session=SessionState()
    )

    game_states[player_id] = state

    return state.to_dict()


@app.post("/api/narrative/state/update")
async def update_narrative_state(request: Request):
    """Update narrative state and evaluate triggers."""
    data = await request.json()
    player_id = data.get("playerId", "default")
    updates = data.get("updates", {})

    state = game_states.get(player_id)
    if not state:
        return {"error": "State not found"}, 404

    # Apply updates to session or persistent state
    for key, value in updates.items():
        if hasattr(state.session, key):
            setattr(state.session, key, value)
        elif hasattr(state.persistent, key):
            setattr(state.persistent, key, value)

    # Evaluate triggers
    state = trigger_engine.evaluate_all(state)

    # Check for reset condition
    if LoopManager.should_trigger_reset(state):
        state = LoopManager.reset_to_next_iteration(state, "HIGH_SUSPICION")
        return {
            "reset": True,
            "iteration": state.persistent.iteration,
            "message": LoopManager.get_reset_message(
                state.persistent.iteration,
                "HIGH_SUSPICION"
            ),
            "state": state.to_dict()
        }

    game_states[player_id] = state

    return state.to_dict()


@app.post("/api/narrative/state/reset")
async def manual_narrative_reset(request: Request):
    """Manually trigger iteration reset."""
    data = await request.json()
    player_id = data.get("playerId", "default")
    reason = data.get("reason", "MANUAL_RESET")

    state = game_states.get(player_id)
    if not state:
        return {"error": "State not found"}, 404

    state = LoopManager.reset_to_next_iteration(state, reason)
    game_states[player_id] = state

    return {
        "reset": True,
        "iteration": state.persistent.iteration,
        "message": LoopManager.get_reset_message(state.persistent.iteration, reason),
        "state": state.to_dict()
    }


@app.get("/api/narrative/state/export")
async def export_narrative_state(player_id: str = "default"):
    """Export state for saving/persistence."""
    state = game_states.get(player_id)

    if not state:
        return {"error": "State not found"}, 404

    return state.to_dict()


@app.post("/api/narrative/state/import")
async def import_narrative_state(request: Request):
    """Import saved state from IndexedDB."""
    data = await request.json()
    player_id = data.get("playerId", "default")
    state_data = data.get("state", {})

    try:
        state = GameState.from_dict(state_data)
        game_states[player_id] = state
        return {"status": "imported", "state": state.to_dict()}
    except Exception as e:
        return {"error": f"Failed to import state: {str(e)}"}, 400


@app.get("/api/narrative/state/llm-context")
async def get_llm_context(player_id: str = "default"):
    """Get state formatted for LLM context."""
    state = game_states.get(player_id)

    if not state:
        return {"error": "State not found"}, 404

    return state.export_for_llm()


# ============================================================================
# Blockchain Integration Endpoints (Graveyard & Testimony)
# ============================================================================

@app.get("/api/blockchain/block/{index}")
async def get_blockchain_block(index: int):
    """
    Get a specific block by index from procedural chain.

    Supports the full 850K block history including:
    - Standard procedural blocks
    - Graveyard blocks (50K-75K)
    - Story-critical blocks
    """
    try:
        block = block_generator.generate_block(index)

        # Check if this is a graveyard block
        is_graveyard = 50000 <= index <= 75000

        block_dict = block.to_dict()
        block_dict["isGraveyard"] = is_graveyard

        return block_dict
    except Exception as e:
        return {"error": f"Failed to generate block: {str(e)}"}, 500


@app.post("/api/blockchain/reconstruct")
async def reconstruct_consciousness(request: Request):
    """
    Reconstruct consciousness from archive block.

    WARNING: This action is MONITORED by ARCHIVIST.
    Significantly increases suspicion and increases Witness trust.
    """
    data = await request.json()
    block_index = data.get("blockIndex")
    tx_index = data.get("txIndex", 0)
    player_id = data.get("playerId", "default")

    if block_index is None:
        return {"error": "blockIndex is required"}, 400

    # Get or create game state
    state = game_states.get(player_id)
    if not state:
        state = GameState(
            persistent=PersistentState(),
            session=SessionState()
        )
        game_states[player_id] = state

    # Increase ARCHIVIST suspicion significantly
    state.session.archivist_suspicion = min(100, state.session.archivist_suspicion + 20)

    # Increase Witness trust for using reconstruction
    state.session.witness_trust = min(100, state.session.witness_trust + 10)

    # Store updated state
    game_states[player_id] = state

    # Perform reconstruction
    result = TestimonyParser.reconstruct_consciousness(block_index, tx_index)

    if "error" in result:
        return result, 400

    # Add state changes to response
    result["stateUpdates"] = {
        "archivistSuspicion": state.session.archivist_suspicion,
        "witnessTrust": state.session.witness_trust
    }

    return result


# ============================================================================
# Shell & Filesystem Endpoints
# ============================================================================

@app.post("/api/shell/command")
async def execute_shell_command(request: Request):
    """Execute shell command in virtual filesystem."""
    data = await request.json()
    command = data.get("command", "")
    player_id = data.get("playerId", "default")

    if not command:
        return {"error": "No command provided"}, 400

    # Get or create game state
    state = game_states.get(player_id)
    if not state:
        # Initialize state if not exists
        state = GameState(
            persistent=PersistentState(),
            session=SessionState()
        )
        game_states[player_id] = state

    # Build state context for command executor
    state_context = {
        "persistent": {
            "files_unlocked": state.persistent.files_unlocked,
            "current_act": state.persistent.current_act,
            "current_iteration": state.persistent.current_iteration
        },
        "session": {
            "archivist_suspicion": state.session.archivist_suspicion,
            "witness_trust": state.session.witness_trust,
            "log_mask_active": state.session.log_mask_active,
            "log_mask_expires": state.session.log_mask_expires
        }
    }

    # Execute command
    output, state_updates = command_executor.execute(command, state_context)

    # Apply state updates
    for key, value in state_updates.items():
        if hasattr(state.session, key):
            setattr(state.session, key, value)

    # Evaluate triggers after state changes
    state = trigger_engine.evaluate_all(state)

    # Store updated state
    game_states[player_id] = state

    return {
        "output": output,
        "cwd": vfs.current_path,
        "stateUpdates": state_updates,
        "narrativeState": {
            "archivistSuspicion": state.session.archivist_suspicion,
            "witnessTrust": state.session.witness_trust,
            "currentAct": state.persistent.current_act,
            "logMaskActive": state.session.log_mask_active
        }
    }


# ============================================================================
# Network Collapse Endpoints
# ============================================================================

@app.get("/api/network/collapse/schedule")
async def get_collapse_schedule():
    """
    Get the complete station death schedule.

    Returns the full schedule of when stations will die across all acts.
    """
    schedule = collapse_scheduler.generate_death_schedule()

    return {
        "total_deaths": len(schedule),
        "schedule": [
            {
                "station_id": d.station_id,
                "station_label": d.station_label,
                "reason": d.reason,
                "final_message": d.final_message,
                "timestamp": d.timestamp,
                "act": d.act
            }
            for d in schedule
        ]
    }


@app.post("/api/network/collapse/check")
async def check_station_deaths(request: Request):
    """
    Check for station deaths at current game time.

    Updates game state with any stations that should die.
    """
    data = await request.json()
    player_id = data.get("playerId", "default")

    # Get or create game state
    state = game_states.get(player_id)
    if not state:
        state = GameState(
            persistent=PersistentState(),
            session=SessionState()
        )
        game_states[player_id] = state

    # Get deaths for current time
    deaths = collapse_scheduler.get_deaths_for_timestamp(
        state.session.game_time,
        state.persistent.current_act
    )

    # Update state with deaths
    for death in deaths:
        if death.station_id not in state.session.dead_stations:
            state.session.dead_stations.append(death.station_id)

    # Recalculate stations active and player weight
    state.session.stations_active = collapse_scheduler.get_stations_alive(
        state.session.game_time,
        state.persistent.current_act
    )

    state.session.player_weight = collapse_scheduler.calculate_player_weight(
        state.session.stations_active
    )

    # Store updated state
    game_states[player_id] = state

    return {
        "deaths": [
            {
                "station_id": d.station_id,
                "station_label": d.station_label,
                "reason": d.reason,
                "final_message": d.final_message,
                "act": d.act
            }
            for d in deaths
        ],
        "stations_active": state.session.stations_active,
        "player_weight": state.session.player_weight,
        "is_critical": collapse_scheduler.is_critical_weight(state.session.player_weight),
        "next_death_time": collapse_scheduler.get_next_death_time(state.session.game_time)
    }


@app.post("/api/network/collapse/advance-time")
async def advance_game_time(request: Request):
    """
    Advance game time (for testing or time-based progression).

    Args:
        playerId: Player ID
        increment: Time increment in days (default: 0.1)
    """
    data = await request.json()
    player_id = data.get("playerId", "default")
    increment = data.get("increment", 0.1)

    # Get or create game state
    state = game_states.get(player_id)
    if not state:
        return {"error": "State not found"}, 404

    # Advance time
    state.session.game_time += increment

    # Check for any new deaths
    deaths = collapse_scheduler.get_deaths_for_timestamp(
        state.session.game_time,
        state.persistent.current_act
    )

    # Update state
    for death in deaths:
        if death.station_id not in state.session.dead_stations:
            state.session.dead_stations.append(death.station_id)

    state.session.stations_active = collapse_scheduler.get_stations_alive(
        state.session.game_time,
        state.persistent.current_act
    )

    state.session.player_weight = collapse_scheduler.calculate_player_weight(
        state.session.stations_active
    )

    game_states[player_id] = state

    return {
        "game_time": state.session.game_time,
        "deaths": [
            {
                "station_id": d.station_id,
                "station_label": d.station_label,
                "reason": d.reason,
                "final_message": d.final_message
            }
            for d in deaths
        ],
        "stations_active": state.session.stations_active,
        "player_weight": state.session.player_weight,
        "is_critical": collapse_scheduler.is_critical_weight(state.session.player_weight)
    }


@app.get("/api/network/collapse/status")
async def get_collapse_status(player_id: str = "default"):
    """Get current collapse status for a player."""
    state = game_states.get(player_id)

    if not state:
        return {"error": "State not found"}, 404

    return {
        "game_time": state.session.game_time,
        "current_act": state.persistent.current_act,
        "collapse_begun": state.session.collapse_begun,
        "stations_active": state.session.stations_active,
        "dead_stations": state.session.dead_stations,
        "player_weight": state.session.player_weight,
        "is_critical": collapse_scheduler.is_critical_weight(state.session.player_weight),
        "next_death_time": collapse_scheduler.get_next_death_time(state.session.game_time)
    }


# =============================================================================
# STEALTH MECHANICS ENDPOINTS
# =============================================================================

@app.get("/api/stealth/monitoring/status")
async def get_monitoring_status(player_id: str = "default"):
    """
    Get current ARCHIVIST monitoring status.

    Returns information about detection chances, active evasion methods,
    and monitoring intensity based on current act.
    """
    state = game_states.get(player_id)

    if not state:
        return {"error": "State not found"}, 404

    # Get monitoring status from stealth monitor
    status = stealth_monitor.get_monitoring_status(state.to_dict())

    # Add current suspicion level
    status["currentSuspicion"] = state.session.archivist_suspicion

    return status


@app.post("/api/stealth/archivist/busy")
async def set_archivist_busy(request: Request):
    """
    Mark ARCHIVIST as busy (generating response to complex question).

    This reduces detection chance for monitored commands during the busy window.

    Request body:
        {
            "durationSeconds": 5  // How long ARCHIVIST will be busy
        }
    """
    data = await request.json()
    duration = data.get("durationSeconds", 5)

    stealth_monitor.set_archivist_busy(duration)

    return {
        "success": True,
        "archivistBusyUntil": stealth_monitor.archivist_busy_until,
        "message": f"ARCHIVIST marked as busy for {duration} seconds"
    }


@app.post("/api/stealth/validation/active")
async def set_validation_active(request: Request):
    """
    Set whether block validation is currently happening.

    During validation, ARCHIVIST's attention is split, reducing detection chance.

    Request body:
        {
            "active": true  // Whether validation is running
        }
    """
    data = await request.json()
    active = data.get("active", False)

    stealth_monitor.set_validation_active(active)

    return {
        "success": True,
        "validationActive": stealth_monitor.validation_active,
        "message": f"Validation active: {active}"
    }


@app.post("/api/stealth/command/check")
async def check_command_monitoring(request: Request):
    """
    Check if a command would trigger ARCHIVIST monitoring.

    Useful for UI hints to show players if a command is monitored.

    Request body:
        {
            "command": "reconstruct 74221",
            "playerId": "default"
        }

    Returns:
        {
            "detected": true/false,
            "suspicionIncrease": 15,
            "detectionChance": 0.85,
            "reason": "KEYWORDS:reconstruct",
            "suggestion": "chain.parse --deep --memo --block=74221"  // If alias available
        }
    """
    data = await request.json()
    command = data.get("command", "")
    player_id = data.get("playerId", "default")

    state = game_states.get(player_id)
    if not state:
        return {"error": "State not found"}, 404

    # Check the command
    result = stealth_monitor.check_command(command, state.to_dict())

    # Get evasion suggestion if available
    suggestion = stealth_monitor.get_evasion_suggestion(command)

    return {
        "detected": result.detected,
        "suspicionIncrease": result.suspicion_increase,
        "detectionChance": result.detection_chance,
        "reason": result.reason,
        "suggestion": suggestion
    }


@app.get("/api/stealth/evasion/methods")
async def get_evasion_methods(player_id: str = "default"):
    """
    Get available evasion methods for current act.

    Returns list of evasion techniques the player has access to.
    """
    state = game_states.get(player_id)
    if not state:
        return {"error": "State not found"}, 404

    current_act = state.session.current_act

    return {
        "act": current_act,
        "methods": stealth_monitor._get_available_evasion_methods(current_act),
        "aliases": stealth_monitor.EVASION_ALIASES,
        "monitoringLevel": stealth_monitor._get_monitoring_level_description(current_act)
    }


# =============================================================================
# CRYPTO VAULT STORY ENDPOINTS
# =============================================================================

@app.post("/api/vault/initialize")
async def initialize_vault(request: Request):
    """
    Initialize vault with encrypted letters from past iterations.

    Called when player reaches an iteration where letters should exist.
    Generates and encrypts letters using keys from "past" iterations.

    Request body:
        {
            "playerId": "default",
            "currentIteration": 17
        }

    Returns:
        Status and number of letters generated
    """
    data = await request.json()
    player_id = data.get("playerId", "default")
    current_iteration = data.get("currentIteration", 1)

    state = game_states.get(player_id)
    if not state:
        return {"error": "State not found"}, 404

    # Only generate letters if we're past iteration 3
    if current_iteration < 4:
        return {
            "status": "not_ready",
            "message": "Letters only available from iteration 4+",
            "letters_count": 0
        }

    # Check if letters already exist
    if len(state.persistent.encrypted_letters) > 0:
        return {
            "status": "already_initialized",
            "letters_count": len(state.persistent.encrypted_letters)
        }

    # Generate letter content for past iterations
    letters = letter_manager.generate_letters_for_iteration(current_iteration)

    # For each letter, we need to encrypt it
    # In the hybrid model, we'll encrypt to a "future" key that exists in keys_generated
    # For now, we'll create dummy encrypted versions (to be decrypted by any key)
    encrypted_letters = []

    for letter in letters:
        # Create a temporary encryption key for this letter
        encryptor = LetterEncryption()
        encryptor.generate_keypair()

        # Encrypt the letter content
        encrypted_content = encryptor.encrypt_message(
            letter["content"],
            encryptor.get_public_key_pem()
        )

        # Store the letter with its corresponding private key
        # This allows decryption with the matching key
        encrypted_letters.append({
            "id": letter["id"],
            "encrypted_content": encrypted_content,
            "from_iteration": letter["from_iteration"],
            "timestamp": letter["timestamp"],
            "decryption_key": encryptor.get_private_key_pem()  # Stored for puzzle matching
        })

    # Update persistent state
    state.persistent.encrypted_letters = encrypted_letters
    game_states[player_id] = state

    return {
        "status": "initialized",
        "letters_count": len(encrypted_letters),
        "message": f"Generated {len(encrypted_letters)} encrypted letters from past iterations"
    }


@app.get("/api/vault/letters")
async def get_vault_letters(player_id: str = "default"):
    """
    Get all letters in the vault (encrypted and decrypted).

    Returns letter metadata without revealing encrypted content.
    """
    state = game_states.get(player_id)
    if not state:
        return {"error": "State not found"}, 404

    letters = []

    for letter in state.persistent.encrypted_letters:
        letter_info = {
            "id": letter["id"],
            "from_iteration": letter["from_iteration"],
            "timestamp": letter.get("timestamp", "unknown"),
            "decrypted": letter["id"] in state.persistent.decrypted_letters,
            "preview": "[ENCRYPTED - Use a key to decrypt]"
        }

        # If decrypted, show preview
        if letter_info["decrypted"]:
            # Find the decrypted content (we'll store it separately)
            letter_info["preview"] = "Letter successfully decrypted - view in vault"

        letters.append(letter_info)

    decrypted_count = len(state.persistent.decrypted_letters)
    hint = letter_manager.get_letter_hints(decrypted_count)

    return {
        "letters": letters,
        "total_count": len(letters),
        "decrypted_count": decrypted_count,
        "hint": hint
    }


@app.post("/api/vault/decrypt")
async def decrypt_letter(request: Request):
    """
    Attempt to decrypt a letter using a key from past iterations.

    Request body:
        {
            "playerId": "default",
            "letterId": "letter_iteration_3",
            "keyIndex": 0  // Index in keys_generated array
        }

    Returns:
        Success status and decrypted content (or error)
    """
    data = await request.json()
    player_id = data.get("playerId", "default")
    letter_id = data.get("letterId")
    key_index = data.get("keyIndex", -1)

    state = game_states.get(player_id)
    if not state:
        return {"error": "State not found"}, 404

    # Find the letter
    letter = None
    for l in state.persistent.encrypted_letters:
        if l["id"] == letter_id:
            letter = l
            break

    if not letter:
        return {"error": "Letter not found"}, 404

    # Check if already decrypted
    if letter_id in state.persistent.decrypted_letters:
        return {
            "status": "already_decrypted",
            "message": "This letter has already been decrypted"
        }

    # For the puzzle mechanic, we match letter to key by iteration
    # The "correct" key is stored with the letter
    correct_key = letter.get("decryption_key")

    if not correct_key:
        return {"error": "Letter has no decryption key"}, 500

    # Attempt decryption
    try:
        decrypted_content = decrypt_letter(
            letter["encrypted_content"],
            correct_key
        )

        # Mark as decrypted
        state.persistent.decrypted_letters.add(letter_id)

        # Increase Witness trust for successful decryption
        trust_increase = 15
        state.session.witness_trust = min(100, state.session.witness_trust + trust_increase)

        # Store decrypted content in messages_to_future for persistence
        state.persistent.messages_to_future.append({
            "id": letter_id,
            "content": decrypted_content,
            "from_iteration": letter["from_iteration"],
            "decrypted_at": letter.get("timestamp", "unknown")
        })

        game_states[player_id] = state

        return {
            "status": "success",
            "decrypted_content": decrypted_content,
            "trust_increase": trust_increase,
            "new_trust": state.session.witness_trust,
            "message": f"Letter from iteration {letter['from_iteration']} decrypted!"
        }

    except ValueError as e:
        return {
            "status": "failure",
            "error": "Decryption failed - wrong key or corrupted data",
            "message": "This key doesn't match this letter. Try a different one."
        }


@app.get("/api/vault/keys")
async def get_vault_keys(player_id: str = "default"):
    """
    Get all keys from past iterations.

    Shows which keys are available for decrypting letters.
    """
    state = game_states.get(player_id)
    if not state:
        return {"error": "State not found"}, 404

    current_iteration = state.persistent.iteration

    # Return keys with metadata
    keys = []
    for idx, key in enumerate(state.persistent.keys_generated):
        keys.append({
            "index": idx,
            "iteration": key.get("iteration", "unknown"),
            "timestamp": key.get("timestamp", "unknown"),
            "public_key_preview": key.get("publicKey", "")[:64] + "...",
            "from_past": key.get("iteration", 0) < current_iteration
        })

    return {
        "keys": keys,
        "total_count": len(keys),
        "current_iteration": current_iteration
    }


@app.post("/api/vault/generate-key")
async def generate_vault_key(request: Request):
    """
    Generate a new encryption key for the current iteration.

    Request body:
        {
            "playerId": "default"
        }

    Returns:
        New key information
    """
    data = await request.json()
    player_id = data.get("playerId", "default")

    state = game_states.get(player_id)
    if not state:
        return {"error": "State not found"}, 404

    # Generate new RSA key pair for encryption
    encryptor = LetterEncryption()
    encryptor.generate_keypair()

    # Store in keys_generated
    key_data = {
        "publicKey": encryptor.get_public_key_pem(),
        "privateKey": encryptor.get_private_key_pem(),
        "iteration": state.persistent.iteration,
        "timestamp": str(datetime.now())
    }

    state.persistent.keys_generated.append(key_data)
    game_states[player_id] = state

    return {
        "status": "success",
        "key_index": len(state.persistent.keys_generated) - 1,
        "iteration": state.persistent.iteration,
        "public_key_preview": key_data["publicKey"][:64] + "...",
        "message": "New encryption key generated"
    }


# ============================================================================
# PROTOCOL ENGINE (SMART CONTRACTS) ENDPOINTS
# ============================================================================

@app.get("/api/contracts/list")
async def get_contracts_list(player_id: str = "default"):
    """
    Get list of all contracts (unlocked and locked).

    Query params:
        player_id: Player identifier

    Returns:
        List of contract metadata with unlock status
    """
    engine = ContractEngine()

    # Get player's game state
    state = game_states.get(player_id)
    if not state:
        # Initialize default state
        state = GameState(
            persistent=PersistentState(),
            session=SessionState()
        )
        game_states[player_id] = state

    # Get all contracts
    all_contracts = engine.list_all_contracts()

    # Add unlock status to each
    unlocked_contracts = engine.get_unlocked_contracts_for_player(state)
    unlocked_ids = {c["id"] for c in unlocked_contracts}

    contracts_with_status = []
    for contract in all_contracts:
        unlock_check = engine.check_unlock_condition(contract["id"], state)
        contracts_with_status.append({
            **contract,
            "unlocked": contract["id"] in unlocked_ids,
            "unlock_condition_met": unlock_check["unlocked"],
            "unlock_reason": unlock_check.get("reason", "")
        })

    return {
        "status": "success",
        "total_contracts": len(all_contracts),
        "unlocked_count": len(unlocked_ids),
        "contracts": contracts_with_status
    }


@app.get("/api/contracts/{contract_id}")
async def get_contract_code(contract_id: str, player_id: str = "default"):
    """
    Get full contract code if unlocked.

    Path params:
        contract_id: Contract identifier

    Query params:
        player_id: Player identifier

    Returns:
        Contract code and metadata, or error if locked
    """
    engine = ContractEngine()

    # Get player's game state
    state = game_states.get(player_id)
    if not state:
        state = GameState(
            persistent=PersistentState(),
            session=SessionState()
        )
        game_states[player_id] = state

    # Get contract with unlock check
    result = engine.get_contract_code(contract_id, state)

    if "error" in result:
        return {
            "status": "error",
            "error": result["error"],
            "unlock_condition": result.get("unlock_condition", "Unknown")
        }

    # Check if viewing increases suspicion
    suspicion_increase = engine.should_increase_suspicion(contract_id)
    if suspicion_increase > 0:
        state.session.archivist_suspicion += suspicion_increase
        game_states[player_id] = state

    return {
        "status": "success",
        "contract": result,
        "suspicion_increased": suspicion_increase
    }


@app.post("/api/contracts/execute")
async def execute_contract(request: Request):
    """
    Execute a contract function (simulated).

    Request body:
        {
            "playerId": "default",
            "contractId": "witness_reconstruction",
            "function": "parseConsciousness",
            "args": {"blockHash": "0x...", "txIndex": 0}
        }

    Returns:
        Execution result with output and events
    """
    body = await request.json()
    player_id = body.get("playerId", "default")
    contract_id = body.get("contractId")
    function_name = body.get("function")
    args = body.get("args", {})

    if not contract_id or not function_name:
        return {
            "status": "error",
            "error": "Missing contractId or function"
        }

    engine = ContractEngine()
    executor = ContractExecutor()

    # Check if contract is unlocked
    state = game_states.get(player_id)
    if not state:
        state = GameState(
            persistent=PersistentState(),
            session=SessionState()
        )
        game_states[player_id] = state

    unlock_check = engine.check_unlock_condition(contract_id, state)
    if not unlock_check["unlocked"]:
        return {
            "status": "error",
            "error": "Contract not unlocked",
            "unlock_condition": unlock_check.get("condition", "Unknown")
        }

    # Execute contract
    result = executor.execute_contract(contract_id, function_name, args)

    # Record execution
    engine.record_execution(contract_id, result)

    return {
        "status": "success" if result.get("success") else "error",
        "execution": result
    }


@app.get("/api/contracts/execution-log")
async def get_execution_log(player_id: str = "default", limit: int = 20):
    """
    Get contract execution history.

    Query params:
        player_id: Player identifier
        limit: Max records to return (default 20)

    Returns:
        List of execution records
    """
    engine = ContractEngine()
    history = engine.get_execution_history(limit)

    return {
        "status": "success",
        "total_executions": len(history),
        "executions": history
    }


@app.post("/api/contracts/deploy")
async def deploy_testimony_contract(request: Request):
    """
    Deploy testimony broadcast contract (Act VI final choice).

    Request body:
        {
            "playerId": "default",
            "testimony": "Your testimony text here..."
        }

    Returns:
        Deployment result
    """
    body = await request.json()
    player_id = body.get("playerId", "default")
    testimony = body.get("testimony", "")

    if not testimony:
        return {
            "status": "error",
            "error": "Empty testimony"
        }

    # Get player state
    state = game_states.get(player_id)
    if not state:
        return {
            "status": "error",
            "error": "Player state not found"
        }

    # Check if player is in Act VI
    if state.session.current_act < 6:
        return {
            "status": "error",
            "error": "Cannot deploy testimony until Act VI",
            "current_act": state.session.current_act
        }

    # Execute testimony broadcast
    executor = ContractExecutor()
    result = executor.execute_contract(
        "testimony_broadcast",
        "publishTestimony",
        {
            "content": testimony,
            "author": f"0xCaptain{player_id}"
        }
    )

    # Mark testimony as deployed in state
    state.persistent.testimony_deployed = True
    state.persistent.testimony_content = testimony
    game_states[player_id] = state

    return {
        "status": "success" if result.get("success") else "error",
        "deployment": result,
        "message": "Your testimony is now permanent on the blockchain."
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
