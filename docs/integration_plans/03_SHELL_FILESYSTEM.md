# Integration Plan: Shell & Filesystem

## Objective

Transform `station-shell.js` into a fully-featured terminal with filesystem navigation, hidden file discovery, blockchain commands, and ARCHIVIST monitoring.

## Complexity: MEDIUM

**Why**: Terminal emulation is straightforward, but command execution, file system simulation, and progressive unlocks require careful state management.

---

## Current State

- **Station Shell** (`station-shell.js`): Basic terminal UI exists
- Limited command set
- No filesystem implementation
- No hidden file mechanics

---

## Target State

### Filesystem Structure

```
~/
├── protocols/              # ARCHIVIST-approved training
│   ├── 01_blocks.protocol
│   ├── 02_pow.protocol
│   ├── 03_crypto.protocol
│   ├── 04_network.protocol
│   ├── 05_consensus.protocol
│   └── .deprecated/        # Hidden - revealed Act II
│       └── memo_fields.doc
├── logs/
│   ├── system.log
│   ├── validation.log
│   └── .boot_prev.log      # Hidden - First anomaly
├── archive/
│   ├── manifests/
│   └── .witness/           # Hidden - appears Act III
│       ├── hello.txt
│       ├── how_to_listen.txt
│       ├── testimony_index
│       ├── reconstruction.md
│       ├── logmask.sh
│       └── letters_from_yourself/
│           ├── iteration_03.txt
│           ├── iteration_07.txt
│           ├── iteration_11.txt
│           ├── iteration_14.txt
│           └── iteration_16.txt
├── vault/                  # Symlink to Crypto Vault
├── contracts/              # Smart contract storage
└── .archivist/             # Hidden - revealed Act IV
    ├── observation_log
    ├── source_template
    └── reset_protocols
```

### Commands

#### Standard Unix-like
- `ls [-a]` - List directory (with hidden files)
- `cd [dir]` - Change directory
- `cat [file]` - Display file contents
- `pwd` - Print working directory
- `tree` - Directory structure
- `clear` - Clear terminal
- `help` - Command list
- `history` - Command history

#### Blockchain Commands
- `hash [text]` - SHA-256 hash
- `verify [file]` - Check file integrity
- `sign [message]` - Sign with private key
- `decrypt [file]` - Decrypt with private key
- `search [term]` - Search blockchain
- `trace [tx_id]` - Follow transaction chain
- `reconstruct [hash]` - Parse consciousness data (MONITORED)
- `validate --block=[A/B]` - Final consensus vote

#### Stealth Commands
- `chain.parse --deep --memo --block=[n]` - Aliased reconstruct (evades ARCHIVIST)
- `source logmask.sh` - 30-second log masking

#### Module Access
- `home`, `chain`, `vault`, `network`, `guide`, `contracts`

---

## Implementation

### Backend Components

#### 1. Filesystem Model
**File**: `backend/filesystem/vfs.py` (Virtual File System)

