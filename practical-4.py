# Practical 4: Constraint Satisfaction Problem using Branch and Bound and Backtracking for n-queens problem

def read_board_size():
    """Read board size."""
    while True:
        try:
            size = int(input("Enter number of queens: "))
            if size > 0:
                return size
            print("Please enter a number greater than 0.")
        except ValueError:
            print("Please enter a valid integer.")


def read_solution_choice():
    """Ask how many solutions to display."""
    while True:
        print("\nChoose output option:")
        print("1. Show one solution")
        print("2. Show all solutions")

        choice = input("Enter your choice: ")
        if choice in ["1", "2"]:
            return choice

        print("Invalid choice. Please enter 1 or 2.")


class NQueensSolver:
    def __init__(self, size):
        self.size = size
        self.board = [["." for _ in range(size)] for _ in range(size)]
        self.solutions = []

        self.used_columns = set()
        self.used_left_diagonals = set()
        self.used_right_diagonals = set()

    def is_safe(self, row, column):
        """Check if a queen can be placed."""
        left_diagonal = row - column
        right_diagonal = row + column

        return (
            column not in self.used_columns
            and left_diagonal not in self.used_left_diagonals
            and right_diagonal not in self.used_right_diagonals
        )

    def place_queen(self, row, column):
        """Place a queen."""
        self.board[row][column] = "Q"
        self.used_columns.add(column)
        self.used_left_diagonals.add(row - column)
        self.used_right_diagonals.add(row + column)

    def remove_queen(self, row, column):
        """Remove a queen."""
        self.board[row][column] = "."
        self.used_columns.remove(column)
        self.used_left_diagonals.remove(row - column)
        self.used_right_diagonals.remove(row + column)

    def solve(self, row=0):
        """Find all solutions using backtracking."""
        if row == self.size:
            self.solutions.append([board_row.copy() for board_row in self.board])
            return

        for column in range(self.size):
            if self.is_safe(row, column):
                self.place_queen(row, column)
                self.solve(row + 1)
                self.remove_queen(row, column)

    def print_board(self, board):
        """Display the board."""
        cell_width = len(str(self.size)) + 2
        label_width = len(str(self.size))
        horizontal_border = (
            " " * (label_width + 1)
            + "+"
            + "+".join("-" * cell_width for _ in range(self.size))
            + "+"
        )

        column_labels = " " * (label_width + 2)
        column_labels += " ".join(
            f"{column:^{cell_width}}" for column in range(1, self.size + 1)
        )
        print(column_labels)
        print(horizontal_border)

        for row_index, row in enumerate(board, start=1):
            cells = "|".join(f"{value:^{cell_width}}" for value in row)
            print(f"{row_index:>{label_width}} |{cells}|")
            print(horizontal_border)


def main():
    size = read_board_size()
    choice = read_solution_choice()
    solver = NQueensSolver(size)

    print(f"\nSolving {size}-Queens Problem using Backtracking and Branch and Bound...")

    solver.solve()

    if solver.solutions:
        if choice == "1":
            print("\nOne Solution Found:")
            solver.print_board(solver.solutions[0])
        else:
            print(f"\n{len(solver.solutions)} Solution(s) Found:")
            for index, solution in enumerate(solver.solutions, start=1):
                print(f"\nSolution {index}:")
                solver.print_board(solution)
    else:
        print("\nNo solution exists.")


if __name__ == "__main__":
    main()