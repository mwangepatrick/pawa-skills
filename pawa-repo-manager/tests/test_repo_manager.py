import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import repo_manager


def git(path: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(path), *args], text=True,
                            capture_output=True, check=True)
    return result.stdout.strip()


class RepoManagerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.remote = self.root / "remote.git"
        subprocess.run(["git", "init", "--bare", str(self.remote)], check=True,
                       capture_output=True)
        self.repo = self.root / "repo"
        subprocess.run(["git", "init", "-b", "main", str(self.repo)], check=True,
                       capture_output=True)
        git(self.repo, "config", "user.email", "test@example.invalid")
        git(self.repo, "config", "user.name", "Test")
        (self.repo / "README.md").write_text("initial\n", encoding="utf-8")
        git(self.repo, "add", "README.md")
        git(self.repo, "commit", "-m", "initial")
        git(self.repo, "remote", "add", "origin", str(self.remote))
        git(self.repo, "push", "-u", "origin", "main")
        self.manifest = self.root / "repo.json"
        self.manifest.write_text(json.dumps({
            "schemaVersion": 1,
            "workspace": ".",
            "ignorePaths": ["archives"],
            "repositories": [{"name": "repo", "path": "repo", "kind": "repository",
                               "scope": "active", "remote": str(self.remote),
                               "defaultBranch": "main", "syncPolicy": "fast-forward-only"}]
        }), encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def test_clean_synced_status(self):
        root, data = repo_manager.load_manifest(self.manifest)
        status = repo_manager.statuses(root, data)[0]
        self.assertEqual(status.state, "clean/synced")
        self.assertEqual((status.ahead, status.behind), (0, 0))

    def test_dirty_status(self):
        (self.repo / "README.md").write_text("changed\n", encoding="utf-8")
        root, data = repo_manager.load_manifest(self.manifest)
        self.assertEqual(repo_manager.statuses(root, data)[0].state, "dirty")

    def test_ahead_status(self):
        (self.repo / "new.txt").write_text("local\n", encoding="utf-8")
        git(self.repo, "add", "new.txt")
        git(self.repo, "commit", "-m", "local")
        root, data = repo_manager.load_manifest(self.manifest)
        status = repo_manager.statuses(root, data)[0]
        self.assertEqual(status.state, "ahead")
        self.assertEqual(status.ahead, 1)

    def test_manifest_rejects_path_escape(self):
        self.manifest.write_text(json.dumps({"schemaVersion": 1, "repositories": [
            {"name": "bad", "path": "../outside", "kind": "repository", "scope": "active"}
        ]}), encoding="utf-8")
        with self.assertRaises(ValueError):
            repo_manager.load_manifest(self.manifest)

    def test_ignored_entry_is_not_operated(self):
        data = json.loads(self.manifest.read_text(encoding="utf-8"))
        data["repositories"][0]["scope"] = "ignored"
        self.manifest.write_text(json.dumps(data), encoding="utf-8")
        status = repo_manager.statuses(*repo_manager.load_manifest(self.manifest))[0]
        self.assertEqual(status.state, "ignored")

    def test_lock_is_atomic(self):
        lock = repo_manager.acquire(self.root, "test")
        try:
            with self.assertRaises(RuntimeError):
                repo_manager.acquire(self.root, "second")
        finally:
            repo_manager.release(lock)

    def test_redacts_credentials(self):
        self.assertEqual(repo_manager.redact("https://user:secret@example.com/x.git"),
                         "https://<redacted>@example.com/x.git")


if __name__ == "__main__":
    unittest.main()
