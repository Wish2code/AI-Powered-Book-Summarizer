#!/usr/bin/env python3
"""
Minimal launcher for the Streamlit book summarizer.
"""

import subprocess
import sys


def main():
    print("Starting Streamlit app...")
    print("If dependencies are missing, install with: pip install -r requirements.txt\n")
    try:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                "app.py",
                "--server.port",
                "8501",
                "--server.address",
                "0.0.0.0",
            ],
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        print(f"Streamlit exited with an error: {exc}")
        sys.exit(exc.returncode)
    except KeyboardInterrupt:
        print("\nStopping Streamlit...")


if __name__ == "__main__":
    main()
