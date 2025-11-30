"""Interactive demo of the shell filesystem."""

from filesystem.vfs import VirtualFileSystem
from filesystem.commands import CommandExecutor


def print_separator():
    print("\n" + "=" * 60 + "\n")


def demo():
    """Run an interactive demo of the shell system."""
    print("🚀 Chain of Truth - Phase 03 Shell & Filesystem Demo")
    print_separator()

    # Initialize
    vfs = VirtualFileSystem()
    executor = CommandExecutor(vfs)

    # Mock game state
    game_state = {
        "persistent": {
            "files_unlocked": {
                "~/logs/.boot_prev.log",
                "~/archive/.witness/hello.txt"
            },
            "current_act": 1,
            "current_iteration": 17
        },
        "session": {
            "archivist_suspicion": 0,
            "witness_trust": 0,
            "log_mask_active": False,
            "log_mask_expires": 0
        }
    }

    commands = [
        ("pwd", "Check current directory"),
        ("ls", "List directory contents"),
        ("ls -a", "Show hidden files"),
        ("cd protocols", "Navigate to protocols"),
        ("ls", "List protocol files"),
        ("cat 01_blocks.protocol", "Read blockchain protocol"),
        ("cd ../logs", "Navigate to logs"),
        ("ls -a", "Show hidden logs"),
        ("cat .boot_prev.log", "Read hidden boot log (reveals iteration 17)"),
        ("hash hello world", "Calculate SHA-256 hash"),
        ("help", "Show available commands"),
        ("tree", "Display directory tree"),
    ]

    for cmd, description in commands:
        print(f"📍 {description}")
        print(f"$ {cmd}")
        print()

        output, updates = executor.execute(cmd, game_state)

        # Apply updates
        for key, value in updates.items():
            if key in game_state["session"]:
                game_state["session"][key] = value

        # Print output (truncated if too long)
        lines = output.split('\n')
        if len(lines) > 15:
            print('\n'.join(lines[:15]))
            print(f"... ({len(lines) - 15} more lines)")
        else:
            print(output)

        if updates:
            print(f"\n🔄 State Updates: {updates}")

        print_separator()

    # Show monitoring demo
    print("🕵️ ARCHIVIST Monitoring Demo")
    print_separator()

    print("$ reconstruct abc123")
    output, updates = executor.execute("reconstruct abc123", game_state)
    print(output)
    print(f"\n⚠️  Suspicion increased: {game_state['session']['archivist_suspicion']} → {updates['archivist_suspicion']}")
    game_state["session"]["archivist_suspicion"] = updates["archivist_suspicion"]

    print_separator()

    print("$ source logmask.sh")
    output, updates = executor.execute("source logmask.sh", game_state)
    print(output)
    print(f"\n🎭 Log masking active for 30 seconds")

    print_separator()

    # Show stealth alternative
    print("$ chain.parse --deep --memo --block=52441")
    game_state["session"]["log_mask_active"] = False  # Reset for demo
    output, updates = executor.execute("chain.parse --deep --memo --block=52441", game_state)
    print(output)
    if "archivist_suspicion" in updates:
        print(f"\n📊 Suspicion increase: +{updates['archivist_suspicion'] - game_state['session']['archivist_suspicion']} (much lower than 'reconstruct')")

    print_separator()

    # Show hidden directory navigation
    print("🔍 Hidden Directory Discovery Demo")
    print_separator()

    cmds = [
        "cd ~/archive",
        "ls -a",
        "cd .witness",
        "cat hello.txt"
    ]

    for cmd in cmds:
        print(f"$ {cmd}")
        output, updates = executor.execute(cmd, game_state)
        print(output)
        print()

    print_separator()
    print("✅ Demo Complete!")
    print("\nKey Features Demonstrated:")
    print("  ✓ File navigation (ls, cd, pwd)")
    print("  ✓ Hidden file discovery (ls -a)")
    print("  ✓ File reading (cat)")
    print("  ✓ Story content (boot logs, witness messages)")
    print("  ✓ Blockchain commands (hash)")
    print("  ✓ ARCHIVIST monitoring")
    print("  ✓ Log masking (stealth mechanics)")
    print("  ✓ Stealth alternatives (chain.parse)")
    print("  ✓ Directory tree visualization")
    print("\nPhase 03: Shell & Filesystem - COMPLETE ✨")


if __name__ == "__main__":
    demo()
