# Implementation Specification

## Module Structure

```
main.py
├── Existing: parse_line(), parse_input()
└── New additions:
    ├── class GF2Matrix          # Matrix operations over GF(2)
    ├── class ButtonPuzzleSolver # Main solver
    ├── solve_puzzle()           # High-level solver function
    └── main()                   # Updated to use solver
```

## Class: GF2Matrix

### Purpose
Handle matrix operations in the binary field GF(2) where addition is XOR.

### Attributes
```python
data: list[list[int]]  # 2D matrix of 0s and 1s
rows: int              # Number of rows
cols: int              # Number of columns
```

### Methods

#### `__init__(self, rows: int, cols: int)`
Initialize matrix with zeros.

#### `set(self, row: int, col: int, value: int)`
Set matrix element (value must be 0 or 1).

#### `get(self, row: int, col: int) -> int`
Get matrix element.

#### `swap_rows(self, row1: int, row2: int)`
Swap two rows in the matrix.

#### `add_row(self, target_row: int, source_row: int)`
Add source_row to target_row (XOR operation in GF(2)).

#### `gaussian_elimination(self) -> bool`
Perform Gaussian elimination to row echelon form.
Returns True if system is consistent, False otherwise.

**Algorithm**:
```python
for col in range(min(rows, cols)):
    # Find pivot (first 1 in column)
    pivot_row = find_pivot(col)
    if pivot_row is None:
        continue  # No pivot in this column
    
    # Swap to bring pivot to diagonal
    swap_rows(col, pivot_row)
    
    # Eliminate all other 1s in this column
    for row in range(rows):
        if row != col and get(row, col) == 1:
            add_row(row, col)  # XOR rows
```

#### `back_substitute(self) -> list[int] | None`
Extract solution from row echelon form.
Returns solution vector or None if no solution exists.

#### `copy(self) -> GF2Matrix`
Create a deep copy of the matrix.

## Class: ButtonPuzzleSolver

### Purpose
Solve the button toggle puzzle using linear algebra over GF(2).

### Attributes
```python
target_state: list[int]      # Target state as 0s and 1s
buttons: list[list[int]]     # List of button effects
num_positions: int           # Number of positions
num_buttons: int             # Number of buttons
matrix: GF2Matrix            # Augmented matrix [A|b]
```

### Methods

#### `__init__(self, chars: list[str], button_lists: list[list[int]])`
Initialize solver with parsed puzzle data.

**Steps**:
1. Convert chars to binary (`.` → 0, `#` → 1)
2. Store button effects
3. Calculate dimensions
4. Build augmented matrix

#### `build_matrix(self)`
Construct the augmented matrix [A|b].

**Matrix structure**:
- Rows: one per position (0 to num_positions-1)
- Columns: one per button + 1 for target state
- A[i][j] = 1 if button j affects position i, else 0
- b[i] = target state at position i

**Example**:
```
Position 0: [0, 0, 0, 0, 1, 1 | 0]  # Buttons 4,5 affect pos 0
Position 1: [0, 1, 0, 0, 0, 1 | 1]  # Buttons 1,5 affect pos 1
Position 2: [0, 0, 1, 1, 1, 0 | 1]  # Buttons 2,3,4 affect pos 2
Position 3: [1, 1, 0, 1, 0, 0 | 0]  # Buttons 0,1,3 affect pos 3
```

#### `solve(self) -> tuple[int, list[int]] | None`
Solve the puzzle and return (min_presses, button_indices).

**Algorithm**:
```python
1. Create copy of matrix for manipulation
2. Perform Gaussian elimination
3. Check if solution exists
4. Extract solution vector
5. Handle free variables (if any)
6. Count number of 1s in solution
7. Return (count, indices of pressed buttons)
```

#### `verify_solution(self, solution: list[int]) -> bool`
Verify that a solution produces the target state.

**Steps**:
1. Start with all 0s
2. For each button in solution, toggle its positions
3. Compare final state with target
4. Return True if match, False otherwise

