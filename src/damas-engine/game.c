#include "game.h"

static int magnitude(int value)
{
    return value < 0 ? -value : value;
}

bool game_inside(int row, int col)
{
    return row >= 0 && row < 8 && col >= 0 && col < 8;
}

int game_owner(int piece)
{
    if (piece == BLUE || piece == BLUE_KING) return BLUE;
    if (piece == PINK || piece == PINK_KING) return PINK;
    return EMPTY;
}

void game_reset(Game *game)
{
    game->turn = BLUE;
    for (int row = 0; row < 8; ++row) {
        for (int col = 0; col < 8; ++col) {
            game->board[row][col] = EMPTY;
            if ((row + col) % 2 == 1) {
                if (row < 3) game->board[row][col] = BLUE;
                if (row > 4) game->board[row][col] = PINK;
            }
        }
    }
}

int game_count(const Game *game, int player)
{
    int count = 0;
    for (int row = 0; row < 8; ++row)
        for (int col = 0; col < 8; ++col)
            if (game_owner(game->board[row][col]) == player) ++count;
    return count;
}

/* Resolve the original click-on-opponent control before validating a move. */
static void landing(const Game *game, int player, int row, int col, int *to_row, int *to_col)
{
    if (game_inside(*to_row, *to_col) &&
        magnitude(*to_row - row) == 1 && magnitude(*to_col - col) == 1 &&
        game_owner(game->board[*to_row][*to_col]) == 3 - player) {
        *to_row += *to_row - row;
        *to_col += *to_col - col;
    }
}

static bool can_move_for(const Game *game, int player, int row, int col, int to_row, int to_col)
{
    if (!game_inside(row, col) || !game_inside(to_row, to_col)) return false;
    const int piece = game->board[row][col];
    if (game_owner(piece) != player) return false;
    landing(game, player, row, col, &to_row, &to_col);
    if (!game_inside(to_row, to_col) || game->board[to_row][to_col] != EMPTY)
        return false;
    const int dr = to_row - row;
    const int dc = to_col - col;
    if (magnitude(dr) != magnitude(dc) || magnitude(dr) < 1 || magnitude(dr) > 2) return false;
    if ((piece == BLUE && dr < 0) || (piece == PINK && dr > 0)) return false;
    if (magnitude(dr) == 2 &&
        game_owner(game->board[row + dr / 2][col + dc / 2]) != 3 - player)
        return false;
    return true;
}

bool game_can_move(const Game *game, int row, int col, int to_row, int to_col)
{
    return can_move_for(game, game->turn, row, col, to_row, to_col);
}

bool game_has_moves(const Game *game, int player)
{
    for (int row = 0; row < 8; ++row) {
        for (int col = 0; col < 8; ++col) {
            if (game_owner(game->board[row][col]) != player) continue;
            for (int dr = -2; dr <= 2; ++dr)
                for (int dc = -2; dc <= 2; ++dc)
                    if (can_move_for(game, player, row, col, row + dr, col + dc))
                        return true;
        }
    }
    return false;
}

bool game_move(Game *game, int row, int col, int to_row, int to_col)
{
    if (!game_inside(row, col) || !game_inside(to_row, to_col) ||
        game_owner(game->board[row][col]) != game->turn) return false;
    if (row == to_row && col == to_col) {
        game->turn = 3 - game->turn;
        return true;
    }
    if (!game_can_move(game, row, col, to_row, to_col)) return false;
    landing(game, game->turn, row, col, &to_row, &to_col);
    int piece = game->board[row][col];
    if (magnitude(to_row - row) == 2)
        game->board[(row + to_row) / 2][(col + to_col) / 2] = EMPTY;
    game->board[row][col] = EMPTY;
    if (piece == BLUE && to_row == 7) piece = BLUE_KING;
    if (piece == PINK && to_row == 0) piece = PINK_KING;
    game->board[to_row][to_col] = piece;
    game->turn = 3 - game->turn;
    return true;
}

int game_winner(const Game *game)
{
    if (game_count(game, BLUE) == 0) return PINK;
    if (game_count(game, PINK) == 0) return BLUE;
    if (!game_has_moves(game, game->turn)) return 3 - game->turn;
    return EMPTY;
}
