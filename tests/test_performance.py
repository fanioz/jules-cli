import time
import sys
import subprocess

def test_cli_import_time_threshold():
    """Ensure CLI startup time remains fast."""
    # Run the import in a separate process to avoid caching from other tests
    code = 'import time; start = time.time(); import jules_cli.cli; print(time.time() - start)'
    result = subprocess.run([sys.executable, '-c', code], capture_output=True, text=True)

    elapsed = float(result.stdout.strip())
    # Note: Using 0.25s as a conservative threshold for CI environments which might be slower
    assert elapsed < 0.25, f"Import too slow: {elapsed:.3f}s"
