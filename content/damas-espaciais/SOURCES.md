# Damas Espaciais

- Design and first-person copy: user-supplied `Project · Damas Espaciais-html.zip`,
  `Damas.dc.html`. The original ten menu, board, rocket and screen images are
  copied unchanged to `img/damas-espaciais/` with descriptive names.
- Code and technical claims: [project repository](https://github.com/Raiagues/Jogo-Damas-Espaciais/tree/7d8acc3be2baf779bddefa17f8d8a95b51491807),
  README, `src/game.c`, `src/game.h`, `src/web.c`, `tests/test_game.c` and
  `docs/TECHNICAL_EVIDENCE.md`, checked on 25 October 2026.
- The supplied prototype duplicated the C rules in JavaScript. The production
  page instead uses the original C engine compiled to WebAssembly, retaining the
  prototype's board and move-inspector design. It is a local two-player game.
- The current source documents 5,446 native checks, including 3,200 exhaustive
  square/direction cases. Stale restored-file line counts were replaced with
  descriptions of each module's responsibility. The historic 1,587-line figure
  concerns the preserved 2021 file, not the current implementation.
- Professor: [Marcelo Serrano Zanetti — UFSM institucional profile](https://ufsmpublica.ufsm.br/docente/17861),
  based on his Lattes CV (last updated 22 June 2026). Lists a master's in Computer
  Science and doctorate in Complex Systems from ETH Zürich. The page deliberately
  omits degree years: UFSM's two faculty profiles disagree on 2013 versus 2014 for
  the doctorate. ETH Zürich is his educational institution; the project and course
  took place at UFSM. The professor provided the base Pong code, as stated in the
  supplied project content; the game implementation is Emilly's.

The ZIP and extracted design references are kept locally under the ignored
`local-reference/designs/`. They are not part of the public build.
