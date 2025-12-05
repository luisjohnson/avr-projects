#!/usr/bin/env python3
"""Generate the VS Code C/C++ IntelliSense configuration per host OS."""

import json
import platform
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[1]
VCODE_DIR = WORKSPACE / ".vscode"
VCODE_DIR.mkdir(exist_ok=True)
TARGET = VCODE_DIR / "c_cpp_properties.json"

COMMON = {
    "name": "AVR",
    "defines": ["F_CPU=8000000UL"],
    "cStandard": "c11",
    "cppStandard": "c++17",
    "intelliSenseMode": "gcc-x64",
}

CONFIGS = {
    "Darwin": {
        "includePath": [
            "${workspaceFolder}/**",
            "/opt/homebrew/Cellar/avr-gcc@9/9.5.0/avr/include",
            "/opt/homebrew/Cellar/avr-gcc@9/9.5.0/lib/avr-gcc/9/gcc/avr/9.5.0/include",
            "/opt/homebrew/Cellar/avr-gcc@9/9.5.0/lib/avr-gcc/9/gcc/avr/9.5.0/include-fixed",
        ],
        "compilerPath": "/opt/homebrew/bin/avr-gcc",
        "browse": {
            "path": [
                "${workspaceFolder}/**",
                "/opt/homebrew/Cellar/avr-gcc@9/9.5.0/avr/include",
            ],
            "limitSymbolsToIncludedHeaders": True,
        },
    },
    "Linux": {
        "includePath": [
            "${workspaceFolder}/**",
            "/usr/lib/avr/include",
            "/usr/lib/gcc/avr/11/include",
            "/usr/lib/gcc/avr/9/include",
            "/usr/include",
        ],
        "compilerPath": "/usr/bin/avr-gcc",
        "browse": {
            "path": [
                "${workspaceFolder}/**",
                "/usr/lib/avr/include",
            ],
            "limitSymbolsToIncludedHeaders": True,
        },
    },
}


def main() -> None:
    system = platform.system()
    config = CONFIGS.get(system)
    if config is None:
        raise SystemExit(f"Unsupported platform: {system}")

    payload = {
        "configurations": [
            {**COMMON, **config},
        ],
        "version": 4,
    }
    TARGET.write_text(json.dumps(payload, indent=2))
    print(f"Wrote {TARGET} for {system}")


if __name__ == "__main__":
    main()
