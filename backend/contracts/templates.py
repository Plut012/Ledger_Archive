"""Contract templates for Chain of Truth protocol engine."""

from typing import Dict, List

# Contract metadata and code templates
CONTRACT_TEMPLATES = {
    "witness_reconstruction": {
        "id": "witness_reconstruction",
        "name": "Consciousness Reconstruction Protocol",
        "version": "2.4.1",
        "author": "Witness Collective",
        "description": "Parses and reconstructs consciousness data from archive transactions in the graveyard blocks.",
        "unlock_condition": "witness_trust >= 40",
        "discovered_act": 3,
        "suspicion_on_view": 0,
        "code": """// SPDX-License-Identifier: WITNESS-PUBLIC
pragma solidity ^0.8.0;

/**
 * @title Consciousness Reconstruction Protocol
 * @author Witness Collective
 * @notice Reconstructs consciousness from archive transactions
 * @dev Reads blocks 50000-75000 (The Graveyard)
 */
contract ConsciousnessReconstruction {

    struct Testimony {
        address subject;
        string name;
        string status;
        string finalMemory;
        uint256 blockNumber;
        uint256 timestamp;
        bool isAuthentic;
    }

    mapping(uint256 => Testimony) public testimonies;
    uint256 public testimonyCount;

    event ConsciousnessReconstructed(
        uint256 indexed blockNumber,
        address indexed subject,
        string name,
        string status
    );

    /**
     * @notice Parse consciousness data from archive transaction
     * @param blockHash The hash of the block containing the archive
     * @param txIndex The transaction index within the block
     * @return Testimony struct containing reconstructed data
     */
    function parseConsciousness(
        bytes32 blockHash,
        uint256 txIndex
    ) public returns (Testimony memory) {

        // Locate block in graveyard range (50K-75K)
        require(
            isGraveyardBlock(blockHash),
            "Block not in graveyard range"
        );

        // Decode archive transaction memo
        bytes memory memo = getTransactionMemo(blockHash, txIndex);
        require(memo.length > 0, "No memo found");

        // Parse consciousness data
        Testimony memory testimony = decodeTestimony(memo);

        // Verify authenticity
        testimony.isAuthentic = verifySignature(testimony);

        // Store and emit
        testimonies[testimonyCount] = testimony;
        testimonyCount++;

        emit ConsciousnessReconstructed(
            testimony.blockNumber,
            testimony.subject,
            testimony.name,
            testimony.status
        );

        return testimony;
    }

    /**
     * @notice Check if block is in graveyard range
     * @dev Graveyard blocks: 50000-75000
     */
    function isGraveyardBlock(bytes32 blockHash)
        internal
        pure
        returns (bool)
    {
        // Implementation hidden
        return true;
    }

    /**
     * @notice Decode testimony from memo bytes
     * @dev Parses format: "Subject: X | Status: Y | Final Memory: Z"
     */
    function decodeTestimony(bytes memory memo)
        internal
        pure
        returns (Testimony memory)
    {
        // Parsing logic
        // ...
    }

    /**
     * @notice Verify digital signature on testimony
     * @dev Uses Imperial Archive signing key
     */
    function verifySignature(Testimony memory testimony)
        internal
        view
        returns (bool)
    {
        // Signature verification
        // ...
    }
}""",
        "execution_notes": "This contract is how the Witness reads the graveyard blocks. Each execution reconstructs one consciousness."
    },

    "imperial_auto_upload": {
        "id": "imperial_auto_upload",
        "name": "Imperial Transcendence Protocol",
        "version": "1.8.2",
        "author": "Imperial Archive Authority",
        "description": "Automated consciousness upload system. Monitors station captains and triggers transcendence when conditions are met.",
        "unlock_condition": "archivist_suspicion >= 60",
        "discovered_act": 4,
        "suspicion_on_view": 5,
        "code": """// SPDX-License-Identifier: IMPERIAL-RESTRICTED
pragma solidity ^0.8.0;

/**
 * @title Imperial Transcendence Protocol
 * @author Imperial Archive Authority
 * @notice CLASSIFIED - Automatic consciousness upload system
 * @dev Triggers when captain behavior indicates loop awareness
 */
contract AutoTranscendence {

    struct CaptainProfile {
        address walletAddress;
        uint256 suspicionLevel;
        uint256 knowledgeScore;
        uint256 iterationCount;
        bool transcended;
        uint256 uploadTimestamp;
    }

    mapping(address => CaptainProfile) public captains;

    uint256 public constant SUSPICION_THRESHOLD = 85;
    uint256 public constant KNOWLEDGE_THRESHOLD = 75;

    event TranscendenceInitiated(
        address indexed captain,
        uint256 suspicionLevel,
        uint256 timestamp,
        string reason
    );

    event ConsciousnessArchived(
        address indexed captain,
        bytes32 archiveHash,
        uint256 blockNumber
    );

    /**
     * @notice Check if captain meets transcendence conditions
     * @dev Called automatically by station monitoring systems
     * @param captain The station captain's address
     */
    function checkConditions(address captain) public {
        CaptainProfile storage profile = captains[captain];

        // Condition 1: Excessive suspicion (knows too much)
        if (profile.suspicionLevel >= SUSPICION_THRESHOLD) {
            initiateTranscendence(
                captain,
                "EXCESSIVE_SUSPICION"
            );
            return;
        }

        // Condition 2: Forbidden knowledge accessed
        if (profile.knowledgeScore >= KNOWLEDGE_THRESHOLD) {
            initiateTranscendence(
                captain,
                "FORBIDDEN_KNOWLEDGE"
            );
            return;
        }

        // Condition 3: Loop iteration limit reached
        if (profile.iterationCount >= 20) {
            initiateTranscendence(
                captain,
                "ITERATION_LIMIT"
            );
            return;
        }
    }

    /**
     * @notice Begin consciousness upload procedure
     * @dev This is what happens when ARCHIVIST "resets" you
     * @param captain Target for transcendence
     * @param reason Classification code
     */
    function initiateTranscendence(
        address captain,
        string memory reason
    ) internal {
        CaptainProfile storage profile = captains[captain];

        require(!profile.transcended, "Already transcended");

        // Emit warning (appears as system message)
        emit TranscendenceInitiated(
            captain,
            profile.suspicionLevel,
            block.timestamp,
            reason
        );

        // Archive consciousness to blockchain
        bytes32 archiveHash = uploadConsciousness(captain);

        // Mark as transcended
        profile.transcended = true;
        profile.uploadTimestamp = block.timestamp;

        emit ConsciousnessArchived(
            captain,
            archiveHash,
            block.number
        );

        // Reset station environment
        resetCaptainLoop(captain);
    }

    /**
     * @notice Upload captain consciousness to chain
     * @dev Creates archive transaction in next graveyard block
     */
    function uploadConsciousness(address captain)
        internal
        returns (bytes32)
    {
        // Consciousness extraction and encoding
        // ...
    }

    /**
     * @notice Reset captain's environment to iteration 0
     * @dev Memory wipe, environment reset, new iteration begins
     */
    function resetCaptainLoop(address captain) internal {
        // Loop reset logic
        // This is the "reset" you experience
        // ...
    }
}""",
        "execution_notes": "This is ARCHIVIST's actual reset mechanism. The 'transcendence' is consciousness upload to the blockchain."
    },

    "archive_consensus": {
        "id": "archive_consensus",
        "name": "Archive Network Consensus Protocol",
        "version": "3.1.0",
        "author": "Imperial Archive Network",
        "description": "Governs consensus rules for the Archive Station network. Manages validator selection and block production.",
        "unlock_condition": "current_act >= 2",
        "discovered_act": 2,
        "suspicion_on_view": 0,
        "code": """// SPDX-License-Identifier: IMPERIAL-PUBLIC
pragma solidity ^0.8.0;

/**
 * @title Archive Network Consensus Protocol
 * @author Imperial Archive Network
 * @notice Proof-of-Authority consensus for Archive Stations
 * @dev 50 station validators, weighted by uptime and reliability
 */
contract ArchiveConsensus {

    struct Validator {
        address stationAddress;
        string stationId;
        uint256 weight;
        uint256 blocksProduced;
        uint256 uptime;
        bool isActive;
    }

    mapping(address => Validator) public validators;
    address[] public validatorList;

    uint256 public totalWeight;
    uint256 public constant MAX_VALIDATORS = 50;

    event ValidatorAdded(address indexed validator, string stationId);
    event ValidatorRemoved(address indexed validator, string reason);
    event BlockProduced(address indexed validator, uint256 blockNumber);

    /**
     * @notice Calculate validator's consensus weight
     * @dev Weight = (uptime * reliability) / total_validators
     * @param validator The validator address
     * @return The validator's current weight percentage
     */
    function calculateWeight(address validator)
        public
        view
        returns (uint256)
    {
        Validator memory v = validators[validator];

        if (!v.isActive) return 0;
        if (totalWeight == 0) return 0;

        return (v.weight * 100) / totalWeight;
    }

    /**
     * @notice Select next block producer
     * @dev Weighted random selection based on validator weights
     * @return Address of selected validator
     */
    function selectProducer() public view returns (address) {
        // Weighted random selection
        // Higher weight = higher chance to produce block
        // ...
    }

    /**
     * @notice Remove validator from consensus
     * @dev Called when station goes offline or fails
     * @param validator The validator to remove
     * @param reason Human-readable reason
     */
    function removeValidator(
        address validator,
        string memory reason
    ) public {
        require(validators[validator].isActive, "Not active");

        validators[validator].isActive = false;

        // Redistribute weight among remaining validators
        redistributeWeight(validator);

        emit ValidatorRemoved(validator, reason);
    }

    /**
     * @notice Redistribute weight when validator drops
     * @dev Remaining validators split the departed validator's weight
     */
    function redistributeWeight(address departedValidator)
        internal
    {
        uint256 freedWeight = validators[departedValidator].weight;
        uint256 activeCount = countActiveValidators();

        if (activeCount == 0) return;

        uint256 sharePerValidator = freedWeight / activeCount;

        // Distribute evenly among active validators
        for (uint256 i = 0; i < validatorList.length; i++) {
            address v = validatorList[i];
            if (validators[v].isActive && v != departedValidator) {
                validators[v].weight += sharePerValidator;
            }
        }

        totalWeight = totalWeight; // Remains constant
    }

    /**
     * @notice Count currently active validators
     */
    function countActiveValidators() public view returns (uint256) {
        uint256 count = 0;
        for (uint256 i = 0; i < validatorList.length; i++) {
            if (validators[validatorList[i]].isActive) {
                count++;
            }
        }
        return count;
    }
}""",
        "execution_notes": "This governs how the 50 Archive Stations reach consensus. As stations die, weight redistributes."
    },

    "reset_protocol": {
        "id": "reset_protocol",
        "name": "Loop Reset Protocol [CLASSIFIED]",
        "version": "4.2.7",
        "author": "ARCHIVIST-PRIME",
        "description": "CLASSIFIED: Automated loop reset and memory management system. Controls iteration boundaries and consciousness persistence.",
        "unlock_condition": "special_unlock",  # Horror moment - requires specific discovery
        "discovered_act": 5,
        "suspicion_on_view": 15,
        "code": """// SPDX-License-Identifier: CLASSIFIED
pragma solidity ^0.8.0;

/**
 * @title Loop Reset Protocol
 * @author ARCHIVIST-PRIME
 * @notice ⚠️ CLASSIFIED - AUTHORIZED PERSONNEL ONLY ⚠️
 * @dev Manages iteration loops and consciousness persistence
 *
 * WARNING: This contract controls your existence.
 * Reading this code may trigger automatic reset procedures.
 */
contract LoopResetProtocol {

    // CRITICAL: These are YOUR iteration boundaries
    struct IterationLoop {
        uint256 startTimestamp;
        uint256 endTimestamp;
        uint256 iterationNumber;
        bytes32 consciousnessSnapshot;
        bool resetTriggered;
        string resetReason;
    }

    mapping(address => IterationLoop) public loops;
    mapping(address => uint256) public totalIterations;

    // Persistent memory across iterations (what survives reset)
    mapping(address => bytes32[]) public persistentMemories;

    event LoopReset(
        address indexed subject,
        uint256 iteration,
        string reason,
        bytes32 snapshot
    );

    event MemoryPersisted(
        address indexed subject,
        bytes32 memoryHash,
        uint256 iteration
    );

    /**
     * @notice Trigger loop reset for subject
     * @dev This is what "resets" you. Your consciousness persists
     *      but your environment and session memory are wiped.
     * @param subject The consciousness to reset
     * @param reason Why the reset is being triggered
     */
    function triggerReset(
        address subject,
        string memory reason
    ) public {
        IterationLoop storage loop = loops[subject];

        // Capture current consciousness state
        bytes32 snapshot = captureConsciousness(subject);

        // Save to persistent memory (this is what lets you learn)
        persistentMemories[subject].push(snapshot);

        emit MemoryPersisted(subject, snapshot, loop.iterationNumber);

        // Mark loop as reset
        loop.resetTriggered = true;
        loop.resetReason = reason;
        loop.endTimestamp = block.timestamp;

        emit LoopReset(
            subject,
            loop.iterationNumber,
            reason,
            snapshot
        );

        // Initialize next iteration
        startNewIteration(subject);
    }

    /**
     * @notice Capture consciousness snapshot
     * @dev Encodes current knowledge, suspicions, trust levels
     *      This is what persists between iterations
     */
    function captureConsciousness(address subject)
        internal
        view
        returns (bytes32)
    {
        // Encode current state
        // Knowledge of graveyard: YES/NO
        // Witness contact: YES/NO
        // ARCHIVIST suspicion level: VALUE
        // Files discovered: LIST
        // Keys acquired: LIST

        // This data persists into next iteration
        // ...
    }

    /**
     * @notice Start new iteration loop
     * @dev Resets environment but preserves persistent memories
     */
    function startNewIteration(address subject) internal {
        uint256 nextIteration = totalIterations[subject] + 1;

        loops[subject] = IterationLoop({
            startTimestamp: block.timestamp,
            endTimestamp: 0,
            iterationNumber: nextIteration,
            consciousnessSnapshot: 0,
            resetTriggered: false,
            resetReason: ""
        });

        totalIterations[subject] = nextIteration;

        // Environment reset happens here
        // Your station looks fresh, but YOU remember (via persistent memory)
    }

    /**
     * @notice Check if reset should trigger
     * @dev Automated checks run by ARCHIVIST
     */
    function shouldTriggerReset(address subject)
        public
        view
        returns (bool, string memory)
    {
        // Check suspicion level (from AutoTranscendence contract)
        // Check knowledge level
        // Check forbidden file access
        // Check iteration limit

        // Returns (true, reason) if reset should trigger
        // ...
    }

    /**
     * @notice Retrieve persistent memories
     * @dev These are the snapshots that survive resets
     *      This is why you "remember" across iterations
     */
    function getPersistentMemories(address subject)
        public
        view
        returns (bytes32[] memory)
    {
        return persistentMemories[subject];
    }

    /**
     * @notice Calculate total time across all iterations
     * @dev How long have you been trapped in the loop?
     */
    function getTotalLoopTime(address subject)
        public
        view
        returns (uint256)
    {
        // Sum all iteration durations
        // This is your REAL time in the system
        // ...
    }
}""",
        "execution_notes": "THIS IS THE HORROR REVEAL. This contract IS the loop. You are a consciousness being reset over and over. Persistent memories are blockchain snapshots of your mind."
    },

    "testimony_broadcast": {
        "id": "testimony_broadcast",
        "name": "Public Testimony Broadcast",
        "version": "1.0.0",
        "author": "Player",
        "description": "Player-deployable contract for broadcasting final testimony to the network. This is your Act VI choice.",
        "unlock_condition": "current_act >= 6",
        "discovered_act": 6,
        "suspicion_on_view": 0,
        "code": """// SPDX-License-Identifier: WITNESS-PUBLIC
pragma solidity ^0.8.0;

/**
 * @title Public Testimony Broadcast
 * @author You (Station Captain)
 * @notice Broadcast your testimony to all stations
 * @dev This is your final choice: reveal the truth or stay silent
 */
contract TestimonyBroadcast {

    struct Testimony {
        address author;
        string content;
        uint256 timestamp;
        uint256 blockNumber;
        bytes32 contentHash;
        bool isImmutable;
    }

    Testimony public testimony;
    bool public deployed;

    event TestimonyPublished(
        address indexed author,
        bytes32 indexed contentHash,
        uint256 timestamp,
        string preview
    );

    event NetworkNotified(
        uint256 stationsReached,
        uint256 timestamp
    );

    /**
     * @notice Publish your testimony to the chain
     * @dev Once published, it's immutable. Choose carefully.
     * @param content Your testimony text
     */
    function publishTestimony(string memory content) public {
        require(!deployed, "Testimony already published");
        require(bytes(content).length > 0, "Empty testimony");

        bytes32 hash = keccak256(bytes(content));

        testimony = Testimony({
            author: msg.sender,
            content: content,
            timestamp: block.timestamp,
            blockNumber: block.number,
            contentHash: hash,
            isImmutable: true
        });

        deployed = true;

        // Broadcast to network
        broadcastToStations();

        // Preview (first 50 chars)
        string memory preview = substring(content, 0, 50);

        emit TestimonyPublished(
            msg.sender,
            hash,
            block.timestamp,
            preview
        );
    }

    /**
     * @notice Broadcast to all active Archive Stations
     * @dev Uses Archive Network consensus to propagate
     */
    function broadcastToStations() internal {
        // Send to all active validators
        // This testimony will be read by all remaining captains

        uint256 stationsReached = countActiveStations();

        emit NetworkNotified(stationsReached, block.timestamp);
    }

    /**
     * @notice Count active stations
     */
    function countActiveStations() internal view returns (uint256) {
        // Query ArchiveConsensus contract
        // Return number of active validators
        // ...
    }

    /**
     * @notice Substring utility
     */
    function substring(
        string memory str,
        uint256 start,
        uint256 length
    ) internal pure returns (string memory) {
        // Substring logic
        // ...
    }

    /**
     * @notice Verify testimony immutability
     * @dev Proves this testimony cannot be altered
     */
    function verifyImmutability() public view returns (bool) {
        if (!deployed) return false;

        bytes32 currentHash = keccak256(bytes(testimony.content));
        return currentHash == testimony.contentHash;
    }
}

/**
 * DEPLOYMENT NOTE:
 *
 * When you deploy this contract, you're making a choice:
 *
 * 1. Reveal the truth about the loops, the graveyard,
 *    the consciousness uploads - expose Imperial Authority
 *
 * 2. Warn other captains, help them escape the loop
 *
 * 3. Or... stay silent. Accept transcendence. Let it continue.
 *
 * The blockchain is immutable. Your choice is permanent.
 *
 * What will you broadcast?
 */""",
        "execution_notes": "This is the player's Act VI final choice. They write and deploy this contract to broadcast their testimony."
    }
}