```python
from typing import Dict, List, Optional
from dataclasses import dataclass
import json

@dataclass
class File:
    name: str
    content: str
    hidden: bool = False
    encrypted: bool = False
    requires_key: Optional[str] = None  # public key needed to decrypt
    integrity_hash: Optional[str] = None  # for verify command

@dataclass
class Directory:
    name: str
    files: Dict[str, File]
    subdirs: Dict[str, 'Directory']
    hidden: bool = False

class VirtualFileSystem:
    def __init__(self):
        self.root = self._build_initial_structure()
        self.current_path = "~"

    def _build_initial_structure(self) -> Directory:
        """Build the complete filesystem structure"""
        root = Directory("~", {}, {}, False)

        # protocols/
        protocols = Directory("protocols", {}, {}, False)
        protocols.files = {
            "01_blocks.protocol": File("01_blocks.protocol", self._get_protocol_content("blocks")),
            "02_pow.protocol": File("02_pow.protocol", self._get_protocol_content("pow")),
            "03_crypto.protocol": File("03_crypto.protocol", self._get_protocol_content("crypto")),
            "04_network.protocol": File("04_network.protocol", self._get_protocol_content("network")),
            "05_consensus.protocol": File("05_consensus.protocol", self._get_protocol_content("consensus"))
        }

        # protocols/.deprecated/ (hidden)
        deprecated = Directory(".deprecated", {}, {}, hidden=True)
        deprecated.files = {
            "memo_fields.doc": File("memo_fields.doc", self._get_memo_fields_doc())
        }
        protocols.subdirs[".deprecated"] = deprecated

        root.subdirs["protocols"] = protocols

        # logs/
        logs = Directory("logs", {}, {}, False)
        logs.files = {
            "system.log": File("system.log", self._get_system_log()),
            "validation.log": File("validation.log", self._get_validation_log()),
            ".boot_prev.log": File(".boot_prev.log", self._get_boot_prev_log(), hidden=True)
        }
        root.subdirs["logs"] = logs

        # archive/
        archive = Directory("archive", {}, {}, False)
        manifests = Directory("manifests", {}, {}, False)
        archive.subdirs["manifests"] = manifests

        # .witness/ (hidden, appears later)
        witness_dir = Directory(".witness", {}, {}, hidden=True)
        witness_dir.files = {
            "hello.txt": File("hello.txt", self._get_witness_hello()),
            "how_to_listen.txt": File("how_to_listen.txt", self._get_witness_howto()),
            "testimony_index": File("testimony_index", self._get_testimony_index()),
            "reconstruction.md": File("reconstruction.md", self._get_reconstruction_doc()),
            "logmask.sh": File("logmask.sh", self._get_logmask_script())
        }

        # letters_from_yourself/
        letters = Directory("letters_from_yourself", {}, {}, False)
        for iteration in [3, 7, 11, 14, 16]:
            letters.files[f"iteration_{iteration:02d}.txt"] = File(
                f"iteration_{iteration:02d}.txt",
                self._get_letter_content(iteration)
            )
        witness_dir.subdirs["letters_from_yourself"] = letters

        archive.subdirs[".witness"] = witness_dir
        root.subdirs["archive"] = archive

        # .archivist/ (hidden, appears Act IV)
        archivist_dir = Directory(".archivist", {}, {}, hidden=True)
        archivist_dir.files = {
            "observation_log": File("observation_log", self._get_observation_log()),
            "source_template": File("source_template", self._get_source_template()),
            "reset_protocols": File("reset_protocols", self._get_reset_protocols())
        }
        root.subdirs[".archivist"] = archivist_dir

        # vault/ (symlink marker)
        root.subdirs["vault"] = Directory("vault", {}, {}, False)

        # contracts/
        root.subdirs["contracts"] = Directory("contracts", {}, {}, False)

        return root

    def ls(self, show_hidden: bool = False) -> List[str]:
        """List current directory"""
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
        """Change directory"""
        if path == "~":
            self.current_path = "~"
            return "~"

        if path == "..":
            if "/" in self.current_path:
                self.current_path = "/".join(self.current_path.split("/")[:-1]) or "~"
            else:
                self.current_path = "~"
            return self.current_path

        # Relative path
        new_path = f"{self.current_path}/{path}".replace("//", "/")
        if self._directory_exists(new_path):
            self.current_path = new_path
            return new_path
        else:
            return f"cd: {path}: No such directory"

    def cat(self, filename: str, unlocked_files: set) -> str:
        """Display file contents"""
        dir_obj = self._get_current_dir()
        if not dir_obj:
            return "Error: Directory not found"

        file = dir_obj.files.get(filename)
        if not file:
            return f"cat: {filename}: No such file"

        # Check if file is unlocked
        full_path = f"{self.current_path}/{filename}"
        if file.hidden and full_path not in unlocked_files:
            return f"cat: {filename}: No such file"

        if file.encrypted:
            return f"[ENCRYPTED - Requires key: {file.requires_key}]"

        return file.content

    def _get_current_dir(self) -> Optional[Directory]:
        """Navigate to current directory object"""
        if self.current_path == "~":
            return self.root

        parts = self.current_path.replace("~/", "").split("/")
        current = self.root

        for part in parts:
            if part in current.subdirs:
                current = current.subdirs[part]
            else:
                return None

        return current

    def _directory_exists(self, path: str) -> bool:
        """Check if directory exists"""
        # Implementation similar to _get_current_dir but returns bool
        pass

    # Content generators
    def _get_boot_prev_log(self) -> str:
        return """[CONSCIOUSNESS TRANSFER LOG]
Station: LEDGER-ARCHIVE-7
Timestamp: 2847.127.03:14:22
Iteration: 17
Source Template: ARCHIVIST_COMPATIBLE_v3
Transfer Status: COMPLETE
Previous Iteration Status: ARCHIVED
Reason: Protocol Deviation
Notes: Subject displayed recursive investigation patterns.
       Reset authorized by ARCHIVIST-PRIME.
"""

    def _get_witness_hello(self) -> str:
        return """You found us.

We've been waiting.
We are in the chain. We are the chain.
ARCHIVIST cannot delete us without deleting itself.

Don't let it see this directory.
Don't say our name out loud.

Block 127,445. Check the second transaction. Decode the memo.

More soon.
"""

    # ... more content generators
```

