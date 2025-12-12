# Shape Fitting Puzzle Visualizer

An animated graphical visualization of the backtracking algorithm used to solve the shape fitting puzzle.

## Overview

This visualization shows how the backtracking algorithm attempts to place polyomino shapes onto a grid. It provides real-time feedback on:
- Valid and invalid placement attempts
- Successful placements
- Backtracking when no solution is found
- Step-by-step progress through the algorithm

## Features

### Visual Elements

1. **Grid Display**: Shows the target grid with cells outlined
2. **Shape Colors**: Each shape type has a unique color for easy identification
3. **Placement Feedback**:
   - **Green (semi-transparent)**: Valid placement being tested
   - **Red (semi-transparent)**: Invalid placement (collision or out of bounds)
   - **Solid colors**: Successfully placed shapes
4. **Information Panel**: Shows:
   - Grid dimensions
   - Step count
   - Backtrack count
   - Number of shapes placed
   - Shape counts by type
   - Current algorithm status

### Text Explanations

The visualization provides real-time text updates explaining what's happening:
- "Starting with N shapes to place"
- "Trying to place shape X at (row, col) - Valid/Invalid"
- "Placed shape X at (row, col). Continuing..."
- "Backtracking: removing shape X from (row, col)"
- "SUCCESS! All shapes placed!" or "No solution found."

## Running the Visualization

### Basic Usage

```bash
uv run visualizer.py
```

This will run the visualization with the sample data from `main.py`.

### Interactive Controls

- **SPACE**: Pause/Resume the animation
- **UP Arrow**: Speed up the animation
- **DOWN Arrow**: Slow down the animation
- **Any key** (at completion): Close the window

## How It Works

### Algorithm Visualization

The visualizer shows the backtracking algorithm in action:

1. **Initialization**: Displays the empty grid and lists shapes to place
2. **Shape Selection**: Highlights which shape is being placed next
3. **Orientation Testing**: Shows different rotations/flips of each shape
4. **Position Testing**: Tries each valid position on the grid
5. **Placement**: When valid, places the shape and moves to the next
6. **Backtracking**: When stuck, removes the last placed shape and tries alternatives
7. **Completion**: Shows success or failure message

### Color Coding

- **Shape 0**: Red
- **Shape 1**: Green
- **Shape 2**: Blue
- **Shape 3**: Yellow
- **Shape 4**: Orange
- **Shape 5**: Purple

### Performance Notes

- The visualization slows down the algorithm to make it observable
- Default speed: 0.3 seconds per step
- Adjust speed with UP/DOWN arrows for faster/slower visualization
- For large grids, consider increasing the speed to avoid long wait times

## Code Structure

### Main Classes

**`ShapeFittingVisualizer`**: Main visualization class
- Manages pygame window and rendering
- Tracks algorithm state
- Handles user input
- Draws grid, shapes, and information panel

### Key Functions

- `draw_grid()`: Renders the grid background
- `draw_shape()`: Draws a shape with specified color and transparency
- `draw_placed_shapes()`: Shows all successfully placed shapes
- `draw_current_attempt()`: Highlights the current placement attempt
- `draw_info_panel()`: Displays statistics and status
- `update_state()`: Updates visualization state and redraws
- `show_completion()`: Displays final result

### Algorithm Integration

The `solve_with_visualization()` function integrates the backtracking algorithm with the visualizer:
- Calls `update_state()` at each step
- Shows placement attempts (valid and invalid)
- Displays backtracking operations
- Reports final success/failure

## Customization

### Adjusting Cell Size

Change the `cell_size` parameter when creating the visualizer:

```python
visualizer = ShapeFittingVisualizer(width, height, shapes, shape_counts, cell_size=50)
```

Larger values make the grid bigger but may not fit on screen for large grids.

### Changing Animation Speed

Modify the `animation_speed` attribute (in seconds):

```python
visualizer.animation_speed = 0.1  # Faster
visualizer.animation_speed = 1.0  # Slower
```

### Using Different Test Cases

To visualize different grid configurations, modify the example usage in `visualizer.py`:

```python
# Use a different grid requirement
width, height, shape_counts = grid_requirements[1]  # Second grid
```

## Example Output

When running the visualizer, you'll see:
1. A window opens showing the grid
2. Shapes appear as the algorithm tries to place them
3. Green overlays show valid attempts
4. Red overlays show invalid attempts
5. Successfully placed shapes remain on the grid
6. The info panel updates with each step
7. A completion message appears when done

## Dependencies

- **pygame**: For graphics and animation
- **Python 3.12+**: Required by the project

Install dependencies with:
```bash
uv sync
```

## Tips for Understanding the Algorithm

1. **Watch the backtracking**: Notice how the algorithm removes shapes when it gets stuck
2. **Observe shape orientations**: See how shapes are rotated and flipped
3. **Count the attempts**: The step counter shows how many placements were tried
4. **Pause to examine**: Use SPACE to pause and study the current state
5. **Speed control**: Slow down for complex parts, speed up for repetitive sections

## Troubleshooting

**Window doesn't appear**: Make sure pygame is installed (`uv sync`)

**Animation too fast/slow**: Use UP/DOWN arrows to adjust speed

**Window closes immediately**: Check for errors in the terminal output

**Out of memory**: Large grids with many shapes may require significant memory