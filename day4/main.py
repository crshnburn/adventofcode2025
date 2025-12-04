


def read_input():
    """Reads input.txt and returns the contents as a matrix of characters."""
    with open('input.txt', 'r') as f:
        return [list(line.strip()) for line in f]


def count_at_symbols_with_few_neighbors(matrix):
    """
    Counts how many '@' symbols have less than 4 neighbors in the 8 ordinal directions.
    
    Args:
        matrix: A 2D list of characters
        
    Returns:
        int: Count of '@' symbols with less than 4 neighbors
    """
    if not matrix or not matrix[0]:
        return 0
    
    rows = len(matrix)
    cols = len(matrix[0])
    count = 0
    
    # 8 ordinal directions: N, NE, E, SE, S, SW, W, NW
    directions = [
        (-1, 0),   # North
        (-1, 1),   # North-East
        (0, 1),    # East
        (1, 1),    # South-East
        (1, 0),    # South
        (1, -1),   # South-West
        (0, -1),   # West
        (-1, -1)   # North-West
    ]
    
    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] == '@':
                # Count valid neighbors
                neighbor_count = 0
                for di, dj in directions:
                    ni, nj = i + di, j + dj
                    # Check if neighbor position is within bounds
                    if 0 <= ni < rows and 0 <= nj < cols and matrix[ni][nj] == '@':
                        neighbor_count += 1
                
                # If less than 4 neighbors, increment count
                if neighbor_count < 4:
                    count += 1
    
    return count

def count_at_symbols_with_few_neighbors_multiple(matrix):
    """
    Counts how many '@' symbols have less than 4 neighbors in the 8 ordinal directions.
    
    Args:
        matrix: A 2D list of characters
        
    Returns:
        int: Count of '@' symbols with less than 4 neighbors
    """
    # Create a copy of matrix
    matrix = [row[:] for row in matrix]
    updated = True
    if not matrix or not matrix[0]:
        return 0
    
    rows = len(matrix)
    cols = len(matrix[0])
    count = 0
    
    # 8 ordinal directions: N, NE, E, SE, S, SW, W, NW
    directions = [
        (-1, 0),   # North
        (-1, 1),   # North-East
        (0, 1),    # East
        (1, 1),    # South-East
        (1, 0),    # South
        (1, -1),   # South-West
        (0, -1),   # West
        (-1, -1)   # North-West
    ]
    
    while updated:
        new_matrix = [row[:] for row in matrix]
        updated = False
        for i in range(rows):
            for j in range(cols):
                if matrix[i][j] == '@':
                    # Count valid neighbors
                    neighbor_count = 0
                    for di, dj in directions:
                        ni, nj = i + di, j + dj
                        # Check if neighbor position is within bounds
                        if 0 <= ni < rows and 0 <= nj < cols and matrix[ni][nj] == '@':
                            neighbor_count += 1
                    
                    # If less than 4 neighbors, increment count
                    if neighbor_count < 4:
                        new_matrix[i][j] = 'x'
                        updated = True
                        count += 1
        matrix = new_matrix
    
    return count


def main():
    matrix = read_input()
    print("Hello from day4!")
    print(f"Matrix dimensions: {len(matrix)} rows x {len(matrix[0]) if matrix else 0} columns")
    print(count_at_symbols_with_few_neighbors(matrix))
    print(count_at_symbols_with_few_neighbors_multiple(matrix))


if __name__ == "__main__":
    main()
