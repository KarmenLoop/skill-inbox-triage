import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from run import process
from runtime import load_json

class SkillTests(unittest.TestCase):
    def sample(self):
        return json.loads((ROOT / "examples/input.json").read_text())

    def test_example_cli(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/run.py"), "--input", str(ROOT / "examples/input.json")], cwd=ROOT, capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), process(self.sample()))

    def test_invalid_input_does_not_write_output(self):
        with tempfile.TemporaryDirectory() as folder:
            source, output = Path(folder) / "bad.json", Path(folder) / "result.json"
            source.write_text("[]")
            result = subprocess.run([sys.executable, str(ROOT / "scripts/run.py"), "--input", str(source), "--output", str(output)], capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 2)
            self.assertFalse(output.exists())

    def test_existing_output_is_preserved(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "result.json"
            output.write_text("keep")
            result = subprocess.run([sys.executable, str(ROOT / "scripts/run.py"), "--input", str(ROOT / "examples/input.json"), "--output", str(output)], cwd=ROOT, capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(output.read_text(), "keep")

    def test_install_to_temporary_directory(self):
        with tempfile.TemporaryDirectory() as folder:
            dest = Path(folder) / "skill"
            command = [sys.executable, str(ROOT / "install.py"), "--destination", str(dest)]
            result = subprocess.run(command, capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((dest / "SKILL.md").is_file())
            self.assertTrue((dest / "scripts/run.py").is_file())
            self.assertFalse((dest / ".git").exists())
            example = subprocess.run([sys.executable, str(dest / "scripts/run.py"), "--input", str(dest / "examples/input.json")], cwd=dest, capture_output=True, text=True, timeout=10)
            self.assertEqual(example.returncode, 0, example.stderr)
            second = subprocess.run(command, capture_output=True, text=True, timeout=10)
            self.assertEqual(second.returncode, 2)

    def test_duplicate_json_keys_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "bad.json"
            source.write_text('{"value":1,"value":2}')
            with self.assertRaises(ValueError):
                load_json(source)


    def test_overdue_before_vip(self):
        self.assertEqual([r["id"] for r in process(self.sample())["queues"]["reply_now"]], ["m2","m1"])

    def test_future_message_rejected(self):
        data = self.sample()
        data["messages"][0]["received_at"] = "2030-01-01T00:00:00Z"
        with self.assertRaises(ValueError):
            process(data)

if __name__ == "__main__":
    unittest.main()
