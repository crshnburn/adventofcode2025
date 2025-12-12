import pygame
import sys
from typing import List, Tuple, Set, Dict
import time

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (240, 240, 240)
DARK_GRAY = (100, 100, 100)
GREEN = (100, 200, 100)
RED = (255, 100, 100)
BLUE = (100, 150, 255)
YELLOW = (255, 255, 100)
ORANGE = (255, 165, 0)
PURPLE = (200, 100, 255)
CYAN = (100, 255, 255)

# Shape colors
SHAPE_COLORS = [
    (255, 100, 100),  # Red
    (100, 255, 100),  # Green
    (100, 150, 255),  # Blue
    (255, 255, 100),  # Yellow
    (255, 165, 0),    # Orange
    (200, 100, 255),  # Purple
]


class ShapeFittingVisualizer:
    def __init__(self, width: int, height: int, shapes: Dict, shape_counts: List[int], cell_size: int = 40):
        """Initialize the visualizer."""
        pygame.init()
        
        self.grid_width = width
        self.grid_height = height
        self.shapes = shapes
        self.shape_counts = shape_counts
        self.cell_size = cell_size
        
        # Calculate window size
        self.grid_pixel_width = width * cell_size
        self.grid_pixel_height = height * cell_size
        self.info_panel_width = 400
        self.window_width = self.grid_pixel_width + self.info_panel_width + 60
        self.window_height = max(self.grid_pixel_height + 100, 600)
        
        # Create window
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Shape Fitting Puzzle Solver")
        
        # Fonts
        self.title_font = pygame.font.Font(None, 36)
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)
        
        # Animation state
        self.grid = set()
        self.placed_shapes = []  # List of (shape_id, orientation, row, col)
        self.current_attempt = None  # (shape_id, orientation, row, col, success)
        self.message = "Starting backtracking algorithm..."
        self.step_count = 0
        self.backtrack_count = 0
        self.animation_speed = 0.3  # seconds per step
        
        # Grid offset for centering
        self.grid_offset_x = 30
        self.grid_offset_y = 80
        
    def draw_grid(self):
        """Draw the grid background."""
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                x = self.grid_offset_x + col * self.cell_size
                y = self.grid_offset_y + row * self.cell_size
                pygame.draw.rect(self.screen, GRAY, (x, y, self.cell_size, self.cell_size), 1)
    
    def draw_shape(self, shape: List[Tuple[int, int]], row: int, col: int, color: Tuple[int, int, int], alpha: int = 255):
        """Draw a shape at the given position."""
        for dr, dc in shape:
            r, c = row + dr, col + dc
            if 0 <= r < self.grid_height and 0 <= c < self.grid_width:
                x = self.grid_offset_x + c * self.cell_size
                y = self.grid_offset_y + r * self.cell_size
                
                # Create surface with alpha
                surf = pygame.Surface((self.cell_size - 2, self.cell_size - 2))
                surf.set_alpha(alpha)
                surf.fill(color)
                self.screen.blit(surf, (x + 1, y + 1))
                
                # Draw border
                pygame.draw.rect(self.screen, DARK_GRAY, (x, y, self.cell_size, self.cell_size), 2)
    
    def draw_placed_shapes(self):
        """Draw all successfully placed shapes."""
        for shape_id, orientation, row, col in self.placed_shapes:
            color = SHAPE_COLORS[shape_id % len(SHAPE_COLORS)]
            self.draw_shape(orientation, row, col, color, 255)
    
    def draw_current_attempt(self):
        """Draw the current shape being attempted."""
        if self.current_attempt:
            shape_id, orientation, row, col, success = self.current_attempt
            if success:
                color = GREEN
                alpha = 180
            else:
                color = RED
                alpha = 120
            self.draw_shape(orientation, row, col, color, alpha)
    
    def draw_info_panel(self):
        """Draw the information panel."""
        panel_x = self.grid_offset_x + self.grid_pixel_width + 30
        panel_y = 80
        
        # Title
        title = self.title_font.render("Solver Status", True, BLACK)
        self.screen.blit(title, (panel_x, 20))
        
        # Stats
        stats = [
            f"Grid: {self.grid_width}x{self.grid_height}",
            f"Steps: {self.step_count}",
            f"Backtracks: {self.backtrack_count}",
            f"Placed: {len(self.placed_shapes)}",
            "",
            "Shape Counts:",
        ]
        
        y = panel_y
        for stat in stats:
            text = self.font.render(stat, True, BLACK)
            self.screen.blit(text, (panel_x, y))
            y += 30
        
        # Draw shape counts with colors
        for shape_id, count in enumerate(self.shape_counts):
            if count > 0:
                color = SHAPE_COLORS[shape_id % len(SHAPE_COLORS)]
                # Draw color box
                pygame.draw.rect(self.screen, color, (panel_x, y, 20, 20))
                pygame.draw.rect(self.screen, BLACK, (panel_x, y, 20, 20), 1)
                # Draw text
                text = self.small_font.render(f"Shape {shape_id}: {count}", True, BLACK)
                self.screen.blit(text, (panel_x + 30, y))
                y += 25
        
        # Current message
        y += 20
        msg_lines = self.wrap_text(self.message, 45)
        for line in msg_lines:
            text = self.small_font.render(line, True, BLUE)
            self.screen.blit(text, (panel_x, y))
            y += 25
        
        # Legend
        y += 20
        legend_items = [
            ("Green: Valid placement", GREEN),
            ("Red: Invalid placement", RED),
        ]
        for label, color in legend_items:
            pygame.draw.rect(self.screen, color, (panel_x, y, 15, 15))
            pygame.draw.rect(self.screen, BLACK, (panel_x, y, 15, 15), 1)
            text = self.small_font.render(label, True, BLACK)
            self.screen.blit(text, (panel_x + 20, y - 2))
            y += 25
    
    def wrap_text(self, text: str, max_chars: int) -> List[str]:
        """Wrap text to fit within max_chars."""
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 <= max_chars:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def draw(self):
        """Draw the entire visualization."""
        self.screen.fill(WHITE)
        
        # Draw title
        title = self.title_font.render("Shape Fitting Puzzle Solver", True, BLACK)
        self.screen.blit(title, (self.grid_offset_x, 20))
        
        # Draw grid and shapes
        self.draw_grid()
        self.draw_placed_shapes()
        self.draw_current_attempt()
        
        # Draw info panel
        self.draw_info_panel()
        
        pygame.display.flip()
    
    def update_state(self, grid: Set, placed_shapes: List, current_attempt: Tuple, message: str, is_backtrack: bool = False):
        """Update the visualization state."""
        self.grid = grid.copy()
        self.placed_shapes = placed_shapes.copy()
        self.current_attempt = current_attempt
        self.message = message
        self.step_count += 1
        if is_backtrack:
            self.backtrack_count += 1
        
        self.draw()
        pygame.time.wait(int(self.animation_speed * 1000))
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Pause
                    paused = True
                    while paused:
                        for e in pygame.event.get():
                            if e.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            elif e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                                paused = False
                elif event.key == pygame.K_UP:
                    self.animation_speed = max(0.05, self.animation_speed - 0.05)
                elif event.key == pygame.K_DOWN:
                    self.animation_speed = min(2.0, self.animation_speed + 0.05)
    
    def show_completion(self, success: bool):
        """Show completion message."""
        if success:
            self.message = "SUCCESS! All shapes placed!"
            color = GREEN
        else:
            self.message = "No solution found."
            color = RED
        
        self.current_attempt = None
        self.draw()
        
        # Draw completion overlay
        overlay = pygame.Surface((self.window_width, 100))
        overlay.set_alpha(200)
        overlay.fill(WHITE)
        self.screen.blit(overlay, (0, self.window_height // 2 - 50))
        
        text = self.title_font.render(self.message, True, color)
        text_rect = text.get_rect(center=(self.window_width // 2, self.window_height // 2))
        self.screen.blit(text, text_rect)
        
        instruction = self.font.render("Press any key to close", True, BLACK)
        inst_rect = instruction.get_rect(center=(self.window_width // 2, self.window_height // 2 + 40))
        self.screen.blit(instruction, inst_rect)
        
        pygame.display.flip()
        
        # Wait for key press
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    waiting = False
        
        pygame.quit()


def normalize_shape(shape):
    """Normalize shape coordinates to start from (0, 0)."""
    if not shape:
        return []
    min_r = min(r for r, c in shape)
    min_c = min(c for r, c in shape)
    return sorted([(r - min_r, c - min_c) for r, c in shape])


def rotate_90(shape):
    """Rotate shape 90 degrees clockwise."""
    rotated = [(c, -r) for r, c in shape]
    return normalize_shape(rotated)


def get_all_orientations(shape):
    """Generate all unique orientations of a shape."""
    orientations = set()
    current = normalize_shape(shape)
    
    for _ in range(4):
        orientations.add(tuple(current))
        current = rotate_90(current)
    
    # Try flipped versions
    flipped_h = [(r, -c) for r, c in shape]
    flipped_h = normalize_shape(flipped_h)
    for _ in range(4):
        orientations.add(tuple(flipped_h))
        flipped_h = rotate_90(flipped_h)
    
    return [list(orient) for orient in orientations]


def can_place_shape(grid, shape, row, col, width, height):
    """Check if shape can be placed at (row, col)."""
    for dr, dc in shape:
        r, c = row + dr, col + dc
        if r < 0 or r >= height or c < 0 or c >= width:
            return False
        if (r, c) in grid:
            return False
    return True


def place_shape(grid, shape, row, col):
    """Place shape on grid."""
    for dr, dc in shape:
        grid.add((row + dr, col + dc))


def remove_shape(grid, shape, row, col):
    """Remove shape from grid."""
    for dr, dc in shape:
        grid.discard((row + dr, col + dc))


def solve_with_visualization(width, height, shape_counts, shapes, visualizer):
    """Solve with visualization."""
    # Build list of shapes to place
    shapes_to_place = []
    for shape_id, count in enumerate(shape_counts):
        shapes_to_place.extend([shape_id] * count)
    
    if not shapes_to_place:
        visualizer.show_completion(True)
        return True
    
    # Pre-compute orientations
    shape_library = {}
    for shape_id in set(shapes_to_place):
        shape_library[shape_id] = get_all_orientations(shapes[shape_id])
    
    # Sort by size
    shapes_to_place.sort(key=lambda sid: len(shapes[sid]), reverse=True)
    
    visualizer.update_state(set(), [], None, f"Starting with {len(shapes_to_place)} shapes to place", False)
    
    # Solve with backtracking
    grid = set()
    placed_shapes = []
    
    def backtrack(index):
        if index >= len(shapes_to_place):
            return True
        
        shape_id = shapes_to_place[index]
        visualizer.update_state(grid, placed_shapes, None, 
                               f"Trying to place shape {shape_id} ({index + 1}/{len(shapes_to_place)})", False)
        
        for orient_idx, orientation in enumerate(shape_library[shape_id]):
            shape_height = max(r for r, c in orientation) + 1
            shape_width = max(c for r, c in orientation) + 1
            
            for row in range(height - shape_height + 1):
                for col in range(width - shape_width + 1):
                    # Show attempt
                    can_place = can_place_shape(grid, orientation, row, col, width, height)
                    visualizer.update_state(grid, placed_shapes, 
                                          (shape_id, orientation, row, col, can_place),
                                          f"Trying shape {shape_id} at ({row},{col}) - {'Valid' if can_place else 'Invalid'}", False)
                    
                    if can_place:
                        # Place shape
                        place_shape(grid, orientation, row, col)
                        placed_shapes.append((shape_id, orientation, row, col))
                        visualizer.update_state(grid, placed_shapes, None,
                                              f"Placed shape {shape_id} at ({row},{col}). Continuing...", False)
                        
                        # Recurse
                        if backtrack(index + 1):
                            return True
                        
                        # Backtrack
                        visualizer.update_state(grid, placed_shapes, None,
                                              f"Backtracking: removing shape {shape_id} from ({row},{col})", True)
                        remove_shape(grid, orientation, row, col)
                        placed_shapes.pop()
        
        return False
    
    success = backtrack(0)
    visualizer.show_completion(success)
    return success


if __name__ == "__main__":
    # Example usage with sample data
    from main import parse_input, sample
    with open("input.txt", "r") as f:
        input = f.read()
    
    shapes, grid_requirements = parse_input(sample)
    
    # Use first grid requirement
    width, height, shape_counts = grid_requirements[1]
    
    print(f"Visualizing {width}x{height} grid with shapes: {shape_counts}")
    print("Controls:")
    print("  SPACE: Pause/Resume")
    print("  UP: Speed up animation")
    print("  DOWN: Slow down animation")
    
    visualizer = ShapeFittingVisualizer(width, height, shapes, shape_counts, cell_size=50)
    solve_with_visualization(width, height, shape_counts, shapes, visualizer)

# Made with Bob
