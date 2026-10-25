# Damas Espaciais — shared C rules

Unmodified `src/game.c`, `src/game.h`, `src/web.c` and `LICENSE` from
[Raiagues/Jogo-Damas-Espaciais](https://github.com/Raiagues/Jogo-Damas-Espaciais/tree/7d8acc3be2baf779bddefa17f8d8a95b51491807),
revision `7d8acc3be2baf779bddefa17f8d8a95b51491807` (25 October 2026).
The included GPL-3.0 license applies to this engine.

`game.wasm` is compiled from these files. Rebuild from the portfolio root with
`python3 scripts/build_damas_engine.py` using Clang and wasm-ld. The normal site
build uses this checked-in module and does not download or compile dependencies.

The module has no imports or heap allocation. Its linear memory is fixed at
128 KiB; the board and turn occupy 260 bytes. These figures describe the C/Wasm
module, not total browser memory. Moves, passing, captures, promotion and victory
are decided by this engine; `src/damas.js` only draws the interface and explains
the checks. All source required to rebuild the module is published beside it.
