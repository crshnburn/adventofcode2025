def read_input(filename='input.txt'):
    """
    Reads input.txt and returns the contents.
    The first part contains ranges of numbers (one per line).
    The second part contains a list of numbers.
    Returns a tuple: (ranges, numbers)
    """
    with open(filename, 'r') as f:
        content = f.read().strip()
    
    # Split by empty line to separate the two parts
    parts = content.split('\n\n')
    
    # Parse the first part (ranges)
    ranges = []
    for line in parts[0].strip().split('\n'):
        ranges.append(line)
    
    # Parse the second part (list of numbers)
    numbers = []
    if len(parts) > 1:
        for line in parts[1].strip().split('\n'):
            numbers.append(line)
    
    return ranges, numbers


def filter_numbers_in_ranges(ranges, numbers):
    """
    Takes a list of ranges and a list of numbers as input and returns
    a list of numbers that are present in at least one of the ranges.
    
    Args:
        ranges: List of range strings in format "start|end"
        numbers: List of number strings
    
    Returns:
        List of numbers that fall within at least one range
    """
    result = []
    
    # Parse ranges into tuples of (start, end)
    parsed_ranges = []
    for range_str in ranges:
        start, end = map(int, range_str.split('-'))
        parsed_ranges.append((start, end))
    
    # Check each number against all ranges
    for num_str in numbers:
        num = int(num_str)
        for start, end in parsed_ranges:
            if start <= num <= end:
                result.append(num_str)
                break  # No need to check other ranges once found
    
    return result

def count_numbers_in_ranges(ranges):
    """
    Takes a list of ranges and returns the count of unique numbers that fall
    within at least one of the ranges.
    
    Args:
        ranges: List of range strings in format "start|end"
    
    Returns:
        Integer count of unique numbers covered by the ranges
    
    Example:
        ranges = ["3-5", "10-14", "16-20", "12-18"]
        Returns 14 (numbers: 3,4,5,10,11,12,13,14,16,17,18,19,20 = 13 unique, but overlapping ranges merge)
    """
    if not ranges:
        return 0
    
    # Parse ranges into tuples of (start, end)
    parsed_ranges = []
    for range_str in ranges:
        start, end = map(int, range_str.split('-'))
        parsed_ranges.append((start, end))
    
    # Sort ranges by start position
    parsed_ranges.sort()
    
    # Merge overlapping ranges and count total numbers
    merged_ranges = []
    current_start, current_end = parsed_ranges[0]
    
    for start, end in parsed_ranges[1:]:
        if start <= current_end + 1:
            # Ranges overlap or are adjacent, merge them
            current_end = max(current_end, end)
        else:
            # No overlap, save current range and start new one
            merged_ranges.append((current_start, current_end))
            current_start, current_end = start, end
    
    # Don't forget the last range
    merged_ranges.append((current_start, current_end))
    
    # Count total numbers in merged ranges
    total_count = 0
    for start, end in merged_ranges:
        total_count += (end - start + 1)
    
    return total_count



def main():
    ranges, numbers = read_input()
    print("Hello from day5!")
    print(f"Ranges: {ranges}")
    print(f"Numbers: {numbers}")
    
    filtered_numbers = filter_numbers_in_ranges(ranges, numbers)
    print(f"Filtered numbers: {len(filtered_numbers)}")
    print(f"Total fresh: {count_numbers_in_ranges(ranges)}")


if __name__ == "__main__":
    main()
