"""
Code Synchronization Module

Monitors code commits across repositories and updates relevant context documents.
Uses GitHub API (PyGithub) with GITHUB_TOKEN when set.
"""

import logging
import os
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


def _get_github():
    """Return PyGithub instance if GITHUB_TOKEN set, else None."""
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        logger.debug("GITHUB_TOKEN not set")
        return None
    try:
        from github import Github
        return Github(token)
    except ImportError:
        logger.warning("PyGithub not installed; run pip install PyGithub")
        return None


class CodeSync:
    """Synchronizes code changes from monitored repositories."""

    def __init__(self, config, project_root=None):
        """Initialize with configuration and optional project root."""
        self.config = config
        self.project_root = Path(project_root) if project_root else None
        self.repos = config.get("repositories", {})
        self.context_files = config.get("sync", {}).get("context_files", {})
        self._agent_dir = Path(__file__).parent.parent

    def _resolve_path(self, relative_path: str) -> Path:
        if self.project_root:
            return self.project_root / relative_path
        return Path(relative_path)

    def sync(self):
        """
        Sync code commits from monitored repositories.

        Returns:
            list: List of change entries for changelog
        """
        changes = []
        if "bed" in self.repos:
            changes.extend(self._sync_repository("bed"))
        if "fed" in self.repos:
            changes.extend(self._sync_repository("fed"))
        return changes

    def _sync_repository(self, repo_key):
        """Fetch recent commits via GitHub API; update state and summary; return change entries."""
        repo_config = self.repos.get(repo_key, {})
        owner = repo_config.get("owner")
        repo_name = repo_config.get("repo")
        branch = repo_config.get("branch", "main")
        if not owner or not repo_name:
            return []

        gh = _get_github()
        if not gh:
            return []

        try:
            import state_manager
            state = state_manager.load_state("code_last_commit", self._agent_dir)
            last_sha = state.get(repo_key)
        except ImportError:
            state = {}
            last_sha = None

        try:
            repo = gh.get_repo(f"{owner}/{repo_name}")
            commits = list(repo.get_commits(sha=branch)[:30])
        except Exception as e:
            logger.error("GitHub get_commits failed for %s: %s", repo_key, e)
            return []

        if not commits:
            return []

        new_commits = []
        for c in commits:
            if last_sha and c.sha == last_sha:
                break
            new_commits.append({"sha": c.sha[:7], "message": (c.commit.message or "").split("\n")[0][:200], "date": c.commit.author.date.isoformat() if c.commit.author else ""})
        if not new_commits:
            logger.info("No new commits for %s", repo_key)
            return []

        try:
            import state_manager
            state[repo_key] = commits[0].sha
            state_manager.save_state("code_last_commit", state, self._agent_dir)
        except ImportError:
            pass

        rel = self.context_files.get("bed_summary" if repo_key == "bed" else "fed_summary", "")
        if rel:
            summary_path = self._resolve_path(rel)
            summary_path.parent.mkdir(parents=True, exist_ok=True)
            header = f"# {repo_name} - Last commits\n\n"
            section = "\n".join(f"- `{c['sha']}` {c['message']}" for c in new_commits[:15])
            try:
                existing = summary_path.read_text() if summary_path.exists() else ""
                if "# Last commits" not in existing:
                    content = (existing.strip() + "\n\n" + header + section + "\n").strip()
                else:
                    content = header + section + "\n"
                summary_path.write_text(content)
            except IOError as e:
                logger.warning("Could not write summary %s: %s", summary_path, e)

        ts = datetime.now().strftime("%Y-%m-%d %H:%M")
        return [{"type": "Code Commit", "repository": f"{owner}/{repo_name}", "timestamp": ts, "commit": new_commits[0]["sha"], "change": f"{len(new_commits)} new commits", "context_updated": rel or repo_key}]
