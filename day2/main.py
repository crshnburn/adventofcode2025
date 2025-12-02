def read_number_pairs(filename='day2/input.txt'):
    """
    Reads from a file and splits the line of text by comma,
    then returns pairs of numbers which are separated by a hyphen.
    
    Example input: "1-2,3-4,5-6"
    Returns: [(1, 2), (3, 4), (5, 6)]
    """
    pairs = []
    with open(filename, 'r') as f:
        content = f.read().strip()
        # Split by comma to get individual pair strings
        pair_strings = content.split(',')
        for pair_str in pair_strings:
            # Split each pair by hyphen
            numbers = pair_str.strip().split('-')
            if len(numbers) == 2:
                pairs.append((int(numbers[0]), int(numbers[1])))
    return pairs

def find_repeated_numbers(pairs):
    """
    Takes a list of pairs and returns a list of numbers where the first half
    of the number is the same as the second half.
    
    Example: 11, 123123, 4444
    
    Args:
        pairs: List of tuples containing (start, end) ranges
        
    Returns:
        List of numbers where first half equals second half
    """
    palindromic_numbers = []
    
    for start, end in pairs:
        for num in range(start, end + 1):
            num_str = str(num)
            length = len(num_str)
            
            # Only check even-length numbers (odd-length can't have equal halves)
            if length % 2 == 0:
                mid = length // 2
                first_half = num_str[:mid]
                second_half = num_str[mid:]
                
                if first_half == second_half:
                    palindromic_numbers.append(num)
    
    return palindromic_numbers

def find_repeated_pattern_numbers(pairs):
    """
    Takes a list of pairs and returns a list of numbers where the number
    is made up of a repeated pattern of digits.
    
    Example: 11, 111, 1010, 222222, 446446, 824824824
    
    Args:
        pairs: List of tuples containing (start, end) ranges
        
    Returns:
        List of numbers that consist of a repeated digit pattern
    """
    repeated_numbers = []
    
    for start, end in pairs:
        for num in range(start, end + 1):
            num_str = str(num)
            length = len(num_str)
            
            # Try all possible pattern lengths (from 1 to half the number length)
            for pattern_len in range(1, (length // 2) + 1):
                if length % pattern_len == 0:
                    # Extract the pattern
                    pattern = num_str[:pattern_len]
                    # Check if repeating this pattern gives us the original number
                    repetitions = length // pattern_len
                    if pattern * repetitions == num_str:
                        repeated_numbers.append(num)
                        break  # Found a valid pattern, no need to check longer ones
    
    return repeated_numbers


def main():
    print("Hello from day2!")
    pairs = read_number_pairs()
    print(f"Number pairs: {pairs}")
    
    palindromic_numbers = find_repeated_numbers(pairs)
    print(f"Palindromic numbers: {palindromic_numbers}")
    print(f"Count: {len(palindromic_numbers)}")
    print(f"Sum: {sum(palindromic_numbers)}")
    
    repeated_pattern_numbers = find_repeated_pattern_numbers(pairs)
    print(f"\nRepeated pattern numbers: {repeated_pattern_numbers}")
    print(f"Count: {len(repeated_pattern_numbers)}")
    print(f"Sum: {sum(repeated_pattern_numbers)}")


if __name__ == "__main__":
    main()