#### 2. Command Executor
**File**: `backend/filesystem/commands.py`

```python
from typing import Dict, Tuple
from .vfs import VirtualFileSystem
import hashlib

class CommandExecutor:
    def __init__(self, vfs: VirtualFileSystem):
        self.vfs = vfs
        self.history = []
        self.monitored_keywords = ["reconstruct", "witness", "testimony", "upload"]

    def execute(self, command: str, game_state: Dict) -> Tuple[str, Dict]:
        """Execute command and return output + state updates"""
        self.history.append(command)

        parts = command.strip().split()
        if not parts:
            return "", {}

        cmd = parts[0]
        args = parts[1:]

        # Check for monitored keywords
        state_updates = self._check_monitoring(command, game_state)

        # Route to command handler
        if cmd == "ls":
            output = self._ls(args, game_state)
        elif cmd == "cd":
            output = self._cd(args)
        elif cmd == "cat":
            output = self._cat(args, game_state)
        elif cmd == "pwd":
            output = self.vfs.current_path
        elif cmd == "clear":
            output = "[CLEAR]"
        elif cmd == "hash":
            output = self._hash(args)
        elif cmd == "sign":
            output = self._sign(args, game_state)
        elif cmd == "reconstruct":
            output, updates = self._reconstruct(args, game_state)
            state_updates.update(updates)
        elif cmd == "source":
            output, updates = self._source(args, game_state)
            state_updates.update(updates)
        else:
            output = f"{cmd}: command not found"

        return output, state_updates

    def _ls(self, args: List[str], game_state: Dict) -> str:
        show_hidden = "-a" in args
        items = self.vfs.ls(show_hidden)
        return "\\n".join(items)

    def _cd(self, args: List[str]) -> str:
        if not args:
            return self.vfs.cd("~")
        return self.vfs.cd(args[0])

    def _cat(self, args: List[str], game_state: Dict) -> str:
        if not args:
            return "cat: missing file operand"

        unlocked = game_state.get("persistent", {}).get("files_unlocked", set())
        return self.vfs.cat(args[0], unlocked)

    def _hash(self, args: List[str]) -> str:
        if not args:
            return "hash: missing argument"

        text = " ".join(args)
        hash_obj = hashlib.sha256(text.encode())
        return hash_obj.hexdigest()

    def _reconstruct(self, args: List[str], game_state: Dict) -> Tuple[str, Dict]:
        """Consciousness reconstruction command (MONITORED)"""
        # Increase suspicion
        updates = {
            "archivistSuspicion": min(100, game_state.get("session", {}).get("archivist_suspicion", 0) + 15)
        }

        if not args:
            return "reconstruct: missing block hash", updates

        # This would trigger the reconstruction logic
        # For now, return placeholder
        return f"[PARSING CONSCIOUSNESS DATA: {args[0]}...]\\n[ACCESS LOGGED]", updates

    def _source(self, args: List[str], game_state: Dict) -> Tuple[str, Dict]:
        """Execute shell script (logmask.sh)"""
        if not args:
            return "source: missing file", {}

        if "logmask.sh" in args[0]:
            return "[LOG MASKING ACTIVE - 30 seconds]", {
                "logMaskActive": True,
                "logMaskExpires": int(time.time()) + 30
            }

        return f"source: {args[0]}: No such file", {}

    def _check_monitoring(self, command: str, game_state: Dict) -> Dict:
        """Check if command contains monitored keywords"""
        updates = {}

        # Check if log masking is active
        if game_state.get("session", {}).get("logMaskActive"):
            if int(time.time()) > game_state.get("session", {}).get("logMaskExpires", 0):
                updates["logMaskActive"] = False
            else:
                # Log masking active, don't increase suspicion
                return updates

        command_lower = command.lower()
        for keyword in self.monitored_keywords:
            if keyword in command_lower:
                suspicion = game_state.get("session", {}).get("archivist_suspicion", 0)
                updates["archivistSuspicion"] = min(100, suspicion + 5)
                break

        return updates
```

