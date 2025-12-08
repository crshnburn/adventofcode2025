

sample = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""

def get_test_coordinates():
    coordinates = []
    for line in sample.split('\n'):
        line = line.strip()
        if line:
            x, y, z = map(int, line.split(','))
            coordinates.append((x, y, z))
    return coordinates


def read_coordinates(filename="input.txt"):
    """
    Reads coordinates from a file where each line contains 3 comma-separated integers.
    Returns a list of tuples (x, y, z).
    """
    coordinates = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                x, y, z = map(int, line.split(','))
                coordinates.append((x, y, z))
    return coordinates

def calculate_distance(coord1, coord2):
    """
    Calculate the Euclidean distance between two 3D coordinates.
    """
    x1, y1, z1 = coord1
    x2, y2, z2 = coord2
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2) ** 0.5


def find_coordinate_pairs_by_distance(coordinates):
    """
    Takes a list of x,y,z coordinates, finds the distance between all of them,
    and returns a list of pairs of coordinates ordered by distance, smallest to largest.
    """
    pairs_with_distances = []
    
    # Generate all unique pairs of coordinates
    for i in range(len(coordinates)):
        for j in range(i + 1, len(coordinates)):
            coord1 = coordinates[i]
            coord2 = coordinates[j]
            distance = calculate_distance(coord1, coord2)
            pairs_with_distances.append((distance, coord1, coord2))
    
    # Sort by distance (smallest to largest)
    pairs_with_distances.sort(key=lambda x: x[0])
    
    # Return list of coordinate pairs (without distances)
    return [(coord1, coord2) for distance, coord1, coord2 in pairs_with_distances]


def create_coordinate_chains(pairs):
    """
    Takes a list of pairs of coordinates and creates chains of coordinates.
    A chain is formed by connecting pairs that share a common coordinate.
    Returns the list of chains ordered from largest to smallest.
    """
    if not pairs:
        return []
    
    # Build an adjacency map: coordinate -> list of connected coordinates
    adjacency = {}
    for coord1, coord2 in pairs:
        if coord1 not in adjacency:
            adjacency[coord1] = []
        if coord2 not in adjacency:
            adjacency[coord2] = []
        adjacency[coord1].append(coord2)
        adjacency[coord2].append(coord1)
    
    # Find all chains using depth-first search
    visited = set()
    chains = []
    
    def dfs(coord, chain):
        """Depth-first search to build a chain"""
        visited.add(coord)
        chain.append(coord)
        if coord in adjacency:
            for neighbor in adjacency[coord]:
                if neighbor not in visited:
                    dfs(neighbor, chain)
    
    # Start DFS from each unvisited coordinate
    for coord in adjacency:
        if coord not in visited:
            chain = []
            dfs(coord, chain)
            chains.append(chain)
    
    # Sort chains by length (largest to smallest)
    chains.sort(key=lambda x: len(x), reverse=True)
    
    return chains

class UnionFind:
    """Union-Find (Disjoint Set Union) data structure for Kruskal's algorithm"""
    def __init__(self, coordinates):
        self.parent = {coord: coord for coord in coordinates}
        self.rank = {coord: 0 for coord in coordinates}
    
    def find(self, coord):
        """Find the root of the set containing coord with path compression"""
        if self.parent[coord] != coord:
            self.parent[coord] = self.find(self.parent[coord])
        return self.parent[coord]
    
    def union(self, coord1, coord2):
        """Union two sets by rank"""
        root1 = self.find(coord1)
        root2 = self.find(coord2)
        
        if root1 == root2:
            return False
        
        if self.rank[root1] < self.rank[root2]:
            self.parent[root1] = root2
        elif self.rank[root1] > self.rank[root2]:
            self.parent[root2] = root1
        else:
            self.parent[root2] = root1
            self.rank[root1] += 1
        
        return True


def create_mst_kruskals(pairs):
    """
    Uses Kruskal's algorithm to create a Minimum Spanning Tree from a sorted list of coordinate pairs.
    Returns the last two coordinates added to the tree.
    
    Args:
        pairs: List of coordinate pairs sorted by distance (smallest to largest)
    
    Returns:
        Tuple of the last two coordinates added to the MST, or None if MST cannot be formed
    """
    if not pairs:
        return None
    
    # Extract all unique coordinates
    all_coords = set()
    for coord1, coord2 in pairs:
        all_coords.add(coord1)
        all_coords.add(coord2)
    
    # Initialize Union-Find structure
    uf = UnionFind(all_coords)
    
    # Track edges added to MST
    mst_edges = []
    
    # Process edges in order (already sorted by distance)
    for coord1, coord2 in pairs:
        # Try to add edge to MST
        if uf.union(coord1, coord2):
            mst_edges.append((coord1, coord2))
            
            # MST is complete when we have n-1 edges for n vertices
            if len(mst_edges) == len(all_coords) - 1:
                break
    
    # Return the last two coordinates added
    if len(mst_edges) >= 2:
        last_edge = mst_edges[-1]
        second_last_edge = mst_edges[-2]
        return (last_edge[0], last_edge[1], second_last_edge[0], second_last_edge[1])
    elif len(mst_edges) == 1:
        return mst_edges[-1]
    else:
        return None


def main():
    coordinates = read_coordinates("input.txt")
    # coordinates = get_test_coordinates()
    print("Hello from day8!")
    # print(f"Read {len(coordinates)} coordinates")
    # print(f"First 10 pairs: {find_coordinate_pairs_by_distance(coordinates)[:10]}")
    pairs_to_check = find_coordinate_pairs_by_distance(coordinates)
    # chains = create_coordinate_chains(pairs_to_check)
    # print(f"Largest chain: {create_coordinate_chains(pairs_to_check)}")
    # print(f'Part 1: {len(chains[0])*len(chains[1])*len(chains[2])}')
    last_nodes = create_mst_kruskals(pairs_to_check)
    print(f"Part 2: {last_nodes[0][0] * last_nodes[1][0]}")
    




if __name__ == "__main__":
    main()