#### `find_minimum_solution(self, solutions: list[list[int]]) -> list[int]`
Given multiple solutions, return the one with minimum button presses.

## Function: solve_puzzle

### Signature
```python
def solve_puzzle(chars: list[str], button_lists: list[list[int]]) -> dict
```

### Purpose
High-level function to solve a single puzzle instance.

### Returns
```python
{
    'target': list[str],           # Original target state
    'min_presses': int,            # Minimum button presses
    'buttons_pressed': list[int],  # Indices of buttons to press
    'solution_exists': bool,       # Whether solution was found
    'verification': bool           # Whether solution was verified
}
```

### Algorithm
```python
1. Create ButtonPuzzleSolver instance
2. Call solve()
3. If solution found:
   - Verify solution
   - Package results
4. Else:
   - Return no solution found
```

## Updated main() Function

### Purpose
Integrate solver with existing parsing code.

### Implementation
```python
def main():
    # Parse input
    parsed_data = parse_input(sample)
    
    # Solve each puzzle
    for i, (chars, button_lists, final_numbers) in enumerate(parsed_data, 1):
        print(f"\n{'='*60}")
        print(f"Puzzle {i}")
        print(f"{'='*60}")
        print(f"Target state: {''.join(chars)}")
        print(f"Number of buttons: {len(button_lists)}")
        
        # Solve
        result = solve_puzzle(chars, button_lists)
        
        # Display results
        if result['solution_exists']:
            print(f"\n✓ Solution found!")
            print(f"  Minimum presses: {result['min_presses']}")
            print(f"  Buttons to press: {result['buttons_pressed']}")
            print(f"  Verification: {'PASS' if result['verification'] else 'FAIL'}")
        else:
            print(f"\n✗ No solution exists for this puzzle")
        
        # Compare with expected (if provided)
        if final_numbers:
            print(f"\n  Expected values: {final_numbers}")
```

## Error Handling

### Cases to Handle

1. **Invalid input**
   - Empty target state
   - Empty button list
   - Invalid characters (not `.` or `#`)

2. **No solution exists**
   - System is inconsistent
   - Target state unreachable

3. **Multiple solutions**
   - Free variables in system
   - Choose solution with minimum presses

4. **Edge cases**
   - All dots target (trivial: 0 presses)
   - All hashes target
   - Single position
   - Single button

## Testing Strategy

### Unit Tests

1. **GF2Matrix tests**
   - Matrix creation
   - Row operations
   - Gaussian elimination
   - Back substitution

2. **ButtonPuzzleSolver tests**
   - Matrix building
   - Solution extraction
   - Verification

### Integration Tests

1. **Sample data tests**
   - Test all three sample puzzles
   - Verify minimum presses
   - Verify solution correctness

2. **Edge case tests**
   - No solution case
   - Trivial solution (all dots)
   - Single button/position

### Test Data

```python
# Test 1: Simple case
target = ['.', '#', '#', '.']
buttons = [[3], [1,3], [2], [2,3], [0,2], [0,1]]
expected_min = 3

# Test 2: No solution
target = ['.', '#']
buttons = [[0], [0]]  # Both buttons affect same position
expected_min = None

# Test 3: Trivial
target = ['.', '.', '.']
buttons = [[0], [1], [2]]
expected_min = 0
```

## Performance Considerations

### Time Complexity
- Matrix building: O(n × b) where n=positions, b=buttons
- Gaussian elimination: O(n³)
- Overall: O(n³) dominated by elimination

### Space Complexity
- Matrix storage: O(n × b)
- Overall: O(n × b)

### Optimization Opportunities
1. Sparse matrix representation (if many zeros)
2. Early termination in elimination
3. Caching for repeated puzzles
4. Parallel processing for multiple puzzles

## Code Style Guidelines

1. Use type hints for all functions
2. Add docstrings with examples
3. Follow PEP 8 conventions
4. Use descriptive variable names
5. Add comments for complex logic
6. Keep functions focused and small