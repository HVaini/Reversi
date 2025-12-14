from reversi.board import (
    new_board, print_board, play_move, valid_moves,
    get_opponent, black_piece, white_piece,
    count_points, end_game
)
from AI.ai_move import ai_move



def main():
    """
    Käynnistää pelin ja sisältää sen ulkoisen käyttöliittymän,
    vuorojen siirron, siirtojen laillisuuden tarkistuksen sekä pelin
    päättymisehtojen tarkistuksen.
    """
    board = new_board()
    current_player = black_piece

    choice = input("Valitse X (aloittava) painamalla 1 tai O painamalla 2:")
    if choice == "2":
        human_player = white_piece
        ai_player = black_piece
    else:
        human_player = black_piece
        ai_player = white_piece

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
        if current_player == ai_player:
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
            print("Anna siirto muodossa kaksi numeroa välillä 0-7, esim. 2 3.")


if __name__ == "__main__":
    main()
