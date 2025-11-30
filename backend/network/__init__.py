"""Network collapse and station death mechanics."""

# Import Network class from the old network.py for backwards compatibility
import sys
from pathlib import Path

# Add parent directory to path to import the old network module
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

try:
    from network_old import Network
except ImportError:
    # If network_old.py doesn't exist, try to import from network.py in parent
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("network_module", parent_dir / "network.py")
        network_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(network_module)
        Network = network_module.Network
    except:
        # If all else fails, create a dummy Network class
        class Network:
            def __init__(self):
                pass
            def create_default_topology(self):
                pass
            def sync_chain(self, chain):
                pass

__all__ = ['Network']