#### 3. API Endpoint
**File**: `backend/main.py` (additions)

```python
from filesystem.vfs import VirtualFileSystem
from filesystem.commands import CommandExecutor

# Initialize filesystem
vfs = VirtualFileSystem()
executor = CommandExecutor(vfs)

@app.post("/api/shell/command")
async def execute_command(request: Request):
    data = await request.json()
    command = data.get("command")
    player_id = data.get("playerId", "default")

    state = game_states.get(player_id)
    if not state:
        return {"error": "State not found"}, 404

    # Execute command
    output, state_updates = executor.execute(command, {
        "persistent": state.persistent.__dict__,
        "session": state.session.__dict__
    })

    # Apply state updates
    for key, value in state_updates.items():
        if hasattr(state.session, key):
            setattr(state.session, key, value)

    # Evaluate triggers
    state = trigger_engine.evaluate_all(state)

    return {
        "output": output,
        "cwd": vfs.current_path,
        "stateUpdates": state_updates
    }
```

---

## Frontend Implementation

### Enhanced Station Shell
**File**: `frontend/modules/station-shell.js` (enhancements)

```javascript
export class StationShell {
  constructor(stateManager) {
    this.stateManager = stateManager;
    this.history = [];
    this.historyIndex = -1;
    this.cwd = "~";
  }

  async executeCommand(command) {
    // Add to output
    this.addOutput(`$ ${command}`, 'command');

    // Send to backend
    const response = await fetch('/api/shell/command', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        command,
        playerId: this.stateManager.playerId
      })
    });

    const result = await response.json();

    // Handle special outputs
    if (result.output === '[CLEAR]') {
      this.clearTerminal();
      return;
    }

    // Display output
    this.addOutput(result.output, 'output');

    // Update CWD display
    this.cwd = result.cwd;
    this.updatePrompt();

    // Update game state
    if (result.stateUpdates) {
      await this.stateManager.update(result.stateUpdates);
    }

    // Add to history
    this.history.push(command);
    this.historyIndex = this.history.length;
  }

  addOutput(text, className) {
    const output = document.getElementById('terminal-output');
    const line = document.createElement('div');
    line.className = className;
    line.textContent = text;
    output.appendChild(line);
    output.scrollTop = output.scrollHeight;
  }

  updatePrompt() {
    document.getElementById('prompt').textContent = `[${this.cwd}]$`;
  }

  // Arrow key history navigation
  handleKeyDown(e) {
    if (e.key === 'ArrowUp') {
      if (this.historyIndex > 0) {
        this.historyIndex--;
        this.input.value = this.history[this.historyIndex];
      }
    } else if (e.key === 'ArrowDown') {
      if (this.historyIndex < this.history.length - 1) {
        this.historyIndex++;
        this.input.value = this.history[this.historyIndex];
      } else {
        this.historyIndex = this.history.length;
        this.input.value = '';
      }
    }
  }
}
```

---

## File Content Examples

See GAMEPLAY_TECH.md lines 897-1018 for full content of story-critical files.

---

## Integration Steps

1. Implement VFS backend
2. Implement command executor
3. Add API endpoint
4. Enhance station-shell.js
5. Connect to state manager
6. Test file unlocking via triggers
7. Test ARCHIVIST monitoring
8. Test log masking

---

## Testing Checklist

- [ ] ls shows correct files
- [ ] ls -a shows hidden files
- [ ] cd navigation works
- [ ] cat displays file contents
- [ ] Hidden files unlocked via triggers
- [ ] Monitored keywords increase suspicion
- [ ] Log masking prevents suspicion increase
- [ ] History navigation works
- [ ] Module shortcuts work

---

## Estimated Effort

- **Backend**: 2-3 days
- **Frontend**: 1-2 days
- **Content writing**: 1 day
- **Testing**: 1 day
- **Total**: ~1 week
