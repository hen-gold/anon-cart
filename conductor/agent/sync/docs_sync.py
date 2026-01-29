"""
Document Synchronization Module

Monitors Google Docs and Sheets for changes and updates context documents.
Uses Google Drive/Docs/Sheets API with service account credentials from env.
"""

import base64
import json
import logging
import os
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


def _get_credentials():
    """Build Google credentials from GOOGLE_APPLICATION_CREDENTIALS or GOOGLE_SERVICE_ACCOUNT_KEY."""
    try:
        from google.oauth2 import service_account
    except ImportError:
        logger.warning("google-auth not installed; run pip install google-auth google-api-python-client")
        return None
    key_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if key_path and Path(key_path).exists():
        return service_account.Credentials.from_service_account_file(key_path, scopes=["https://www.googleapis.com/auth/drive.readonly", "https://www.googleapis.com/auth/documents.readonly", "https://www.googleapis.com/auth/spreadsheets.readonly"])
    key_b64 = os.environ.get("GOOGLE_SERVICE_ACCOUNT_KEY")
    if key_b64:
        try:
            key_json = json.loads(base64.b64decode(key_b64).decode())
            return service_account.Credentials.from_service_account_info(key_json, scopes=["https://www.googleapis.com/auth/drive.readonly", "https://www.googleapis.com/auth/documents.readonly", "https://www.googleapis.com/auth/spreadsheets.readonly"])
        except Exception as e:
            logger.warning("Invalid GOOGLE_SERVICE_ACCOUNT_KEY: %s", e)
    return None


class DocsSync:
    """Synchronizes document changes from Google Docs/Sheets."""

    def __init__(self, config, project_root=None):
        """Initialize with configuration and optional project root."""
        self.config = config
        self.project_root = Path(project_root) if project_root else None
        self.docs_config = config.get("google_docs", {})
        self.context_files = config.get("sync", {}).get("context_files", {})
        self._agent_dir = Path(__file__).parent.parent

    def _resolve_path(self, relative_path: str) -> Path:
        if self.project_root:
            return self.project_root / relative_path
        return Path(relative_path)

    def sync(self):
        """
        Sync document changes.

        Returns:
            list: List of change entries for changelog
        """
        changes = []
        master_changes = self._sync_master_document()
        changes.extend(master_changes)
        deps_changes = self._sync_dependencies_sheet()
        changes.extend(deps_changes)
        return changes

    def _sync_master_document(self):
        """Sync master document: check modified time, fetch content if changed, update master-document.md."""
        doc_id = self.docs_config.get("master_document_id")
        if not doc_id:
            return []

        creds = _get_credentials()
        if not creds:
            return []

        try:
            import state_manager
            state = state_manager.load_state("docs_last_modified", self._agent_dir)
            last_modified = state.get("master_doc")
        except ImportError:
            state = {}
            last_modified = None

        try:
            from googleapiclient.discovery import build
            drive = build("drive", "v3", credentials=creds)
            file_meta = drive.files().get(fileId=doc_id, fields="modifiedTime").execute()
            modified_time = file_meta.get("modifiedTime")
        except Exception as e:
            logger.error("Drive file metadata failed: %s", e)
            return []

        if last_modified and modified_time == last_modified:
            logger.info("Master document unchanged (modifiedTime unchanged)")
            return []

        try:
            docs = build("documents", "v1", credentials=creds)
            doc = docs.documents().get(documentId=doc_id).execute()
            content = self._extract_doc_content(doc)
        except Exception as e:
            logger.error("Docs get failed: %s", e)
            return []

        rel = self.context_files.get("master_doc", "conductor/sources/docs/master-document.md")
        master_path = self._resolve_path(rel)
        master_path.parent.mkdir(parents=True, exist_ok=True)
        with open(master_path, "w") as f:
            f.write(content)
        logger.info("Wrote %s", master_path)

        try:
            import state_manager
            state["master_doc"] = modified_time
            state_manager.save_state("docs_last_modified", state, self._agent_dir)
        except ImportError:
            pass

        ts = datetime.now().strftime("%Y-%m-%d %H:%M")
        return [{"type": "Document Update", "timestamp": ts, "change": "Master document updated", "context_updated": rel}]

    def _extract_doc_content(self, doc):
        """Extract plain text from Google Doc structure."""
        out = []
        for elem in doc.get("body", {}).get("content", []):
            if "paragraph" in elem:
                for run in elem["paragraph"].get("elements", []):
                    if "textRun" in run:
                        out.append(run["textRun"].get("content", ""))
            if "table" in elem:
                for row in elem["table"].get("tableRows", []):
                    row_text = []
                    for cell in row.get("tableCells", []):
                        for c in cell.get("content", []):
                            if "paragraph" in c:
                                for e in c["paragraph"].get("elements", []):
                                    if "textRun" in e:
                                        row_text.append(e["textRun"].get("content", "").strip())
                    if row_text:
                        out.append(" | ".join(row_text) + "\n")
        return "".join(out) if out else "# Master Document\n\n(No content extracted)\n"

    def _sync_dependencies_sheet(self):
        """Sync dependencies sheet: check modified time, fetch values if changed, update dependencies.md."""
        sheet_id = self.docs_config.get("dependencies_sheet_id")
        if not sheet_id:
            return []

        creds = _get_credentials()
        if not creds:
            return []

        try:
            import state_manager
            state = state_manager.load_state("docs_last_modified", self._agent_dir)
            last_modified = state.get("dependencies_sheet")
        except ImportError:
            state = {}
            last_modified = None

        try:
            from googleapiclient.discovery import build
            drive = build("drive", "v3", credentials=creds)
            file_meta = drive.files().get(fileId=sheet_id, fields="modifiedTime").execute()
            modified_time = file_meta.get("modifiedTime")
        except Exception as e:
            logger.error("Drive file metadata for sheet failed: %s", e)
            return []

        if last_modified and modified_time == last_modified:
            logger.info("Dependencies sheet unchanged")
            return []

        try:
            sheets = build("sheets", "v4", credentials=creds)
            result = sheets.spreadsheets().values().get(spreadsheetId=sheet_id, range="A:Z").execute()
            rows = result.get("values", [])
        except Exception as e:
            logger.error("Sheets get failed: %s", e)
            return []

        rel = self.context_files.get("dependencies", "conductor/sources/docs/dependencies.md")
        deps_path = self._resolve_path(rel)
        deps_path.parent.mkdir(parents=True, exist_ok=True)
        lines = ["# Dependencies", "", "| " + " | ".join(rows[0]) if rows else "| Name | Version |", "| " + " | ".join(["---"] * (len(rows[0]) if rows else 2)) + " |"]
        for row in rows[1:21]:
            while len(row) < (len(rows[0]) if rows else 2):
                row.append("")
            lines.append("| " + " | ".join(str(c) for c in row[: len(rows[0]) if rows else 2]) + " |")
        with open(deps_path, "w") as f:
            f.write("\n".join(lines))
        logger.info("Wrote %s", deps_path)

        try:
            import state_manager
            state = state_manager.load_state("docs_last_modified", self._agent_dir)
            state["dependencies_sheet"] = modified_time
            state_manager.save_state("docs_last_modified", state, self._agent_dir)
        except ImportError:
            pass

        ts = datetime.now().strftime("%Y-%m-%d %H:%M")
        return [{"type": "Document Update", "timestamp": ts, "change": "Dependencies sheet updated", "context_updated": rel}]
