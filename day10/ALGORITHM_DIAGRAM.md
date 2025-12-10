# Algorithm Visualization

## Problem Flow

```mermaid
graph TD
    A[Input: Target State and Buttons] --> B[Parse Input]
    B --> C[Build Matrix Representation]
    C --> D[Create Augmented Matrix A|b]
    D --> E[Gaussian Elimination over GF2]
    E --> F{Solution Exists?}
    F -->|Yes| G[Extract Solution Vector]
    F -->|No| H[Return: No Solution]
    G --> I[Count Button Presses]
    I --> J[Return Minimum Presses]
```

## Matrix Construction Example

For target `[.##.]` with 4 positions and 6 buttons:

```mermaid
graph LR
    subgraph Input
        T[Target: 0,1,1,0]
        B0[Button 0: toggles 3]
        B1[Button 1: toggles 1,3]
        B2[Button 2: toggles 2]
        B3[Button 3: toggles 2,3]
        B4[Button 4: toggles 0,2]
        B5[Button 5: toggles 0,1]
    end
    
    subgraph Matrix
        M[Matrix A: 4x6<br/>Each row = position<br/>Each col = button<br/>Value = 1 if button affects position]
    end
    
    Input --> Matrix
```

## Gaussian Elimination Process

```mermaid
graph TD
    A[Start: Augmented Matrix] --> B[Forward Elimination]
    B --> C[Create Row Echelon Form]
    C --> D[Back Substitution]
    D --> E{Free Variables?}
    E -->|Yes| F[Try All Combinations]
    E -->|No| G[Unique Solution]
    F --> H[Select Minimum Presses]
    G --> I[Count Presses]
    H --> I
    I --> J[Return Result]
```

## State Space Example

Starting state: `[....]` (all dots)
Target state: `[.##.]`

```mermaid
graph TD
    S0["[....] <br/> 0 presses"] --> S1["Press B1<br/>[.#.#]<br/>1 press"]
    S0 --> S2["Press B2<br/>[..#.]<br/>1 press"]
    S1 --> S3["Press B2<br/>[.###]<br/>2 presses"]
    S2 --> S4["Press B1<br/>[.###]<br/>2 presses"]
    S3 --> S5["Press B4<br/>[.##.]<br/>3 presses ✓"]
    
    style S5 fill:#90EE90
```

## Algorithm Complexity Analysis

```mermaid
graph LR
    subgraph Approach 1: Gaussian Elimination
        A1[Time: O n³]
        A2[Space: O n²]
        A3[Optimal: Yes]
    end
    
    subgraph Approach 2: BFS
        B1[Time: O 2^b]
        B2[Space: O 2^b]
        B3[Optimal: Yes]
    end
    
    subgraph Comparison
        C1[n = positions<br/>b = buttons]
        C2[GE better when b > 10]
        C3[BFS simpler for small b]
    end
```

## Solution Verification Flow

```mermaid
graph TD
    A[Solution Vector x] --> B[Apply Button Presses]
    B --> C[Simulate Toggles]
    C --> D[Compare with Target]
    D --> E{Match?}
    E -->|Yes| F[Valid Solution ✓]
    E -->|No| G[Invalid Solution ✗]
    F --> H[Count Total Presses]
    G --> I[Debug/Retry]
```

## Data Structure Design

```mermaid
classDiagram
    class PuzzleInput {
        +list~char~ target_state
        +list~list~int~~ buttons
        +int num_positions
        +int num_buttons
    }
    
    class Matrix {
        +list~list~int~~ data
        +int rows
        +int cols
        +swap_rows()
        +add_rows()
        +get_pivot()
    }
    
    class Solver {
        +PuzzleInput puzzle
        +Matrix matrix
        +build_matrix()
        +gaussian_elimination()
        +extract_solution()
        +count_presses()
    }
    
    class Solution {
        +list~int~ buttons_to_press
        +int total_presses
        +bool is_valid
        +verify()
    }
    
    PuzzleInput --> Solver
    Solver --> Matrix
    Solver --> Solution