import re
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from typing import Optional


sample = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""


class GF2Matrix:
    """Matrix operations over GF(2) (binary field) where addition is XOR."""
    
    def __init__(self, rows: int, cols: int):
        """Initialize matrix with zeros."""
        self.rows = rows
        self.cols = cols
        self.data = [[0 for _ in range(cols)] for _ in range(rows)]
    
    def set(self, row: int, col: int, value: int):
        """Set matrix element (value must be 0 or 1)."""
        self.data[row][col] = value % 2
    
    def get(self, row: int, col: int) -> int:
        """Get matrix element."""
        return self.data[row][col]
    
    def swap_rows(self, row1: int, row2: int):
        """Swap two rows in the matrix."""
        self.data[row1], self.data[row2] = self.data[row2], self.data[row1]
    
    def add_row(self, target_row: int, source_row: int):
        """Add source_row to target_row (XOR operation in GF(2))."""
        for col in range(self.cols):
            self.data[target_row][col] ^= self.data[source_row][col]
    
    def copy(self):
        """Create a deep copy of the matrix."""
        new_matrix = GF2Matrix(self.rows, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                new_matrix.data[i][j] = self.data[i][j]
        return new_matrix
    
    def gaussian_elimination(self) -> bool:
        """
        Perform Gaussian elimination to row echelon form.
        Returns True if system is consistent, False otherwise.
        """
        current_row = 0
        
        for col in range(self.cols - 1):  # Don't process the augmented column
            # Find pivot (first 1 in this column at or below current_row)
            pivot_row = None
            for row in range(current_row, self.rows):
                if self.get(row, col) == 1:
                    pivot_row = row
                    break
            
            if pivot_row is None:
                continue  # No pivot in this column, move to next
            
            # Swap to bring pivot to current_row
            if pivot_row != current_row:
                self.swap_rows(current_row, pivot_row)
            
            # Eliminate all other 1s in this column
            for row in range(self.rows):
                if row != current_row and self.get(row, col) == 1:
                    self.add_row(row, current_row)
            
            current_row += 1
        
        # Check for inconsistency (row of form [0 0 ... 0 | 1])
        for row in range(self.rows):
            all_zeros = all(self.get(row, col) == 0 for col in range(self.cols - 1))
            if all_zeros and self.get(row, self.cols - 1) == 1:
                return False  # Inconsistent system
        
        return True
    
    def get_pivot_columns(self):
        """
        Identify pivot columns (columns with leading 1s in row echelon form).
        Returns set of column indices that are pivot columns.
        """
        pivot_cols = set()
        for row in range(self.rows):
            for col in range(self.cols - 1):
                if self.get(row, col) == 1:
                    pivot_cols.add(col)
                    break  # Found leading 1, move to next row
        return pivot_cols
    
    def extract_solution(self) -> Optional[list[int]]:
        """
        Extract solution from row echelon form.
        Returns solution vector or None if no solution exists.
        """
        solution = [0] * (self.cols - 1)
        
        for row in range(self.rows):
            # Find the leading 1 in this row
            leading_col = None
            for col in range(self.cols - 1):
                if self.get(row, col) == 1:
                    leading_col = col
                    break
            
            if leading_col is not None:
                # Set solution value from augmented column
                solution[leading_col] = self.get(row, self.cols - 1)
        
        return solution
    
    def get_free_variables(self) -> list[int]:
        """
        Identify free variables (non-pivot columns).
        Returns list of column indices that are free variables.
        """
        pivot_cols = self.get_pivot_columns()
        free_vars = [col for col in range(self.cols - 1) if col not in pivot_cols]
        return free_vars
    
    def __str__(self) -> str:
        """String representation for debugging."""
        lines = []
        for row in self.data:
            lines.append(' '.join(str(x) for x in row))
        return '\n'.join(lines)


class ButtonPuzzleSolver:
    """Solve the button toggle puzzle using linear algebra over GF(2)."""
    
    def __init__(self, chars: list[str], button_lists: list[list[int]]):
        """Initialize solver with parsed puzzle data."""
        # Convert chars to binary (. → 0, # → 1)
        self.target_state = [1 if c == '#' else 0 for c in chars]
        self.buttons = button_lists
        self.num_positions = len(chars)
        self.num_buttons = len(button_lists)
        self.matrix: Optional[GF2Matrix] = None
    
    def build_matrix(self):
        """Construct the augmented matrix [A|b]."""
        # Create matrix: rows = positions, cols = buttons + 1 (for target)
        self.matrix = GF2Matrix(self.num_positions, self.num_buttons + 1)
        
        # Fill in button effects
        for button_idx, positions in enumerate(self.buttons):
            for pos in positions:
                if 0 <= pos < self.num_positions:
                    self.matrix.set(pos, button_idx, 1)
        
        # Fill in target state (augmented column)
        for pos, target_val in enumerate(self.target_state):
            self.matrix.set(pos, self.num_buttons, target_val)
    
    def verify_solution(self, solution: list[int]) -> bool:
        """Verify that a solution produces the target state."""
        # Start with all 0s
        state = [0] * self.num_positions
        
        # Apply each button press
        for button_idx, press_count in enumerate(solution):
            if press_count % 2 == 1:  # Only odd presses matter (toggle)
                for pos in self.buttons[button_idx]:
                    if 0 <= pos < self.num_positions:
                        state[pos] ^= 1
        
        # Compare with target
        return state == self.target_state
    
    def generate_solutions_from_free_vars(self, base_solution: list[int],
                                         free_vars: list[int],
                                         work_matrix: GF2Matrix) -> list[list[int]]:
        """
        Generate all possible solutions by trying all combinations of free variables.
        """
        if not free_vars:
            return [base_solution[:]]
        
        solutions = []
        # Try all 2^n combinations of free variables
        for mask in range(1 << len(free_vars)):
            solution = base_solution[:]
            
            # Set free variables according to mask
            for i, free_var in enumerate(free_vars):
                solution[free_var] = (mask >> i) & 1
            
            # Back-substitute to find dependent variables
            for row in range(work_matrix.rows):
                # Find the leading 1 (pivot column)
                leading_col = None
                for col in range(work_matrix.cols - 1):
                    if work_matrix.get(row, col) == 1:
                        leading_col = col
                        break
                
                if leading_col is not None:
                    # Calculate value for this pivot variable
                    value = work_matrix.get(row, work_matrix.cols - 1)  # RHS
                    for col in range(leading_col + 1, work_matrix.cols - 1):
                        if work_matrix.get(row, col) == 1:
                            value ^= solution[col]
                    solution[leading_col] = value
            
            # Verify this solution works
            if self.verify_solution(solution):
                solutions.append(solution)
        
        return solutions
    
    def solve(self) -> Optional[tuple[int, list[int]]]:
        """
        Solve the puzzle and return (min_presses, button_indices).
        Returns None if no solution exists.
        """
        # Build the matrix
        self.build_matrix()
        
        # Create a copy for manipulation
        work_matrix = self.matrix.copy()
        
        # Perform Gaussian elimination
        if not work_matrix.gaussian_elimination():
            return None  # No solution exists
        
        # Get free variables
        free_vars = work_matrix.get_free_variables()
        
        # Extract base solution
        base_solution = work_matrix.extract_solution()
        if base_solution is None:
            return None
        
        # Generate all possible solutions
        all_solutions = self.generate_solutions_from_free_vars(
            base_solution, free_vars, work_matrix
        )
        
        if not all_solutions:
            return None
        
        # Find solution with minimum button presses
        min_solution = min(all_solutions, key=lambda s: sum(s))
        
        # Count presses and get button indices
        button_indices = [i for i, val in enumerate(min_solution) if val == 1]
        min_presses = len(button_indices)
        
        return min_presses, button_indices


class IntegerIncrementSolver:
    """Solve the integer increment puzzle using Linear Programming."""
    
    def __init__(self, button_lists: list[list[int]], target_values: list[int]):
        """Initialize solver with button definitions and target values."""
        self.buttons = button_lists
        self.targets = target_values
        self.num_positions = len(target_values)
        self.num_buttons = len(button_lists)
    
    def build_coefficient_matrix(self) -> np.ndarray:
        """
        Build the coefficient matrix A where A[i,j] = 1 if button j affects position i.
        Returns numpy array of shape (num_positions, num_buttons).
        """
        A = np.zeros((self.num_positions, self.num_buttons), dtype=int)
        for button_idx, positions in enumerate(self.buttons):
            for pos in positions:
                if 0 <= pos < self.num_positions:
                    A[pos, button_idx] = 1
        return A
    
    def solve(self) -> Optional[tuple[int, list[int]]]:
        """
        Solve using Integer Linear Programming.
        Returns (total_presses, button_press_counts) or None if no solution exists.
        """
        # Build coefficient matrix
        A = self.build_coefficient_matrix()
        b = np.array(self.targets, dtype=float)
        c = np.ones(self.num_buttons)  # Minimize sum of all button presses
        
        # Set up constraints: A × x = b, x ≥ 0
        constraints = LinearConstraint(A, lb=b, ub=b)
        bounds = Bounds(lb=0, ub=np.inf)
        
        # Solve as MILP (Mixed Integer Linear Program)
        integrality = np.ones(self.num_buttons)  # All variables are integers
        
        try:
            result = milp(
                c=c,
                constraints=constraints,
                bounds=bounds,
                integrality=integrality
            )
            
            if result.success:
                solution = np.round(result.x).astype(int)
                
                # Verify the solution
                if self.verify_solution(solution.tolist()):
                    total_presses = int(np.sum(solution))
                    return total_presses, solution.tolist()
                else:
                    return None
            else:
                return None
        except Exception as e:
            print(f"Error solving ILP: {e}")
            return None
    
    def verify_solution(self, solution: list[int]) -> bool:
        """
        Verify that button presses produce target values.
        Returns True if solution is correct, False otherwise.
        """
        state = [0] * self.num_positions
        
        # Apply each button press
        for button_idx, press_count in enumerate(solution):
            for pos in self.buttons[button_idx]:
                if 0 <= pos < self.num_positions:
                    state[pos] += press_count
        
        # Compare with target
        return state == self.targets


def solve_increment_puzzle(button_lists: list[list[int]], target_values: list[int]) -> dict:
    """
    High-level function to solve the integer increment puzzle.
    
    Args:
        button_lists: List of button definitions (which positions each button affects)
        target_values: Target values for each position
    
    Returns:
        Dictionary with solution details including total_presses and button_counts.
    """
    solver = IntegerIncrementSolver(button_lists, target_values)
    result = solver.solve()
    
    if result is None:
        return {
            'target_values': target_values,
            'total_presses': None,
            'button_counts': [],
            'solution_exists': False,
            'verification': False
        }
    
    total_presses, button_counts = result
    
    return {
        'target_values': target_values,
        'total_presses': total_presses,
        'button_counts': button_counts,
        'solution_exists': True,
        'verification': True
    }



def solve_puzzle(chars: list[str], button_lists: list[list[int]]) -> dict:
    """
    High-level function to solve a single puzzle instance.
    
    Returns:
        Dictionary with solution details including min_presses and buttons_pressed.
    """
    solver = ButtonPuzzleSolver(chars, button_lists)
    result = solver.solve()
    
    if result is None:
        return {
            'target': chars,
            'min_presses': None,
            'buttons_pressed': [],
            'solution_exists': False,
            'verification': False
        }
    
    min_presses, button_indices = result
    
    return {
        'target': chars,
        'min_presses': min_presses,
        'buttons_pressed': button_indices,
        'solution_exists': True,
        'verification': True
    }


def parse_line(line):
    """
    Parse a line to extract:
    - Characters between []
    - List of number lists between ()
    - List of numbers between {}
    
    Returns: (chars, number_lists, final_numbers)
    """
    # Extract characters between []
    bracket_match = re.search(r'\[(.*?)\]', line)
    chars = list(bracket_match.group(1)) if bracket_match else []
    
    # Extract all number lists between ()
    paren_matches = re.findall(r'\(([^)]*)\)', line)
    number_lists = []
    for match in paren_matches:
        if match.strip():
            numbers = [int(n.strip()) for n in match.split(',')]
            number_lists.append(numbers)
        else:
            number_lists.append([])
    
    # Extract numbers between {}
    brace_match = re.search(r'\{([^}]*)\}', line)
    final_numbers = []
    if brace_match:
        final_numbers = [int(n.strip()) for n in brace_match.group(1).split(',')]
    
    return chars, number_lists, final_numbers


def parse_input(text):
    """
    Parse multi-line input and return parsed data for each line.
    
    Returns: List of tuples (chars, number_lists, final_numbers)
    """
    lines = text.strip().split('\n')
    results = []
    for line in lines:
        results.append(parse_line(line))
    return results


def main():
    # Read input from file
    try:
        with open('input.txt', 'r') as f:
            input_text = f.read()
    except FileNotFoundError:
        print("Error: input.txt not found")
        return
    
    # Parse all lines
    lines = input_text.strip().split('\n')
    
    print("=" * 80)
    print("BUTTON PUZZLE SOLVER - PART 1 & PART 2")
    print("=" * 80)
    
    total_button_presses_part1 = 0
    total_button_presses_part2 = 0
    puzzles_solved_part1 = 0
    puzzles_solved_part2 = 0
    
    # Solve each puzzle
    for i, line in enumerate(lines, 1):
        chars, button_lists, final_numbers = parse_line(line)
        
        print(f"\n{'=' * 80}")
        print(f"Puzzle {i}")
        print(f"{'=' * 80}")
        print(f"Number of positions: {len(chars)}")
        print(f"Number of buttons: {len(button_lists)}")
        
        # Display button definitions
        print(f"\nButton definitions:")
        for btn_idx, positions in enumerate(button_lists):
            print(f"  Button {btn_idx}: affects positions {positions}")
        
        # ===== PART 1: Toggle Puzzle =====
        print(f"\n{'─' * 80}")
        print("PART 1: Toggle Puzzle (reach pattern from all dots)")
        print(f"{'─' * 80}")
        print(f"Target pattern: {''.join(chars)}")
        
        result_part1 = solve_puzzle(chars, button_lists)
        
        if result_part1['solution_exists']:
            print(f"✓ Solution found!")
            print(f"  Minimum presses: {result_part1['min_presses']}")
            print(f"  Buttons to press: {result_part1['buttons_pressed']}")
            print(f"  Verification: {'PASS ✓' if result_part1['verification'] else 'FAIL ✗'}")
            
            total_button_presses_part1 += result_part1['min_presses']
            puzzles_solved_part1 += 1
            
            if result_part1['buttons_pressed']:
                print(f"\n  Press sequence:")
                for btn in result_part1['buttons_pressed']:
                    positions = button_lists[btn]
                    print(f"    - Press button {btn} (toggles {positions})")
        else:
            print(f"✗ No solution exists for Part 1")
        
        # ===== PART 2: Increment Puzzle =====
        if final_numbers:
            print(f"\n{'─' * 80}")
            print("PART 2: Increment Puzzle (reach values from all zeros)")
            print(f"{'─' * 80}")
            print(f"Target values: {final_numbers}")
            
            result_part2 = solve_increment_puzzle(button_lists, final_numbers)
            
            if result_part2['solution_exists']:
                print(f"✓ Solution found!")
                print(f"  Total button presses: {result_part2['total_presses']}")
                print(f"  Verification: {'PASS ✓' if result_part2['verification'] else 'FAIL ✗'}")
                
                total_button_presses_part2 += result_part2['total_presses']
                puzzles_solved_part2 += 1
                
                # Show button press counts
                print(f"\n  Button press counts:")
                for btn_idx, count in enumerate(result_part2['button_counts']):
                    if count > 0:
                        positions = button_lists[btn_idx]
                        print(f"    - Button {btn_idx}: {count} presses (increments {positions})")
            else:
                print(f"✗ No solution exists for Part 2")
    
    # Final summary
    print(f"\n{'=' * 80}")
    print("SUMMARY")
    print(f"{'=' * 80}")
    print(f"\nPart 1 (Toggle):")
    print(f"  Puzzles solved: {puzzles_solved_part1}")
    print(f"  Total button presses: {total_button_presses_part1}")
    
    if puzzles_solved_part2 > 0:
        print(f"\nPart 2 (Increment):")
        print(f"  Puzzles solved: {puzzles_solved_part2}")
        print(f"  Total button presses: {total_button_presses_part2}")
    
    print(f"{'=' * 80}\n")


if __name__ == "__main__":
    main()
