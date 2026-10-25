#ifndef SPACE_CHECKERS_GAME_H
#define SPACE_CHECKERS_GAME_H

#include <stdbool.h>

enum { EMPTY, BLUE, PINK, BLUE_KING, PINK_KING };

typedef struct {
    int board[8][8];
    int turn;
} Game;

bool game_inside(int row, int col);
int game_owner(int piece);
void game_reset(Game *game);
int game_count(const Game *game, int player);
bool game_can_move(const Game *game, int row, int col, int to_row, int to_col);
bool game_has_moves(const Game *game, int player);
/* Returns false without changing the board or turn for an invalid move.
 * A destination on the source square passes the turn, as in the original game.
 * A capture accepts either the opposing piece or its empty landing square. */
bool game_move(Game *game, int row, int col, int to_row, int to_col);
int game_winner(const Game *game);

#endif
