/* Browser bridge. All rules are implemented by the same game.c as the desktop. */
#include "game.h"

static Game game;

void web_reset(void) { game_reset(&game); }
int web_turn(void) { return game.turn; }
int web_piece(int row, int col)
{
    return game_inside(row, col) ? game.board[row][col] : -1;
}
int web_move(int row, int col, int to_row, int to_col)
{
    if (game_winner(&game)) return 0;
    return game_move(&game, row, col, to_row, to_col);
}
int web_can_move(int row, int col, int to_row, int to_col)
{
    return game_can_move(&game, row, col, to_row, to_col);
}
int web_count(int player) { return game_count(&game, player); }
int web_winner(void) { return game_winner(&game); }
int web_state_bytes(void) { return (int)sizeof(game); }