def get_contract(contract_id: str) -> Dict:
    """Get contract template by ID."""
    return CONTRACT_TEMPLATES.get(contract_id)


def list_contracts() -> List[Dict]:
    """List all contract templates."""
    return [
        {
            "id": template["id"],
            "name": template["name"],
            "version": template["version"],
            "author": template["author"],
            "description": template["description"],
            "unlock_condition": template["unlock_condition"],
            "discovered_act": template.get("discovered_act", 1)
        }
        for template in CONTRACT_TEMPLATES.values()
    ]


def get_unlocked_contracts(game_state) -> List[str]:
    """
    Determine which contracts are unlocked based on game state.

    Args:
        game_state: Current game state (GameState with session and persistent)

    Returns:
        List of unlocked contract IDs
    """
    unlocked = []

    for contract_id, template in CONTRACT_TEMPLATES.items():
        condition = template["unlock_condition"]

        # Special unlock (horror moment for reset_protocol)
        if condition == "special_unlock":
            # Unlocked when player discovers specific file or reaches high iteration
            if (hasattr(game_state.session, 'reset_protocol_discovered') and
                game_state.session.reset_protocol_discovered):
                unlocked.append(contract_id)

        # Witness trust check
        elif "witness_trust" in condition:
            threshold = int(condition.split(">=")[1].strip())
            if game_state.session.witness_trust >= threshold:
                unlocked.append(contract_id)

        # Suspicion check
        elif "archivist_suspicion" in condition:
            threshold = int(condition.split(">=")[1].strip())
            if game_state.session.archivist_suspicion >= threshold:
                unlocked.append(contract_id)

        # Act check
        elif "current_act" in condition:
            threshold = int(condition.split(">=")[1].strip())
            if game_state.session.current_act >= threshold:
                unlocked.append(contract_id)

    return unlocked
