#!/usr/bin/env python3
"""Optional reproducible build of the vendored C rules; requires clang and wasm-ld.

The normal portfolio build uses the checked-in module and needs only Python.
"""
from pathlib import Path
import subprocess

source = Path(__file__).resolve().parents[1] / 'src/damas-engine'
exports = ['reset', 'turn', 'piece', 'move', 'can_move', 'count', 'winner', 'state_bytes']
subprocess.run([
    'clang', '--target=wasm32-unknown-unknown', '-std=c99', '-O2', '-nostdlib',
    '-fno-builtin', '-Wall', '-Wextra', '-Wpedantic', '-Werror',
    '-Wl,--no-entry', '-Wl,--export-memory', '-Wl,--initial-memory=131072',
    '-Wl,--max-memory=131072', '-Wl,-z,stack-size=16384', '-Wl,--strip-all',
    *[f'-Wl,--export=web_{name}' for name in exports],
    str(source / 'game.c'), str(source / 'web.c'), '-o', str(source / 'game.wasm'),
], check=True)
print(f'Built {(source / "game.wasm").stat().st_size} bytes from the shared C rules.')
