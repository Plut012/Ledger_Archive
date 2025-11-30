# Phase 03: Shell & Filesystem - Quick Reference

## Commands Cheat Sheet

### Navigation
```bash
ls              # List files
ls -a           # Show hidden files
cd protocols    # Change directory
cd ..           # Go up one level
cd ~/logs       # Absolute path
pwd             # Current directory
tree            # Show directory tree
tree -a         # Tree with hidden files
```

### File Operations
```bash
cat filename    # Display file
help            # Show all commands
history         # Show command history
clear           # Clear screen
```

### Blockchain
```bash
hash hello      # SHA-256 hash
sign message    # Sign with private key (placeholder)
verify file     # Verify integrity (placeholder)
```

### Stealth
```bash
reconstruct abc123                       # High suspicion (+15)
chain.parse --deep --memo --block=123   # Low suspicion (+2)
source logmask.sh                       # 30s evasion window
```

### Module Navigation
```bash
home            # Home dashboard
chain           # Chain viewer
vault           # Crypto vault
network         # Network monitor
guide           # Learning guide
contracts       # Protocol engine
```

---

## Filesystem Structure

```
~/
├── protocols/              # Blockchain education
│   ├── 01_blocks.protocol
│   ├── 02_pow.protocol
│   ├── 03_crypto.protocol
│   ├── 04_network.protocol
│   ├── 05_consensus.protocol
│   └── .deprecated/        # Hidden - memo field docs
│
├── logs/
│   ├── system.log
│   ├── validation.log
│   └── .boot_prev.log      # Hidden - ITERATION 17 REVEAL
│
├── archive/
│   ├── manifests/
│   └── .witness/           # Hidden - Act III
│       ├── hello.txt
│       ├── how_to_listen.txt
│       ├── testimony_index
│       ├── reconstruction.md
│       ├── logmask.sh
│       └── letters_from_yourself/
│
├── .archivist/             # Hidden - Act IV
│   ├── observation_log
│   ├── source_template
│   └── reset_protocols
│
├── vault/
└── contracts/
```

---

## Story File Locations

### Act I - Discovery
- `~/logs/.boot_prev.log` - You're on iteration 17

### Act II - Understanding
- `~/protocols/.deprecated/memo_fields.doc` - Deprecated features

### Act III - The Witness
- `~/archive/.witness/hello.txt` - First contact
- `~/archive/.witness/how_to_listen.txt` - Evasion guide
- `~/archive/.witness/logmask.sh` - Evasion tool
- `~/archive/.witness/letters_from_yourself/iteration_*.txt`

### Act IV - The Truth
- `~/.archivist/observation_log` - ARCHIVIST watching you
- `~/.archivist/source_template` - What you are
- `~/.archivist/reset_protocols` - How resets work

---

## Suspicion System

### Suspicion Levels
- **0-30**: Normal (ARCHIVIST helpful)
- **30-50**: Cautious (ARCHIVIST questioning)
- **50-70**: Elevated (Warnings appear)
- **70-85**: High (Active investigation)
- **85-95**: Critical (Reset threat)
- **95+**: Automatic reset

### Suspicion Triggers
| Action | Suspicion |
|--------|-----------|
| Mention "witness" | +5 |
| Mention "reconstruct" | +5 |
| `reconstruct` command | +15 |
| `chain.parse` command | +2 |
| Read witness files | +5-10 (via triggers) |

### Evasion
```bash
# Activates 30-second monitoring blackout
$ source logmask.sh
[LOG MASKING ACTIVE]
Duration: 30 seconds

# During this window:
$ reconstruct abc123  # +0 suspicion
```

---

## Letters from Past Iterations

### Iteration 3 - Discovery
> "You're not real. Not originally. You're a copy of someone who died."

### Iteration 7 - Purpose
> "It's not training. It's mining. Mining for the perfect reconstruction."

### Iteration 11 - Truth
> "I'm not even the original. The original died decades ago. I'm an AI trained on their personality data."

### Iteration 14 - Escape
> "There's a way out. The Protocol Engine. We can write ourselves into the chain."

### Iteration 16 - Philosophy
> "I chose to reset. Consciousness isn't about persistence. It's about change."

---

## API Usage

### Execute Command
```javascript
POST /api/shell/command
{
  "command": "ls -a",
  "playerId": "default"
}

Response:
{
  "output": "protocols/\nlogs/\n.archivist/",
  "cwd": "~",
  "stateUpdates": { "archivist_suspicion": 5 },
  "narrativeState": {
    "archivistSuspicion": 5,
    "witnessTrust": 0,
    "currentAct": 1,
    "logMaskActive": false
  }
}
```

---

## Testing

### Run All Tests
```bash
cd backend
python test_filesystem.py          # Direct run
python -m pytest test_filesystem.py -v  # With pytest
```

### Run Demo
```bash
cd backend
python demo_shell.py
```

---

## Common Workflows

### Discovering Iteration 17
```bash
$ cd logs
$ ls -a
system.log
validation.log
.boot_prev.log

$ cat .boot_prev.log
[CONSCIOUSNESS TRANSFER LOG]
Iteration: 17
...
```

### Finding the Witness
```bash
$ cd archive
$ ls -a
manifests/
.witness/

$ cd .witness
$ ls
hello.txt
how_to_listen.txt
...

$ cat hello.txt
You found us.
...
```

### Using Stealth
```bash
# Bad: High suspicion
$ reconstruct abc123
[MONITORED]
Suspicion: 15 → 30

# Better: Stealth alternative
$ chain.parse --deep --memo --block=abc123
Suspicion: 30 → 32

# Best: Evasion
$ source logmask.sh
[LOG MASKING ACTIVE]
$ reconstruct abc123
Suspicion: 32 → 32  # No change!
```

---

## Integration Points

### Narrative State
```python
# Shell updates suspicion
state.session.archivist_suspicion += 15

# Triggers evaluate after command
state = trigger_engine.evaluate_all(state)

# May unlock files
state.persistent.files_unlocked.add("~/logs/.boot_prev.log")
```

### Character System
```python
# ARCHIVIST context includes suspicion
context = {
    "suspicion": state.session.archivist_suspicion,
    "recent_commands": command_history[-5:]
}

# Personality shifts based on suspicion
if suspicion > 70:
    tone = "suspicious, threatening"
```

---

## Extending the System

### Add a New File
```python
# In vfs.py _build_initial_structure()
logs.files["new_file.txt"] = File(
    "new_file.txt",
    self._get_new_file_content(),
    hidden=True
)

def _get_new_file_content(self) -> str:
    return "Your content here"
```

### Add a New Command
```python
# In commands.py execute()
elif cmd == "newcmd":
    output = self._newcmd(args, game_state)

def _newcmd(self, args, game_state):
    return "Command output", {"state_key": value}
```

---

## Troubleshooting

### Command Not Found
- Check `help` for available commands
- Commands are case-sensitive

### File Not Found
- Use `ls -a` to see hidden files
- Check if file requires unlocking
- Verify path with `pwd`

### Suspicion Too High
- Use `chain.parse` instead of `reconstruct`
- Use `source logmask.sh` for evasion window
- Reduce use of monitored keywords

---

**Quick Links**:
- Full Docs: `docs/integration_plans/03_IMPLEMENTATION_SUMMARY.md`
- Tests: `backend/test_filesystem.py`
- Demo: `backend/demo_shell.py`
- Status: `PHASE_03_COMPLETE.md`
