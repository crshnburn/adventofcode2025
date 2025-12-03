from itertools import combinations

def read_input(filename="input.txt"):
    """Read input file and return a list of all lines."""
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]


def find_largest_two_digit(s):
    """
    Find the largest two-digit integer that appears with digits in order.
    
    Args:
        s: A string containing digits
        
    Returns:
        The largest two-digit integer formed by any two digits in order
        
    Examples:
        811111111111119 returns 89
        818181911112111 returns 92
    """
    max_value = -1
    
    pairs = [int("".join(combo)) for combo in combinations(s, 2)]
    
    return max(pairs)

def find_max_joltage(s, length) -> str:
    if length == 0:
        return ""
    next_digit = max(s[: len(s) - length + 1])
    next_pos = s.find(next_digit)
    return next_digit + find_max_joltage(s[next_pos + 1 :], length - 1)


def main():
    lines = read_input()
    print("Hello from day3!")
    print(f"Read {len(lines)} lines from input.txt")
    
    # Map the find_largest_two_digit function to each line and sum the results
    values = [find_largest_two_digit(line) for line in lines]
    total = sum(values)
    print(f"Sum of largest two-digit values: {total}")
    values = [int(find_max_joltage(line, 12)) for line in lines]
    total = sum(values)
    print(f"Sum of largest twelve-digit values: {total}")


if __name__ == "__main__":
    main()
