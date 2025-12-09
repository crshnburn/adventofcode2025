from collections import deque

sample = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""

def read_input_file():
    """Reads input.txt and returns a list of integer pairs.
    
    Each line in the file should contain a comma-separated pair of integers.
    Returns a list of tuples, where each tuple contains two integers.
    """
    pairs = []
    with open('input.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split(',')
                pair = (int(parts[0]), int(parts[1]))
                pairs.append(pair)
    return pairs

def find_largest_rectangle_area(coordinates):
    """Finds the largest area that can be formed between two coordinates.
    
    Treats any two coordinates as opposite corners of a rectangle and
    returns the maximum area that can be formed.
    
    Args:
        coordinates: A list of tuples, where each tuple contains (x, y) coordinates.
    
    Returns:
        The largest area that can be formed, or 0 if fewer than 2 coordinates.
    """
    if len(coordinates) < 2:
        return 0
    
    max_area = 0
    
    # Check all pairs of coordinates
    for i in range(len(coordinates)):
        for j in range(i + 1, len(coordinates)):
            x1, y1 = coordinates[i]
            x2, y2 = coordinates[j]
            
            # Calculate the area of the rectangle formed by these two points
            width = abs(x2 - x1) + 1
            height = abs(y2 - y1) + 1
            area = width * height
            
            max_area = max(max_area, area)
    
    return max_area

def create_coordinate_pairs(coordinates):
    """Creates pairs of coordinates where each links to the next, and the last links to the first.
    
    Args:
        coordinates: A list of tuples, where each tuple contains (x, y) coordinates.
    
    Returns:
        A list of tuples, where each tuple contains two coordinate tuples forming a pair.
        Returns an empty list if there are fewer than 2 coordinates.
    """
    if len(coordinates) < 2:
        return []
    
    pairs = []
    for i in range(len(coordinates)):
        current = coordinates[i]
        next_coord = coordinates[(i + 1) % len(coordinates)]
        pairs.append((current, next_coord))
    
    return pairs

def get_all_rectangles_by_size(coordinates):
    """Returns all rectangles formed from a list of coordinates, ordered by size.
    
    Each rectangle is formed by treating two coordinates as opposite corners.
    The rectangles are returned in descending order by area.
    
    Args:
        coordinates: A list of tuples, where each tuple contains (x, y) coordinates.
    
    Returns:
        A list of tuples, where each tuple contains:
        - area: The area of the rectangle
        - coord1: The first coordinate (x, y)
        - coord2: The second coordinate (x, y)
        - width: The width of the rectangle
        - height: The height of the rectangle
        
        Returns an empty list if there are fewer than 2 coordinates.
    """
    if len(coordinates) < 2:
        return []
    
    rectangles = []
    
    # Check all pairs of coordinates
    for i in range(len(coordinates)):
        for j in range(i + 1, len(coordinates)):
            x1, y1 = coordinates[i]
            x2, y2 = coordinates[j]
            
            # Calculate the dimensions of the rectangle
            width = abs(x2 - x1) + 1
            height = abs(y2 - y1) + 1
            area = width * height
            
            rectangles.append((area, coordinates[i], coordinates[j], width, height))
    
    # Sort by area in descending order
    rectangles.sort(reverse=True, key=lambda x: x[0])
    
    return rectangles

def get_bounding_area(coordinates):
    """Returns the bounding area that contains all the coordinates.
    
    Calculates the minimum and maximum x and y values from all coordinates,
    then returns the area of the rectangle that would contain all points.
    
    Args:
        coordinates: A list of tuples, where each tuple contains (x, y) coordinates.
    
    Returns:
        The area of the bounding rectangle, or 0 if the list is empty.
    """
    if not coordinates:
        return 0
    
    # Find min and max x and y values
    x_coords = [coord[0] for coord in coordinates]
    y_coords = [coord[1] for coord in coordinates]
    
    min_x = min(x_coords)
    max_x = max(x_coords)
    min_y = min(y_coords)
    max_y = max(y_coords)
    
    return ((min_x, min_y), (max_x, max_y))

def coordinate_compression(coords):
    # Extract and sort unique values
    x_vals = sorted(set(x for x, y in coords))
    y_vals = sorted(set(y for x, y in coords))
    
    # Create compression mappings
    x_compress = {val: idx for idx, val in enumerate(x_vals)}
    y_compress = {val: idx for idx, val in enumerate(y_vals)}
    
    # Apply compression
    compressed = [(x_compress[x], y_compress[y]) for x, y in coords]
    
    return compressed, x_compress, y_compress

def flood_fill_coordinates(boundary_coords, start, grid):
    """Fill area bounded by coordinate set"""
    queue = deque([start])
    visited = {start}
    
    while queue:
        x, y = queue.popleft()
        grid[y][x] = 'X'
        
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            neighbor = (nx, ny)
            
            if (neighbor not in boundary_coords and 
                neighbor not in visited):
                visited.add(neighbor)
                queue.append(neighbor)

def is_rectangle_in_area(rectangle, grid):
    minx = min(rectangle[1][0], rectangle[2][0])
    maxx = max(rectangle[1][0], rectangle[2][0])
    miny = min(rectangle[1][1], rectangle[2][1])
    maxy = max(rectangle[1][1], rectangle[2][1])
    for x in range(minx, maxx + 1):
        for y in range(miny, maxy + 1):
            if grid[y][x] == '.':
                return False
    return True
                

def main():
    print("Hello from day9!")
    pairs = read_input_file()
    sample_pairs = []
    for line in sample.split("\n"):
        if line:
            x1, y1 = map(int, line.split(","))
            sample_pairs.append((x1, y1))
    print(f"Read {len(pairs)} pairs from input.txt")
    print(f"First few pairs: {pairs[:5]}")
    
    largest_area = find_largest_rectangle_area(pairs)
    print(f"Largest rectangle area: {largest_area}")
    rectangles = get_all_rectangles_by_size(pairs)
    compressed_coords, x_map, y_map = coordinate_compression(pairs)
    
    # Create an array of size len(x_map) * len(y_map) and fill with '.'
    grid = [['.' for _ in range(len(x_map))] for _ in range(len(y_map))]
    
    lines_to_draw = create_coordinate_pairs(compressed_coords)
    boundary_coords = []
    for line in lines_to_draw:
        (x1, y1), (x2, y2) = line
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                grid[y][x1] = '#'
                boundary_coords.append((x1, y))
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                grid[y1][x] = '#'
                boundary_coords.append((x, y1))
    
    flood_fill_coordinates(boundary_coords, (2, 119), grid)
    compressed_rectangles = get_all_rectangles_by_size(compressed_coords)
    for rectangle in compressed_rectangles:
        if is_rectangle_in_area(rectangle, grid):
            origx1 = next((k for k, v in x_map.items() if v == rectangle[1][0]))
            origx2 = next(k for k, v in x_map.items() if v == rectangle[2][0])
            origy1 = next((k for k, v in y_map.items() if v == rectangle[1][1]))
            origy2 = next(k for k, v in y_map.items() if v == rectangle[2][1])
            area = (abs(origx2 - origx1) + 1) * (abs(origy2 - origy1) + 1)
            print(f"Largest contained rectangle area: {area}")
            break
        

    # # Print the grid
    # for row in grid:
    #     print(''.join(row))

if __name__ == "__main__":
    main()
