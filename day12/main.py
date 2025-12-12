sample = """0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
"""

def parse_input(text):
    """Parse the input to extract shapes and grid requirements."""
    lines = text.strip().split('\n')
    shapes = {}
    grid_requirements = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Check if this is a shape definition
        if line and ':' in line and not 'x' in line:
            shape_id = int(line.rstrip(':'))
            shape_lines = []
            i += 1
            
            # Read shape grid
            while i < len(lines) and lines[i].strip() and ':' not in lines[i]:
                shape_lines.append(lines[i])
                i += 1
            
            shapes[shape_id] = parse_shape(shape_lines)
        
        # Check if this is a grid requirement
        elif 'x' in line:
            parts = line.split(':')
            dims = parts[0].strip().split('x')
            width, height = int(dims[0]), int(dims[1])
            counts = list(map(int, parts[1].strip().split()))
            grid_requirements.append((width, height, counts))
            i += 1
        else:
            i += 1
    
    return shapes, grid_requirements


def parse_shape(lines):
    """Convert shape text representation to list of (row, col) coordinates."""
    coords = []
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char == '#':
                coords.append((r, c))
    return coords


def normalize_shape(shape):
    """Normalize shape coordinates to start from (0, 0)."""
    if not shape:
        return []
    min_r = min(r for r, c in shape)
    min_c = min(c for r, c in shape)
    return sorted([(r - min_r, c - min_c) for r, c in shape])


def rotate_90(shape):
    """Rotate shape 90 degrees clockwise."""
    # (r, c) -> (c, -r)
    rotated = [(c, -r) for r, c in shape]
    return normalize_shape(rotated)


def flip_horizontal(shape):
    """Flip shape horizontally."""
    flipped = [(r, -c) for r, c in shape]
    return normalize_shape(flipped)


def flip_vertical(shape):
    """Flip shape vertically."""
    flipped = [(-r, c) for r, c in shape]
    return normalize_shape(flipped)


def get_all_orientations(shape):
    """Generate all unique orientations of a shape."""
    orientations = set()
    current = normalize_shape(shape)
    
    # Try all rotations
    for _ in range(4):
        orientations.add(tuple(current))
        current = rotate_90(current)
    
    # Try flipped versions
    flipped_h = flip_horizontal(shape)
    for _ in range(4):
        orientations.add(tuple(flipped_h))
        flipped_h = rotate_90(flipped_h)
    
    flipped_v = flip_vertical(shape)
    for _ in range(4):
        orientations.add(tuple(flipped_v))
        flipped_v = rotate_90(flipped_v)
    
    # Convert back to lists
    return [list(orient) for orient in orientations]


def can_place_shape(grid, shape, row, col, width, height):
    """Check if shape can be placed at (row, col) without overlap or going out of bounds."""
    for dr, dc in shape:
        r, c = row + dr, col + dc
        if r < 0 or r >= height or c < 0 or c >= width:
            return False
        if (r, c) in grid:
            return False
    return True


def place_shape(grid, shape, row, col):
    """Place shape on grid at (row, col)."""
    for dr, dc in shape:
        grid.add((row + dr, col + dc))


def remove_shape(grid, shape, row, col):
    """Remove shape from grid at (row, col)."""
    for dr, dc in shape:
        grid.discard((row + dr, col + dc))


def get_shape_bounds(shape):
    """Get the bounding box dimensions of a shape."""
    if not shape:
        return 0, 0
    max_r = max(r for r, c in shape)
    max_c = max(c for r, c in shape)
    return max_r + 1, max_c + 1


def get_valid_positions(shape, width, height):
    """Pre-compute all valid positions where a shape can be placed."""
    shape_height, shape_width = get_shape_bounds(shape)
    positions = []
    
    for row in range(height - shape_height + 1):
        for col in range(width - shape_width + 1):
            positions.append((row, col))
    
    return positions


def solve_backtrack(grid, shapes_to_place, shape_library, valid_positions, width, height, index=0):
    """
    Optimized backtracking algorithm to place all required shapes on the grid.
    
    Args:
        grid: Set of occupied (row, col) positions
        shapes_to_place: List of shape_ids to place (sorted by size)
        shape_library: Dict mapping shape_id to list of orientations
        valid_positions: Dict mapping (shape_id, orientation_idx) to valid positions
        width, height: Grid dimensions
        index: Current index in shapes_to_place
    
    Returns:
        True if all shapes can be placed, False otherwise
    """
    # Base case: all shapes placed successfully
    if index >= len(shapes_to_place):
        return True
    
    shape_id = shapes_to_place[index]
    
    # Early termination: check if remaining area is sufficient
    remaining_cells = width * height - len(grid)
    remaining_shape_cells = sum(len(shape_library[sid][0]) for sid in shapes_to_place[index:])
    if remaining_cells < remaining_shape_cells:
        return False
    
    # Try each orientation of this shape
    for orient_idx, orientation in enumerate(shape_library[shape_id]):
        # Use pre-computed valid positions for this shape orientation
        key = (shape_id, orient_idx)
        if key not in valid_positions:
            continue
            
        for row, col in valid_positions[key]:
            if can_place_shape(grid, orientation, row, col, width, height):
                # Place the shape
                place_shape(grid, orientation, row, col)
                
                # Recursively try to place remaining shapes
                if solve_backtrack(grid, shapes_to_place, shape_library, valid_positions, width, height, index + 1):
                    return True
                
                # Backtrack: remove the shape
                remove_shape(grid, orientation, row, col)
    
    return False


def can_fit_shapes(width, height, shape_counts, shapes):
    """Check if all required shapes can fit in the grid."""
    # Build list of shapes to place
    shapes_to_place = []
    for shape_id, count in enumerate(shape_counts):
        shapes_to_place.extend([shape_id] * count)
    
    if not shapes_to_place:
        return True
    
    # Early check: total area constraint
    total_area = width * height
    required_area = sum(len(shapes[shape_id]) for shape_id in shapes_to_place)
    if required_area > total_area:
        return False
    
    # Pre-compute all orientations for each shape
    shape_library = {}
    for shape_id in set(shapes_to_place):
        shape_library[shape_id] = get_all_orientations(shapes[shape_id])
    
    # Sort shapes by size (largest first) for better pruning
    shapes_to_place.sort(key=lambda sid: len(shapes[sid]), reverse=True)
    
    # Pre-compute valid positions for each shape orientation
    valid_positions = {}
    for shape_id in set(shapes_to_place):
        for orient_idx, orientation in enumerate(shape_library[shape_id]):
            key = (shape_id, orient_idx)
            valid_positions[key] = get_valid_positions(orientation, width, height)
    
    # Try to place all shapes using backtracking
    grid = set()
    return solve_backtrack(grid, shapes_to_place, shape_library, valid_positions, width, height)


def solve(text):
    """Solve the puzzle and return the count of grids that can fit all required shapes."""
    shapes, grid_requirements = parse_input(text)
    
    count = 0
    for width, height, shape_counts in grid_requirements:
        if can_fit_shapes(width, height, shape_counts, shapes):
            count += 1
    
    return count


def main():
    with open('input.txt', 'r') as f:
        input_text = f.read()
    result = solve(input_text)
    print(f"Number of grids that can fit all required shapes: {result}")


if __name__ == "__main__":
    main()

# Made with Bob
