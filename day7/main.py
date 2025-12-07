import time


def read_input():
    """Reads input.txt and returns the contents as a 2D matrix of characters."""
    with open('input.txt', 'r') as f:
        lines = f.read().strip().split('\n')
    return [list(line) for line in lines]

def count_carets(matrix):
    """
    Finds the starting point marked by 'S' and moves downwards.
    When encountering a '^', branches left and right from that position.
    Returns the total count of '^' characters encountered.
    """
    if not matrix:
        return 0
    
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0
    
    # Find the starting position 'S'
    start_row, start_col = None, None
    for r in range(rows):
        for c in range(cols):
            if matrix[r][c] == 'S':
                start_row, start_col = r, c
                break
        if start_row is not None:
            break
    
    if start_row is None:
        return 0
    
    # Track positions to explore (row, col)
    positions_to_explore = [(start_row, start_col)]
    visited = set()
    caret_count = 0
    
    while positions_to_explore:
        row, col = positions_to_explore.pop(0)
        
        # Skip if out of bounds or already visited
        if row < 0 or row >= rows or col < 0 or col >= cols:
            continue
        if (row, col) in visited:
            continue
        
        visited.add((row, col))
        
        # Check current position
        if matrix[row][col] == '^':
            caret_count += 1
            # Branch left and right
            if col - 1 >= 0 and (row, col - 1) not in visited:
                positions_to_explore.append((row, col - 1))
            if col + 1 < cols and (row, col + 1) not in visited:
                positions_to_explore.append((row, col + 1))
        else:
            # Move downwards
            if row + 1 < rows and (row + 1, col) not in visited:
                positions_to_explore.append((row + 1, col))
    
    return caret_count

def count_timelines(matrix) -> int:
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0
    
    # Find the starting position 'S'
    start_row, start_col = None, None
    for r in range(rows):
        for c in range(cols):
            if matrix[r][c] == 'S':
                start_row, start_col = r, c
                break
        if start_row is not None:
            break
    
    if start_row is None:
        return 0
    
    timeline_counts = {(start_row, start_col): 1}
    for row in range(rows):
        newtimeline_counts = {}
        for key in timeline_counts:
            val = timeline_counts[key]
            if matrix[row][key[1]] == '^':
                if (row, key[1]-1) in newtimeline_counts:
                    newtimeline_counts[(row, key[1]-1)] += val
                else:
                    newtimeline_counts[(row, key[1]-1)] = val
                if (row, key[1]+1) in newtimeline_counts:
                    newtimeline_counts[(row, key[1]+1)] += val
                else:
                    newtimeline_counts[(row, key[1]+1)] = val
            else :
                if (row, key[1]) in newtimeline_counts :
                    newtimeline_counts[(row, key[1])] += val
                else:
                    newtimeline_counts[(row, key[1])] = val
        timeline_counts = newtimeline_counts

    return sum(timeline_counts.values())

def main():
    print("Hello from day7!")
    manifold = read_input()
    # manifold = [list(line) for line in list(sample_input.splitlines())]
    print(manifold)
    result = count_carets(manifold)
    print(f"Number of '^' characters encountered: {result}")
    print(f"Number of timelines: {count_timelines(manifold)}")

sample_input = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
"""

if __name__ == "__main__":
    main()
