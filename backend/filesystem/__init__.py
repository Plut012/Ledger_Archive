"""Virtual filesystem module for terminal shell simulation."""

from .vfs import VirtualFileSystem, File, Directory
from .commands import CommandExecutor

__all__ = ['VirtualFileSystem', 'File', 'Directory', 'CommandExecutor']
