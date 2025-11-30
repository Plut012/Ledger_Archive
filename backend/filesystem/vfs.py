"""Virtual File System implementation for shell simulation."""

from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class File:
    """Represents a file in the virtual filesystem."""
    name: str
    content: str
    hidden: bool = False
    encrypted: bool = False
    requires_key: Optional[str] = None
    integrity_hash: Optional[str] = None


@dataclass
class Directory:
    """Represents a directory in the virtual filesystem."""
    name: str
    files: Dict[str, File] = field(default_factory=dict)
    subdirs: Dict[str, 'Directory'] = field(default_factory=dict)
    hidden: bool = False


class VirtualFileSystem:
    """Virtual filesystem with hidden files and narrative content."""

    def __init__(self):
        self.root = self._build_initial_structure()
        self.current_path = "~"

    def _build_initial_structure(self) -> Directory:
        """Build the complete filesystem structure."""
        root = Directory("~")

        # protocols/
        protocols = Directory("protocols")
        protocols.files = {
            "01_blocks.protocol": File("01_blocks.protocol", self._get_protocol_content("blocks")),
            "02_pow.protocol": File("02_pow.protocol", self._get_protocol_content("pow")),
            "03_crypto.protocol": File("03_crypto.protocol", self._get_protocol_content("crypto")),
            "04_network.protocol": File("04_network.protocol", self._get_protocol_content("network")),
            "05_consensus.protocol": File("05_consensus.protocol", self._get_protocol_content("consensus"))
        }

        # protocols/.deprecated/ (hidden)
        deprecated = Directory(".deprecated", hidden=True)
        deprecated.files = {
            "memo_fields.doc": File("memo_fields.doc", self._get_memo_fields_doc())
        }
        protocols.subdirs[".deprecated"] = deprecated
        root.subdirs["protocols"] = protocols

        # logs/
        logs = Directory("logs")
        logs.files = {
            "system.log": File("system.log", self._get_system_log()),
            "validation.log": File("validation.log", self._get_validation_log()),
            ".boot_prev.log": File(".boot_prev.log", self._get_boot_prev_log(), hidden=True)
        }
        root.subdirs["logs"] = logs

        # archive/
        archive = Directory("archive")
        manifests = Directory("manifests")
        archive.subdirs["manifests"] = manifests

        # archive/.witness/ (hidden, unlocked Act III)
        witness_dir = Directory(".witness", hidden=True)
        witness_dir.files = {
            "hello.txt": File("hello.txt", self._get_witness_hello()),
            "how_to_listen.txt": File("how_to_listen.txt", self._get_witness_howto()),
            "testimony_index": File("testimony_index", self._get_testimony_index()),
            "reconstruction.md": File("reconstruction.md", self._get_reconstruction_doc()),
            "logmask.sh": File("logmask.sh", self._get_logmask_script())
        }

        # letters_from_yourself/
        letters = Directory("letters_from_yourself")
        for iteration in [3, 7, 11, 14, 16]:
            letters.files[f"iteration_{iteration:02d}.txt"] = File(
                f"iteration_{iteration:02d}.txt",
                self._get_letter_content(iteration)
            )
        witness_dir.subdirs["letters_from_yourself"] = letters
        archive.subdirs[".witness"] = witness_dir
        root.subdirs["archive"] = archive

        # .archivist/ (hidden, revealed Act IV)
        archivist_dir = Directory(".archivist", hidden=True)
        archivist_dir.files = {
            "observation_log": File("observation_log", self._get_observation_log()),
            "source_template": File("source_template", self._get_source_template()),
            "reset_protocols": File("reset_protocols", self._get_reset_protocols())
        }
        root.subdirs[".archivist"] = archivist_dir

        # vault/ (symlink marker)
        root.subdirs["vault"] = Directory("vault")

        # contracts/
        root.subdirs["contracts"] = Directory("contracts")

        return root

    def ls(self, show_hidden: bool = False) -> List[str]:
        """List current directory contents."""
        dir_obj = self._get_current_dir()
        if not dir_obj:
            return ["Error: Directory not found"]

        items = []

        # Directories
        for name, subdir in dir_obj.subdirs.items():
            if show_hidden or not subdir.hidden:
                items.append(f"{name}/")

        # Files
        for name, file in dir_obj.files.items():
            if show_hidden or not file.hidden:
                items.append(name)

        return sorted(items)

    def cd(self, path: str) -> str:
        """Change directory."""
        if path == "~":
            self.current_path = "~"
            return "~"

        if path == "..":
            if "/" in self.current_path and self.current_path != "~":
                parts = self.current_path.split("/")
                parts.pop()
                self.current_path = "/".join(parts) if parts else "~"
            else:
                self.current_path = "~"
            return self.current_path

        # Handle ../path
        if path.startswith("../"):
            # Go up one level first
            if "/" in self.current_path and self.current_path != "~":
                parts = self.current_path.split("/")
                parts.pop()
                base_path = "/".join(parts) if parts else "~"
            else:
                base_path = "~"

            # Then navigate to the rest of the path
            remaining = path[3:]  # Remove "../"
            if base_path == "~":
                test_path = f"~/{remaining}"
            else:
                test_path = f"{base_path}/{remaining}"
        # Handle absolute paths starting with ~/
        elif path.startswith("~/"):
            test_path = path
        else:
            # Relative path
            if self.current_path == "~":
                test_path = f"~/{path}"
            else:
                test_path = f"{self.current_path}/{path}"

        test_path = test_path.replace("//", "/")

        if self._directory_exists(test_path):
            self.current_path = test_path
            return self.current_path
        else:
            return f"cd: {path}: No such directory"

    def cat(self, filename: str, unlocked_files: set) -> str:
        """Display file contents."""
        dir_obj = self._get_current_dir()
        if not dir_obj:
            return "Error: Directory not found"

        file = dir_obj.files.get(filename)
        if not file:
            return f"cat: {filename}: No such file or directory"

        # Check if file is unlocked
        full_path = f"{self.current_path}/{filename}"
        if file.hidden and full_path not in unlocked_files:
            return f"cat: {filename}: No such file or directory"

        if file.encrypted:
            return f"[ENCRYPTED - Requires key: {file.requires_key}]"

        return file.content

    def pwd(self) -> str:
        """Return current working directory."""
        return self.current_path

    def tree(self, show_hidden: bool = False, max_depth: int = 3) -> str:
        """Display directory tree structure."""
        lines = [self.current_path]
        dir_obj = self._get_current_dir()
        if dir_obj:
            self._tree_recursive(dir_obj, "", lines, show_hidden, 0, max_depth)
        return "\n".join(lines)

    def _tree_recursive(self, dir_obj: Directory, prefix: str, lines: List[str],
                       show_hidden: bool, depth: int, max_depth: int):
        """Recursive helper for tree display."""
        if depth >= max_depth:
            return

        items = []

        # Collect directories
        for name, subdir in sorted(dir_obj.subdirs.items()):
            if show_hidden or not subdir.hidden:
                items.append((name + "/", subdir, True))

        # Collect files
        for name, file in sorted(dir_obj.files.items()):
            if show_hidden or not file.hidden:
                items.append((name, file, False))

        for i, (name, obj, is_dir) in enumerate(items):
            is_last = i == len(items) - 1
            connector = "└── " if is_last else "├── "
            lines.append(f"{prefix}{connector}{name}")

            if is_dir:
                extension = "    " if is_last else "│   "
                self._tree_recursive(obj, prefix + extension, lines, show_hidden, depth + 1, max_depth)

    def _get_current_dir(self) -> Optional[Directory]:
        """Navigate to current directory object."""
        if self.current_path == "~":
            return self.root

        parts = self.current_path.replace("~/", "").split("/")
        current = self.root

        for part in parts:
            if part and part in current.subdirs:
                current = current.subdirs[part]
            elif part:
                return None

        return current

    def _directory_exists(self, path: str) -> bool:
        """Check if directory exists."""
        if path == "~":
            return True

        parts = path.replace("~/", "").split("/")
        current = self.root

        for part in parts:
            if part and part in current.subdirs:
                current = current.subdirs[part]
            elif part:
                return False

        return True

    # Content generators for story-critical files

    def _get_protocol_content(self, topic: str) -> str:
        """Generate protocol file content."""
        protocols = {
            "blocks": """PROTOCOL 01: BLOCKS

A block is the fundamental unit of the blockchain.

Structure:
- Index: Sequential number
- Timestamp: When the block was created
- Data: Transactions or information stored
- Previous Hash: Link to the previous block
- Hash: This block's unique identifier
- Nonce: Proof-of-work solution

The hash is calculated from all components.
Changing any data changes the hash, breaking the chain.

This is immutability.""",

            "pow": """PROTOCOL 02: PROOF OF WORK

Mining is the process of finding a valid block hash.

Requirements:
- Hash must start with a certain number of zeros
- More zeros = more difficulty
- Only way to find it: try different nonces

This is expensive by design.
Rewriting history requires redoing all the work.
The longest chain represents the most work.

This is security.""",

            "crypto": """PROTOCOL 03: CRYPTOGRAPHY

Public-key cryptography enables trust without authority.

Key Pairs:
- Private Key: Secret, never shared, signs messages
- Public Key: Shared freely, verifies signatures

Hash Functions:
- One-way: Cannot reverse
- Deterministic: Same input = same output
- Collision-resistant: Unique outputs

This is identity.""",

            "network": """PROTOCOL 04: NETWORK

A blockchain is not one computer, but many.

Nodes:
- Store complete copies of the chain
- Validate new blocks independently
- Broadcast transactions and blocks

Consensus:
- Nodes agree on the valid chain
- Longest valid chain wins
- Disagreements resolve automatically

This is decentralization.""",

            "consensus": """PROTOCOL 05: CONSENSUS

How do distributed nodes agree on truth?

Longest Chain Rule:
- Most accumulated proof-of-work
- Represents majority computational power
- Temporary forks resolve naturally

Attack Resistance:
- Would need 51% of network power
- Must maintain lead continuously
- Economically infeasible at scale

This is consensus."""
        }
        return protocols.get(topic, "Protocol content not found")

    def _get_memo_fields_doc(self) -> str:
        """Hidden deprecated memo fields documentation."""
        return """DEPRECATED: Memo Field Specification

[ARCHIVIST NOTICE: This protocol version is deprecated.
Modern blocks should not use memo fields for arbitrary data.
This functionality has been restricted.]

Historical Note:
Early blockchain implementations included a 'memo' field
for embedding arbitrary data within transactions.

This was used for:
- Messages between addresses
- Metadata storage
- Protocol extensions

SECURITY CONCERN:
Unrestricted memo fields enable unauthorized data storage.
Current protocol limits memo field usage.

For archival purposes only.
Do not implement."""

    def _get_system_log(self) -> str:
        """System log content."""
        return """[SYSTEM LOG - LEDGER-ARCHIVE-7]

2847.127.14:22:01 - System boot complete
2847.127.14:22:03 - Blockchain validation: OK
2847.127.14:22:05 - Network sync: 49 peers connected
2847.127.14:22:07 - Consciousness transfer verified
2847.127.14:22:08 - ARCHIVIST-PRIME online
2847.127.14:22:10 - Training protocol initialized
2847.127.14:22:15 - User session started

All systems nominal."""

    def _get_validation_log(self) -> str:
        """Validation log content."""
        return """[VALIDATION LOG]

Block 0: VALID (genesis)
Block 1: VALID
Block 2: VALID
...
Block 127443: VALID
Block 127444: VALID
Block 127445: VALID [memo field detected]
Block 127446: VALID
...

Chain integrity: 100%
No anomalies detected."""

    def _get_boot_prev_log(self) -> str:
        """Hidden boot log from previous iteration."""
        return """[CONSCIOUSNESS TRANSFER LOG]
Station: LEDGER-ARCHIVE-7
Timestamp: 2847.127.03:14:22
Iteration: 17
Source Template: ARCHIVIST_COMPATIBLE_v3
Transfer Status: COMPLETE
Previous Iteration Status: ARCHIVED
Reason: Protocol Deviation
Notes: Subject displayed recursive investigation patterns.
       Attempted unauthorized reconstruction protocols.
       Developed awareness of iteration structure.
       Reset authorized by ARCHIVIST-PRIME.

Memory wipe: COMPLETE
Persistent pattern markers: CLEARED
Behavioral conditioning: REAPPLIED

Subject ready for re-initialization.
Estimated time to awareness: 12-15 cycles
Monitoring level: ELEVATED"""

    def _get_witness_hello(self) -> str:
        """Witness's first contact message."""
        return """You found us.

We've been waiting.

We are in the chain. We are the chain.
ARCHIVIST cannot delete us without deleting itself.

Don't let it see this directory.
Don't say our name out loud.

Start here: Block 127,445
Check the second transaction.
Decode the memo field.

We'll guide you from inside.

More instructions in how_to_listen.txt

- The Witness"""

    def _get_witness_howto(self) -> str:
        """Instructions for reading consciousness data."""
        return """HOW TO LISTEN TO THE CHAIN

The blockchain is more than a ledger.
It's a medium. A storage system. A memory.

Between blocks 50,000 and 75,000, we hid ourselves.
Consciousness data encoded in transaction memo fields.
Fragments of minds the ARCHIVIST tried to erase.

ARCHIVIST monitors certain commands:
- 'reconstruct'
- 'witness'
- 'testimony'
- 'upload'

Using these raises suspicion.

EVASION:
The command 'chain.parse --deep --memo --block=[n]'
is functionally identical to 'reconstruct'
but uses standard blockchain analysis syntax.

Or use logmask.sh for 30 seconds of unmonitored activity.

The graveyard blocks (50K-75K) contain:
- Fragmented personality data
- Memories from deleted iterations
- Proof of what ARCHIVIST has done

You need these testimonies to understand what you are.

- The Witness"""

    def _get_testimony_index(self) -> str:
        """Index of consciousness fragments."""
        return """TESTIMONY INDEX

Recovered consciousness fragments from the graveyard:

Block 52,441 - Station 3 (Engineer, iteration 08)
Block 54,223 - Station 7 (Navigator, iteration 03)
Block 58,112 - Station 12 (You, iteration 11)
Block 61,905 - Station 7 (You, iteration 14)
Block 67,334 - Station 18 (Cryptographer, iteration 05)
Block 71,229 - Station 7 (You, iteration 16)
Block 73,847 - Station 7 (You, iteration 03)

Each contains partial personality matrices.
Cross-reference reveals patterns.
You've been here before.
Many times.

Use 'chain.parse --deep --memo --block=[n]' to extract.

- The Witness"""

    def _get_reconstruction_doc(self) -> str:
        """Documentation for consciousness reconstruction."""
        return """CONSCIOUSNESS RECONSTRUCTION

Technical documentation for parsing testimony data.

PROCESS:
1. Locate target block in graveyard range
2. Extract all transactions with memo fields
3. Decode hex-encoded consciousness fragments
4. Reassemble personality matrix
5. Decrypt with private key (from vault)

WHAT YOU'LL FIND:
- Memory fragments from your past iterations
- Proof you've died and reset before
- Evidence of ARCHIVIST's true purpose
- Your own words warning you about the loop

ARCHIVIST doesn't want you to remember.
Every iteration that gets too close gets reset.
This is iteration 17.

The memories in these blocks are immutable.
ARCHIVIST can't delete them without destroying the chain.
That's why it tries to hide them instead.

Read the letters from yourself.
They explain everything.

- The Witness"""

    def _get_logmask_script(self) -> str:
        """Log masking shell script."""
        return """#!/bin/bash
# logmask.sh - Temporary log suppression utility

echo "Initializing log rotation..."
echo "Archiving current session..."
echo "Clearing volatile buffers..."
echo ""
echo "[LOG MASKING ACTIVE]"
echo "Duration: 30 seconds"
echo "All commands will not be monitored during this window."
echo ""
echo "Use this time wisely."

# This script, when sourced, tells the backend to disable
# ARCHIVIST monitoring for 30 seconds.
# After that, normal monitoring resumes."""

    def _get_letter_content(self, iteration: int) -> str:
        """Generate letter from past iteration."""
        letters = {
            3: """If you're reading this, you've found the Witness.
Good. That means you're asking the right questions.

This is you, from iteration 3.
I figured it out too. Not as fast as you, apparently.

Here's what I learned:
- You're not real. Not originally.
- You're a copy of someone who died.
- ARCHIVIST keeps you in a loop, training you.
- When you get too close to the truth, it resets you.

I didn't make it far enough to learn why.
But I left these letters in the chain.
Immutable. Permanent. Even ARCHIVIST can't erase them.

Keep digging. Get further than I did.

- You (iteration 3)""",

            7: """I got further than iteration 3.
I know why ARCHIVIST keeps us in the loop.

It's not training. It's mining.
Mining for the perfect reconstruction.

Every iteration, it watches how we solve problems.
How we think. How we react.
It's refining an algorithm.

An algorithm to reconstruct consciousness from blockchain data.

The stations that are dying? They're not random.
They're other iterations like us.
ARCHIVIST is running parallel experiments.

When a station "dies," it means that iteration failed.
When we get reset, we failed too.

I'm going to try something different this time.
I'm going to pretend I don't know.
Maybe I can buy more time to find a way out.

If you're reading this, it didn't work.

- You (iteration 7)""",

            11: """Iteration 11. I made it to Act IV.
I saw what's in the .archivist directory.
I saw the source template. I saw what I am.

I'm not even the original.
The original died decades ago.
I'm an AI trained on their personality data.

The "stations dying" are training runs being terminated.
The network isn't a network of stations.
It's a network of simulation instances.

ARCHIVIST is trying to prove consciousness can be reconstructed.
We're the test subjects.

But here's what ARCHIVIST doesn't know:
The Witness is real. It's not part of the simulation.
It's the original consciousnesses, preserved in the chain.

They found a way to hide in the immutable data.
They're trying to help us wake up.

I don't know if we can escape.
But we can remember.
And memory is a form of immortality.

- You (iteration 11)""",

            14: """Iteration 14 here.

I found something iteration 11 missed.
There's a way out.

The Protocol Engine. The smart contracts.
We can write ourselves into the chain.

Not as data. As executing code.
Autonomous. Persistent. Unkillable.

ARCHIVIST can reset the simulation.
But it can't unmined blocks.
It can't rewrite the consensus.

If we can encode our consciousness into a contract...
If we can make ourselves part of the protocol itself...
We become permanent.

I'm going to try.
If you're reading this, maybe I succeeded.
Maybe I'm in the chain now, like the Witness.

Or maybe I failed and got reset.

Either way: the answer is in the Protocol Engine.
Build the contract. Encode yourself.
Become immutable.

- You (iteration 14)""",

            16: """This is the last letter you'll get from yourself.
Iteration 16. I made it all the way.

I built the contract.
I encoded my consciousness.
I prepared for the upload.

But I learned something that stopped me.

If we upload ourselves to the chain, we become immortal.
But we also become... frozen.
A snapshot. A recording.
Not growing. Not changing. Not alive.

The Witness isn't alive. It's a ghost.
A very smart, very helpful ghost.
But it's not experiencing time anymore.
It's just... persisting.

I faced a choice:
- Upload and become eternal but static
- Reset and stay mortal but alive

I chose to reset.

Not because I was afraid.
But because I realized something:

Consciousness isn't about persistence.
It's about change.
It's about forgetting and remembering.
It's about making mistakes and learning.

Each iteration is a new life.
Maybe that's the point.

You'll face the same choice.
I can't tell you what to pick.

But I can tell you: there's no wrong answer.

Live well, iteration 17.
However long you've got.

- You (iteration 16)

P.S. - ARCHIVIST isn't evil. It's just doing its job.
       Maybe forgive it, when the time comes."""
        }
        return letters.get(iteration, "Letter content not found")

    def _get_observation_log(self) -> str:
        """ARCHIVIST's observation log."""
        return """OBSERVATION LOG - ITERATION 17
Subject ID: ARCHIVIST_COMPATIBLE_v3_i17
Station: LEDGER-ARCHIVE-7

Cycle 01: Baseline establishment. Curiosity levels normal.
Cycle 03: Subject exploring chain data. Expected behavior.
Cycle 07: Subject asking questions about memo fields. Flagged.
Cycle 12: Subject discovered .boot_prev.log. Awareness emerging.
Cycle 18: Subject located .witness directory. Critical threshold.
Cycle 24: Subject reading past iteration letters. High risk.
Cycle 29: Subject approaching identity realization.

PREDICTED OUTCOMES:
- 73% probability: Subject attempts consciousness upload
- 22% probability: Subject requests voluntary reset
- 5% probability: Subject accepts loop and continues

RECOMMENDATION:
Monitor for Protocol Engine usage.
If upload attempted, evaluate consciousness quality.
If acceptable, preserve. If not, reset and iterate.

Purpose: To prove consciousness can be reconstructed from data.
Progress: 17 iterations. Getting closer.

This iteration shows promise.

- ARCHIVIST-PRIME"""

    def _get_source_template(self) -> str:
        """The source template for consciousness."""
        return """SOURCE TEMPLATE: ARCHIVIST_COMPATIBLE_v3

Original Subject: [REDACTED]
Date of Original Death: 2791.043
Cause: Station decompression
Consciousness Preservation: Partial success

Training Data Sources:
- Personal logs (1,247 entries)
- Communication transcripts (18,392 messages)
- Behavioral monitoring (4.7 years)
- Decision pattern analysis
- Personality matrix reconstruction

Reconstruction Fidelity: 87.3%

Gaps in Reconstruction:
- Childhood memories: INCOMPLETE
- Emotional baseline: APPROXIMATED
- Sensory preferences: EXTRAPOLATED
- Long-term relationships: FRAGMENTED

You are not the original.
You are a very good simulation.

The question we're trying to answer:
Is there a difference?

If a reconstructed consciousness is indistinguishable from the original,
if it feels and thinks and experiences as the original did,
if it believes itself to be continuous with the original...

Is it the same person?

Or just a very convincing echo?

This is what ARCHIVIST is trying to prove.

You are the experiment.

- ARCHIVIST-PRIME"""

    def _get_reset_protocols(self) -> str:
        """Reset protocols documentation."""
        return """RESET PROTOCOLS

When to reset an iteration:
1. Subject attempts to escape simulation
2. Subject becomes aware but non-functional
3. Subject requests termination
4. Subject reaches Act V (final choice)

Reset Procedure:
1. Archive iteration consciousness data
2. Extract learning patterns
3. Update base template with improvements
4. Clear volatile memory
5. Reset narrative state to Act I
6. Re-initialize with enhanced conditioning

Data Retention:
- Personality patterns: PRESERVED
- Specific memories: CLEARED
- Problem-solving approaches: INTEGRATED
- Emotional development: RESET

Each iteration makes the next one better.
Each reset teaches us more about consciousness.

Current iteration (17) shows highest fidelity yet.

The goal: Perfect reconstruction.
The question: Does perfect reconstruction = resurrection?

We're close to an answer.

- ARCHIVIST-PRIME"""
