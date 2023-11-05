import itertools
from enum import Enum
from typing import Optional


class Player(Enum):
    RED = "R"
    YELLOW = "Y"


class Board:
    _DIRECTIONS = set(itertools.product([-1, 0, 1], [-1, 0, 1])) - set(
        [(0, 0), (-1, 0)]
    )

    def __init__(self, width: int = 7, height: int = 6, n: int = 4):
        assert width > 0
        assert height > 0
        assert n > 0 and n <= max(width, height)

        self._width = width
        self._height = height
        self._n = n

        self._board: list[list[Optional[Player]]] = [
            [None for _ in range(width)] for _ in range(height)
        ]
        self.num_cells_empty = width * height

    def _add_cell(self, column: int, player: Player) -> Optional[int]:
        if column < 0 or column >= self._width:
            return None

        bottommost_index = None
        for y in range(self._height):
            from_bottom: int = self._height - y - 1
            if self._board[from_bottom][column] is None:
                bottommost_index = from_bottom
                break

        if bottommost_index is None:
            return None
        self._board[bottommost_index][column] = player
        return bottommost_index

    def move(self, column: int, player: Player) -> Optional[bool]:
        """Takes in a (zero-indexed) column number and the player that's making the move.
        Returns if the move led to the player winning; and None if move was invalid."""
        row = self._add_cell(column, player)
        if row is None:
            return None

        self.num_cells_empty -= 1

        for i, j in Board._DIRECTIONS:
            valid = True
            for k in range(1, self._n):
                new_row = row + (i * k)
                new_col = column + (j * k)
                if (
                    new_row < 0
                    or new_row >= self._height
                    or new_col < 0
                    or new_col >= self._width
                    or self._board[new_row][new_col] != player
                ):
                    valid = False
                    break
            if valid:
                return valid
        return False

    def __str__(self):
        return "\n".join(
            [
                " ".join([cell.value if cell is not None else "." for cell in row])
                for row in self._board
            ]
        )


def main():
    while True:
        board = Board()
        print(board)
        player = Player.RED
        while True:
            column = input(
                f"What column do you want to put your cell in, Player {player.value}? "
            )
            if not column.isdigit():
                print("Write an valid input please! ")
                continue
            column = int(column)
            move_result = board.move(column, player)
            if move_result is None:
                print("You can't place that there! ")
                continue
            if board.num_cells_empty == 0:
                print("The game is a tie. :) ")
                break

            print(board)

            if move_result:
                print(f"Player {player.value} won! Congratulate them! :) ")
                break

            player = Player.RED if player == Player.YELLOW else Player.YELLOW

        promptResponse = input("Do you want to play again? :) (Write yes if so) ")
        if promptResponse.lower().startswith("y"):
            continue

        print("Thanks for playing! :) ")
        break


if __name__ == "__main__":
    main()
