"""Command executor for virtual filesystem shell."""

from typing import Dict, List, Tuple, Any, Optional
import hashlib
import time
from .vfs import VirtualFileSystem
from stealth.monitor import StealthMonitor


class CommandExecutor:
    """Executes shell commands and manages monitoring."""

    def __init__(self, vfs: VirtualFileSystem, stealth_monitor: Optional[StealthMonitor] = None):
        self.vfs = vfs
        self.history: List[str] = []
        self.stealth_monitor = stealth_monitor or StealthMonitor()
        # Keep for backwards compatibility, but now used by StealthMonitor
        self.monitored_keywords = ["reconstruct", "witness", "testimony", "upload"]

    def execute(self, command: str, game_state: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """
        Execute command and return output + state updates.

        Args:
            command: The command string to execute
            game_state: Current game state with 'persistent' and 'session' dicts

        Returns:
            Tuple of (output_string, state_updates_dict)
        """
        self.history.append(command)

        parts = command.strip().split()
        if not parts:
            return "", {}

        cmd = parts[0]
        args = parts[1:]

        # Check for monitored keywords (before command execution)
        state_updates = self._check_monitoring(command, game_state)

        # Route to command handler
        if cmd == "ls":
            output = self._ls(args, game_state)
        elif cmd == "cd":
            output = self._cd(args)
        elif cmd == "cat":
            output = self._cat(args, game_state)
        elif cmd == "pwd":
            output = self.vfs.pwd()
        elif cmd == "tree":
            output = self._tree(args)
        elif cmd == "clear":
            output = "[CLEAR]"
        elif cmd == "help":
            output = self._help()
        elif cmd == "history":
            output = self._history()
        elif cmd == "hash":
            output = self._hash(args)
        elif cmd == "sign":
            output = self._sign(args, game_state)
        elif cmd == "verify":
            output = self._verify(args)
        elif cmd == "reconstruct":
            output, updates = self._reconstruct(args, game_state)
            state_updates.update(updates)
        elif cmd == "source":
            output, updates = self._source(args, game_state)
            state_updates.update(updates)
        elif cmd == "chain.parse":
            output, updates = self._chain_parse(args, game_state)
            state_updates.update(updates)
        # Module navigation shortcuts
        elif cmd in ["home", "chain", "vault", "network", "guide", "contracts"]:
            output = f"[NAVIGATE:{cmd}]"
        else:
            output = f"{cmd}: command not found"

        return output, state_updates

    def _ls(self, args: List[str], game_state: Dict[str, Any]) -> str:
        """List directory contents."""
        show_hidden = "-a" in args or "--all" in args
        items = self.vfs.ls(show_hidden)
        return "\n".join(items)

    def _cd(self, args: List[str]) -> str:
        """Change directory."""
        if not args:
            return self.vfs.cd("~")
        return self.vfs.cd(args[0])

    def _cat(self, args: List[str], game_state: Dict[str, Any]) -> str:
        """Display file contents."""
        if not args:
            return "cat: missing file operand"

        unlocked = game_state.get("persistent", {}).get("files_unlocked", set())
        return self.vfs.cat(args[0], unlocked)

    def _tree(self, args: List[str]) -> str:
        """Display directory tree."""
        show_hidden = "-a" in args or "--all" in args
        return self.vfs.tree(show_hidden)

    def _help(self) -> str:
        """Display available commands."""
        return """STATION SHELL COMMANDS

File System:
  ls [-a]          List directory contents
  cd [dir]         Change directory
  cat [file]       Display file contents
  pwd              Print working directory
  tree [-a]        Display directory tree
  clear            Clear terminal
  history          Show command history

Blockchain:
  hash [text]      Calculate SHA-256 hash
  sign [msg]       Sign message with private key
  verify [file]    Verify file integrity
  reconstruct [h]  Parse consciousness data [MONITORED]

Stealth:
  chain.parse      Alias for reconstruct (evades monitoring)
  source [script]  Execute shell script (e.g., logmask.sh)

Navigation:
  home             Go to home dashboard
  chain            Go to chain viewer
  vault            Go to crypto vault
  network          Go to network monitor
  guide            Go to learning guide
  contracts        Go to protocol engine

Use 'ls -a' to show hidden files and directories."""

    def _history(self) -> str:
        """Show command history."""
        if not self.history:
            return "No command history"

        lines = []
        for i, cmd in enumerate(self.history[-20:], 1):  # Last 20 commands
            lines.append(f"  {i}  {cmd}")
        return "\n".join(lines)

    def _hash(self, args: List[str]) -> str:
        """Calculate SHA-256 hash."""
        if not args:
            return "hash: missing argument\nUsage: hash [text]"

        text = " ".join(args)
        hash_obj = hashlib.sha256(text.encode())
        return f"SHA-256: {hash_obj.hexdigest()}"

    def _sign(self, args: List[str], game_state: Dict[str, Any]) -> str:
        """Sign a message (placeholder for crypto integration)."""
        if not args:
            return "sign: missing message\nUsage: sign [message]"

        # TODO: Integrate with crypto vault for actual signing
        message = " ".join(args)
        return f"[SIGNATURE PLACEHOLDER]\nMessage: {message}\nStatus: Crypto vault integration pending"

    def _verify(self, args: List[str]) -> str:
        """Verify file integrity (placeholder)."""
        if not args:
            return "verify: missing file\nUsage: verify [file]"

        # TODO: Implement file integrity verification
        return f"verify: {args[0]}: Verification not yet implemented"

    def _reconstruct(self, args: List[str], game_state: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """
        Consciousness reconstruction command (MONITORED).
        Increases ARCHIVIST suspicion significantly.
        """
        # Increase suspicion
        current_suspicion = game_state.get("session", {}).get("archivist_suspicion", 0)
        updates = {
            "archivist_suspicion": min(100, current_suspicion + 15)
        }

        if not args:
            return "reconstruct: missing block hash\nUsage: reconstruct [hash]", updates

        # TODO: Integrate with blockchain to actually parse consciousness data
        block_ref = args[0]
        output = f"""[PARSING CONSCIOUSNESS DATA: {block_ref}]
[WARNING: This command is monitored by ARCHIVIST]
[ACCESS LOGGED]

Extracting memo fields from transactions...
Decoding consciousness fragments...

[Integration pending with chain viewer module]"""

        return output, updates

    def _chain_parse(self, args: List[str], game_state: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """
        Chain parsing command - functionally identical to reconstruct
        but uses standard blockchain syntax, so evades monitoring.
        """
        # Check for --deep --memo flags
        if "--deep" not in args or "--memo" not in args:
            return "chain.parse: requires --deep --memo flags\nUsage: chain.parse --deep --memo --block=[n]", {}

        # Extract block number
        block_num = None
        for arg in args:
            if arg.startswith("--block="):
                block_num = arg.split("=")[1]
                break

        if not block_num:
            return "chain.parse: missing --block parameter", {}

        # This does the same as reconstruct but doesn't trigger monitoring
        # Only slight suspicion increase from using advanced commands
        current_suspicion = game_state.get("session", {}).get("archivist_suspicion", 0)
        updates = {
            "archivist_suspicion": min(100, current_suspicion + 2)  # Much lower than reconstruct
        }

        output = f"""[DEEP CHAIN ANALYSIS: Block {block_num}]

Parsing transaction memo fields...
Extracting embedded data...

[Integration pending with chain viewer module]

Memo field content detected.
Use 'cat' on extracted files to read decoded data."""

        return output, updates

    def _source(self, args: List[str], game_state: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """Execute shell script (primarily logmask.sh)."""
        if not args:
            return "source: missing file\nUsage: source [script]", {}

        script_name = args[0]

        # Check if it's logmask.sh
        if "logmask.sh" in script_name:
            return self._execute_logmask()

        return f"source: {script_name}: No such file or directory", {}

    def _execute_logmask(self) -> Tuple[str, Dict[str, Any]]:
        """Execute logmask.sh script - enables 30 seconds of unmonitored activity."""
        output = """Initializing log rotation...
Archiving current session...
Clearing volatile buffers...

[LOG MASKING ACTIVE]
Duration: 30 seconds
All commands will not be monitored during this window.

Use this time wisely."""

        updates = {
            "log_mask_active": True,
            "log_mask_expires": int(time.time()) + 30
        }

        return output, updates

    def _check_monitoring(self, command: str, game_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if command contains monitored keywords using StealthMonitor.
        Returns state updates for suspicion tracking.
        """
        updates = {}

        # Use the advanced stealth monitoring system
        result = self.stealth_monitor.check_command(command, game_state)

        # Update suspicion if detected
        if result.detected and result.suspicion_increase > 0:
            session = game_state.get("session", {})
            current_suspicion = session.get("archivist_suspicion", 0)
            new_suspicion = min(100, current_suspicion + result.suspicion_increase)
            updates["archivist_suspicion"] = new_suspicion

        # Check if log mask has expired
        session = game_state.get("session", {})
        if session.get("log_mask_active"):
            if int(time.time()) > session.get("log_mask_expires", 0):
                updates["log_mask_active"] = False

        return updates
