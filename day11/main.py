sample = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""


sample2 = """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out"""


def parse_input(input_string):
    """
    Takes a String as input and returns a dict where the keys are the characters
    before the ":" and the values are a list of the words after the ":"
    """
    result = {}
    lines = input_string.strip().split('\n')
    for line in lines:
        if ':' in line:
            key, values = line.split(':', 1)
            result[key.strip()] = values.strip().split()
    return result

def count_out_paths(graph):
    """
    Takes a dict as input, starts with the value in "you" and follows the links
    to other elements until it reaches "out". Returns how many times it reaches out.
    """
    def dfs(node):
        if node == "out":
            return 1
        if node not in graph:
            return 0
        
        count = 0
        for neighbor in graph[node]:
            count += dfs(neighbor)
        return count
    
    if "you" not in graph:
        return 0
    
    total_count = 0
    for start_node in graph["you"]:
        total_count += dfs(start_node)
    
    return total_count


def count_paths_with_nodes(graph, start, end, required_nodes):
    """
    Count paths from start to end that contain all required_nodes.
    Uses DFS with memoization - only tracks which required nodes have been collected.
    This is much more efficient than tracking all visited nodes.
    """
    memo = {}
    required_set = frozenset(required_nodes)
    
    def dfs(node, collected_required):
        # Create cache key: (current node, which required nodes we've collected)
        cache_key = (node, collected_required)
        
        if cache_key in memo:
            return memo[cache_key]
        
        # Update collected required nodes if current node is one of them
        new_collected = collected_required
        if node in required_set:
            new_collected = collected_required | frozenset([node])
        
        # If we reached the end, check if all required nodes are collected
        if node == end:
            result = 1 if new_collected == required_set else 0
            memo[cache_key] = result
            return result
        
        # If node not in graph, dead end
        if node not in graph:
            memo[cache_key] = 0
            return 0
        
        count = 0
        # Explore all neighbors
        for neighbor in graph[node]:
            count += dfs(neighbor, new_collected)
        
        memo[cache_key] = count
        return count
    
    # Start DFS from the start node
    return dfs(start, frozenset())


def main():
    # Test with sample2
    print("Testing with sample2:")
    parsed_sample2 = parse_input(sample2)
    print("Parsed data:")
    for key, values in parsed_sample2.items():
        print(f"{key}: {values}")
    
    # Count paths from 'svr' to 'out' that contain both 'dac' and 'fft'
    required_nodes = {'dac', 'fft'}
    result = count_paths_with_nodes(parsed_sample2, 'svr', 'out', required_nodes)
    print(f"\nPaths from 'svr' to 'out' containing both 'dac' and 'fft': {result}")
    
    # Original functionality with input.txt
    print("\n" + "="*50)
    print("Testing with input.txt:")
    try:
        with open('input.txt', 'r') as f:
            input_string = f.read()
        parsed_data = parse_input(input_string)
        print("Parsed data:")
        for key, values in parsed_data.items():
            print(f"{key}: {values}")
        
        print("\nCounting paths to 'out':")
        result = count_out_paths(parsed_data)
        print(f"Total paths reaching 'out': {result}")
        
        # Count paths from 'svr' to 'out' that contain both 'dac' and 'fft'
        if 'svr' in parsed_data:
            required_nodes = {'dac', 'fft'}
            result_with_nodes = count_paths_with_nodes(parsed_data, 'svr', 'out', required_nodes)
            print(f"Total paths reaching 'out' containing both 'dac' and 'fft': {result_with_nodes}")
    except FileNotFoundError:
        print("input.txt not found, skipping...")


if __name__ == "__main__":
    main()
