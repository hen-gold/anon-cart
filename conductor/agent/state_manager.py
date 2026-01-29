"""
State Manager

Read/write JSON state files for sync modules (Jira, Slack, Google, code).
State is stored under .state/ relative to the agent directory.
"""

import json
import logging
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)


def _state_dir(agent_dir: Optional[Path] = None) -> Path:
    """Return the .state directory path; create if needed."""
    if agent_dir is None:
        agent_dir = Path(__file__).parent
    state_dir = agent_dir / ".state"
    state_dir.mkdir(parents=True, exist_ok=True)
    return state_dir


def load_state(name: str, agent_dir: Optional[Path] = None) -> dict:
    """
    Load state from .state/<name>.json.

    Args:
        name: State file name without extension (e.g. jira_last_state)
        agent_dir: Optional agent directory; default is this file's parent.

    Returns:
        dict: Loaded state, or {} if file missing or invalid
    """
    state_dir = _state_dir(agent_dir)
    path = state_dir / f"{name}.json"
    if not path.exists():
        return {}
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        logger.warning(f"Could not load state {name}: {e}")
        return {}


def save_state(name: str, data: dict, agent_dir: Optional[Path] = None) -> None:
    """
    Save state to .state/<name>.json.

    Args:
        name: State file name without extension
        data: Dict to save (must be JSON-serializable)
        agent_dir: Optional agent directory
    """
    state_dir = _state_dir(agent_dir)
    path = state_dir / f"{name}.json"
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
    except (TypeError, IOError) as e:
        logger.error(f"Could not save state {name}: {e}")
