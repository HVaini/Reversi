from reversi.board import (
    new_board, print_board, play_move, valid_moves,
    get_opponent, black_piece, white_piece,
    count_points, end_game, empty_slot
)
from AI.minimax_endscore import minimax_endscore
from AI.random_ai import random_ai
import random, copy

def ai_move(board, player):
    empty_count = sum(row.count(empty_slot) for row in board)
    moves = valid_moves(board, player)
    if not moves:
        return None

    if empty_count <= 7:
        val, best = minimax_endscore(copy.deepcopy(board), player)
        print(f"Tekoälyn arvio: {val}")
        print(f"Tekoälyn siirto: {best}")
        return best
    else:
        move = random.choice(moves)
        print(f"Tekoälyn siirto: {move}")
        return move


def main():
    board = new_board()
    current_player = black_piece

    while True:
        print_board(board)
        b_score, w_score = count_points(board)
        print(f"\nPisteet X: {b_score}  O: {w_score}")

        if end_game(board):
            print("\nPeli päättyi.")
            if b_score > w_score:
                print(f"Voittaja: X ({b_score} - {w_score})")
            elif w_score > b_score:
                print(f"Voittaja: O ({w_score} - {b_score})")
            else:
                print("Tasapeli")
            break

        valid = valid_moves(board, current_player)
        if not valid:
            print(f"Ei laillisia siirtoja pelaajalle {current_player}. Vuoro siirtyy.")
            current_player = get_opponent(current_player)
            continue

        # AI:n vuoro
        if current_player == white_piece:
            move = ai_move(board, current_player)
            if move:
                play_move(board, move, current_player)
            current_player = get_opponent(current_player)
            continue

        # Ihmisen vuoro
        print(f"\nLailliset siirrot: {valid}")
        move_input = input("Anna siirto muodossa 'rivi sarake': ")
        try:
            r, c = map(int, move_input.split())
            if (r, c) in valid:
                play_move(board, (r, c), current_player)
                current_player = get_opponent(current_player)
            else:
                print("Virheellinen siirto, yritä uudelleen.")
        except Exception:
            print("Anna siirto muodossa kaksi numeroa, esim. 2 3.")


if __name__ == "__main__":
    main()
