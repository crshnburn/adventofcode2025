# Button Toggle Puzzle Solver

## Problem Description

This project solves a button toggle puzzle where:
- You start with all positions as `.` (dots)
- You have a target state with some positions as `#` (hashes)
- You have buttons that toggle specific positions between `.` and `#`
- Goal: Find the **minimum number of button presses** to reach the target state

## Example

```
Target: [.##.]
Buttons: (3) (1,3) (2) (2,3) (0,2) (0,1)

Starting state: [....] (all dots)
Target state:   [.##.] (hashes at positions 1 and 2)

Solution: Press buttons 1, 2, and 4 (3 total presses)
```

## Mathematical Approach

This puzzle is solved using **Gaussian elimination over GF(2)** (the binary field):

1. Each button press toggles specific positions (toggle is its own inverse)
2. Each button needs to be pressed 0 or 1 times (pressing twice = no effect)
3. The problem becomes a system of linear equations in GF(2)
4. We solve: `A × x = b` where:
   - `A` = matrix of button effects
   - `x` = which buttons to press (0 or 1)
   - `b` = target state

## Solution Algorithm

```
1. Parse input (target state and button definitions)
2. Build augmented matrix [A|b]
3. Perform Gaussian elimination over GF(2)
4. Extract solution vector
5. Count button presses (number of 1s in solution)
6. Verify solution correctness
```

## Project Structure

- [`main.py`](main.py) - Main implementation with parsing and solver
- [`PLAN.md`](PLAN.md) - Detailed solution plan and approach
- [`ALGORITHM_DIAGRAM.md`](ALGORITHM_DIAGRAM.md) - Visual diagrams and flowcharts
- [`IMPLEMENTATION_SPEC.md`](IMPLEMENTATION_SPEC.md) - Technical implementation details

## Usage

```bash
python main.py
```

## Input Format

```
[target_state] (button1) (button2) ... {optional_numbers}
```

Example:
```
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
```

Where:
- `[.##.]` - Target state (dots and hashes)
- `(3)` - Button that toggles position 3
- `(1,3)` - Button that toggles positions 1 and 3
- `{3,5,4,7}` - Optional metadata (not used in solving)

## Key Features

- ✓ Optimal solution using Gaussian elimination
- ✓ Handles multiple solutions (chooses minimum presses)
- ✓ Detects when no solution exists
- ✓ Solution verification
- ✓ O(n³) time complexity where n = number of positions

## Algorithm Complexity

- **Time**: O(n³) where n is the number of positions
- **Space**: O(n × b) where b is the number of buttons
- **Optimal**: Yes, guaranteed to find minimum if solution exists

## Implementation Status

- [x] Problem analysis and planning
- [ ] Core GF(2) matrix operations
- [ ] Gaussian elimination solver
- [ ] Solution verification
- [ ] Integration with existing parser
- [ ] Testing with sample data
- [ ] Performance optimization

## References

- Linear algebra over finite fields
- Gaussian elimination in GF(2)
- Toggle switch puzzles (similar to "Lights Out")