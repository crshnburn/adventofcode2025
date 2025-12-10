# Button Toggle Puzzle - Solution Plan

## Problem Statement

Given:
- A target state: list of characters `['.', '#', '#', '.']`
- A set of buttons: each button toggles specific positions (e.g., button 1 toggles positions `[1, 3]`)
- Initial state: all positions are `'.'`

Goal: Find the **minimum number of button presses** to transform the initial state to the target state.

## Key Insights

### 1. Toggle Property
- Pressing a button twice returns to the original state (toggle is its own inverse)
- Therefore, each button needs to be pressed either 0 or 1 times
- Order of button presses doesn't matter (commutative operations)

### 2. Mathematical Formulation
This is a **system of linear equations over GF(2)** (binary field):
- Each position has a target state: 0 (dot) or 1 (hash)
- Each button press contributes to certain positions
- We need to find which buttons to press (0 or 1) to reach the target

### 3. Example Walkthrough

For `[.##.]` with buttons `(3) (1,3) (2) (2,3) (0,2) (0,1)`:

```
Target: [., #, #, .]  →  [0, 1, 1, 0]
Start:  [., ., ., .]  →  [0, 0, 0, 0]

Buttons:
- Button 0: toggles position 3
- Button 1: toggles positions 1, 3
- Button 2: toggles position 2
- Button 3: toggles positions 2, 3
- Button 4: toggles positions 0, 2
- Button 5: toggles positions 0, 1

Matrix representation (rows = positions, cols = buttons):
Position | B0 | B1 | B2 | B3 | B4 | B5 | Target
---------|----|----|----|----|----|----|-------
    0    | 0  | 0  | 0  | 0  | 1  | 1  |   0
    1    | 0  | 1  | 0  | 0  | 0  | 1  |   1
    2    | 0  | 0  | 1  | 1  | 1  | 0  |   1
    3    | 1  | 1  | 0  | 1  | 0  | 0  |   0
```

We need to solve: `A × x = b` (mod 2)
- A = button effect matrix
- x = which buttons to press (0 or 1)
- b = target state

## Solution Approaches

### Approach 1: Gaussian Elimination over GF(2) ✓ (Recommended)
**Complexity**: O(n³) where n is the number of positions

**Algorithm**:
1. Build the augmented matrix [A | b]
2. Perform Gaussian elimination in GF(2) (XOR operations)
3. Back-substitute to find solution
4. Count the number of 1s in the solution vector

**Advantages**:
- Deterministic and efficient
- Finds optimal solution if one exists
- Can detect if no solution exists

**Implementation steps**:
- Create matrix representation
- Implement row reduction over GF(2)
- Handle free variables (multiple solutions)
- Choose solution with minimum button presses

### Approach 2: BFS/Dynamic Programming
**Complexity**: O(2^b) where b is the number of buttons

**Algorithm**:
1. Use BFS to explore all possible button press combinations
2. Track visited states to avoid cycles
3. Return the first solution found (minimum presses)

**Advantages**:
- Conceptually simpler
- Guaranteed to find minimum if solution exists

**Disadvantages**:
- Exponential time complexity
- Only practical for small number of buttons (<20)

### Approach 3: Greedy Heuristic (Not Optimal)
**Not recommended** - greedy approaches don't guarantee optimal solution for this problem

## Implementation Plan

### Phase 1: Core Algorithm
1. Implement matrix representation builder
2. Implement Gaussian elimination over GF(2)
3. Implement solution extraction and counting

### Phase 2: Integration
1. Integrate with existing parsing code in [`main.py`](main.py:8-50)
2. Add solver function that takes parsed input
3. Return minimum button presses

### Phase 3: Testing & Validation
1. Test with sample data
2. Verify results
3. Add edge case handling (no solution, multiple solutions)

### Phase 4: Optimization (if needed)
1. Profile performance
2. Optimize matrix operations
3. Add caching if beneficial

## Expected Output Format

For each puzzle line:
```
Line 1: [.##.]
  Buttons: [(3), (1,3), (2), (2,3), (0,2), (0,1)]
  Minimum presses: 3
  Solution: Press buttons [1, 2, 4]
```

## Edge Cases to Handle

1. **No solution exists**: Some target states may be unreachable
2. **Multiple solutions**: Choose one with minimum presses
3. **Empty buttons**: Button with no positions to toggle
4. **All dots or all hashes**: Trivial cases

## Mathematical Background

### GF(2) Operations
- Addition: XOR (0+0=0, 0+1=1, 1+0=1, 1+1=0)
- Multiplication: AND (0×0=0, 0×1=0, 1×0=0, 1×1=1)
- No subtraction needed (a-b = a+b in GF(2))

### Why This Works
- Toggle operations form a vector space over GF(2)
- Each button press is a basis vector
- Target state is a linear combination of button presses
- Gaussian elimination finds the coefficients (0 or 1)