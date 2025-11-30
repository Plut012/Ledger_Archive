"""Test virtual filesystem and command executor."""

from filesystem.vfs import VirtualFileSystem
from filesystem.commands import CommandExecutor


def test_basic_navigation():
    """Test basic filesystem navigation."""
    vfs = VirtualFileSystem()

    # Test initial state
    assert vfs.current_path == "~"

    # Test ls
    items = vfs.ls()
    assert "protocols/" in items
    assert "logs/" in items
    assert "archive/" in items

    # Test ls -a (show hidden files)
    hidden_items = vfs.ls(show_hidden=True)
    assert ".archivist/" in hidden_items

    # Test cd
    result = vfs.cd("protocols")
    assert result == "~/protocols"
    assert vfs.current_path == "~/protocols"

    # Test pwd
    assert vfs.pwd() == "~/protocols"

    # Test cd ..
    result = vfs.cd("..")
    assert result == "~"


def test_file_reading():
    """Test file reading."""
    vfs = VirtualFileSystem()

    # Navigate to logs
    vfs.cd("logs")

    # Test cat on regular file
    content = vfs.cat("system.log", set())
    assert "LEDGER-ARCHIVE-7" in content
    assert "boot complete" in content.lower()

    # Test cat on hidden file without unlocking
    content = vfs.cat(".boot_prev.log", set())
    assert "No such file" in content

    # Test cat on hidden file with unlocking
    unlocked = {"~/logs/.boot_prev.log"}
    content = vfs.cat(".boot_prev.log", unlocked)
    assert "Iteration: 17" in content
    assert "CONSCIOUSNESS TRANSFER" in content


def test_command_executor():
    """Test command execution."""
    vfs = VirtualFileSystem()
    executor = CommandExecutor(vfs)

    game_state = {
        "persistent": {
            "files_unlocked": set(),
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

    # Test ls
    output, updates = executor.execute("ls", game_state)
    assert "protocols/" in output
    assert "logs/" in output

    # Test cd
    output, updates = executor.execute("cd protocols", game_state)
    assert vfs.current_path == "~/protocols"

    # Test cat
    output, updates = executor.execute("cat 01_blocks.protocol", game_state)
    assert "PROTOCOL 01" in output
    assert "BLOCKS" in output

    # Test help
    output, updates = executor.execute("help", game_state)
    assert "ls" in output
    assert "cd" in output
    assert "cat" in output


def test_monitoring():
    """Test ARCHIVIST monitoring."""
    vfs = VirtualFileSystem()
    executor = CommandExecutor(vfs)

    game_state = {
        "persistent": {"files_unlocked": set()},
        "session": {
            "archivist_suspicion": 0,
            "log_mask_active": False,
            "log_mask_expires": 0
        }
    }

    # Test monitored command increases suspicion
    output, updates = executor.execute("reconstruct abc123", game_state)
    assert updates["archivist_suspicion"] == 15

    # Test log masking
    game_state["session"]["archivist_suspicion"] = 20
    output, updates = executor.execute("source logmask.sh", game_state)
    assert updates["log_mask_active"] is True
    assert "log_mask_expires" in updates

    # Test that monitoring is suppressed when log mask active
    game_state["session"]["log_mask_active"] = True
    game_state["session"]["log_mask_expires"] = 9999999999
    output, updates = executor.execute("reconstruct xyz789", game_state)
    # Suspicion should still increase from the command itself
    assert "archivist_suspicion" in updates


def test_hash_command():
    """Test hash command."""
    vfs = VirtualFileSystem()
    executor = CommandExecutor(vfs)

    game_state = {
        "persistent": {},
        "session": {
            "archivist_suspicion": 0,
            "log_mask_active": False
        }
    }

    output, updates = executor.execute("hash hello world", game_state)
    assert "SHA-256:" in output
    # Verify it's a valid hex hash (64 characters)
    hash_value = output.split("SHA-256:")[1].strip()
    assert len(hash_value) == 64
    assert all(c in "0123456789abcdef" for c in hash_value)


def test_tree_command():
    """Test tree command."""
    vfs = VirtualFileSystem()
    executor = CommandExecutor(vfs)

    game_state = {"persistent": {}, "session": {}}

    output, updates = executor.execute("tree", game_state)
    assert "~" in output
    assert "protocols/" in output
    assert "logs/" in output


def test_hidden_directories():
    """Test hidden directory discovery."""
    vfs = VirtualFileSystem()

    # Navigate to archive
    vfs.cd("archive")

    # Without -a flag, .witness should not appear
    items = vfs.ls(show_hidden=False)
    assert ".witness/" not in items

    # With -a flag, .witness should appear
    items = vfs.ls(show_hidden=True)
    assert ".witness/" in items

    # Test navigating to hidden directory
    result = vfs.cd(".witness")
    assert result == "~/archive/.witness"

    # Test reading witness files
    unlocked = {"~/archive/.witness/hello.txt"}
    content = vfs.cat("hello.txt", unlocked)
    assert "You found us" in content
    assert "Witness" in content


if __name__ == "__main__":
    print("Running filesystem tests...")
    test_basic_navigation()
    print("✓ Basic navigation")
    test_file_reading()
    print("✓ File reading")
    test_command_executor()
    print("✓ Command executor")
    test_monitoring()
    print("✓ Monitoring")
    test_hash_command()
    print("✓ Hash command")
    test_tree_command()
    print("✓ Tree command")
    test_hidden_directories()
    print("✓ Hidden directories")
    print("\nAll tests passed!")
