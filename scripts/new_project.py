#!/usr/bin/env python3
"""Create a new AVR project directory based on the template."""

import argparse
import re
import shutil
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = WORKSPACE / "template"

REPLACE_KEYS = frozenset({"DEVICE", "CLOCK", "PROGRAMMER", "FUSES"})


def replace_makefile_vars(target: Path, overrides: dict[str, str]) -> None:
    if not overrides:
        return
    data = target.read_text()
    for key, value in overrides.items():
        if key not in REPLACE_KEYS:
            continue
        pattern = re.compile(rf"^{key}\s*=\s*.*$", re.MULTILINE)
        data, count = pattern.subn(f"{key} = {value}", data, count=1)
        if count == 0:
            raise SystemExit(f"{key} not found in {target}")
    target.write_text(data)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Copy the template directory and adjust Makefile defaults for a new AVR project"
    )
    parser.add_argument("name", help="Directory name for the new project")
    parser.add_argument("--device", help="MCU device (default attiny85)")
    parser.add_argument("--clock", help="Clock frequency in Hz")
    parser.add_argument("--programmer", help="Programmer string (eg. -c usbasp)")
    parser.add_argument("--fuses", help="Fuse settings (eg. -U lfuse:w:0x62:m ...)")
    args = parser.parse_args()

    target = WORKSPACE / args.name
    if target.exists():
        raise SystemExit(f"{target} already exists")
    shutil.copytree(TEMPLATE_DIR, target)

    overrides = {}
    if args.device:
        overrides["DEVICE"] = args.device
    if args.clock:
        overrides["CLOCK"] = args.clock
    if args.programmer:
        overrides["PROGRAMMER"] = args.programmer
    if args.fuses:
        overrides["FUSES"] = args.fuses

        if overrides:
            makefile = target / "Makefile"
            replace_makefile_vars(makefile, overrides)

        print(f"Created {target}")


if __name__ == "__main__":
    main()
