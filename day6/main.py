def read_columns_from_file(filename="input.txt"):
    """
    Reads a file and splits each row at positions where there is a space character
    in the same position across all rows. Returns a list of columns (transposed data).
    """
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    # Remove trailing newlines but keep the content
    rows = [line.rstrip('\n') for line in lines if line.strip()]
    
    if not rows:
        return []
    
    # Find positions where there is a space in the same position in all rows
    max_length = max(len(row) for row in rows)
    split_positions = []
    
    for pos in range(max_length):
        # Check if all rows have a space at this position (or are shorter than this position)
        if all(pos >= len(row) or row[pos] == ' ' for row in rows):
            split_positions.append(pos)
    
    # Split each row based on the identified positions
    split_rows = []
    for row in rows:
        parts = []
        start = 0
        for pos in split_positions:
            if pos > start:
                parts.append(row[start:pos])
            start = pos + 1
        # Add the remaining part after the last split position
        if start < len(row):
            parts.append(row[start:].strip())
        # Filter out empty parts
        parts = [part for part in parts if part]
        split_rows.append(parts)
    
    # Transpose rows to columns
    if not split_rows:
        return []
    
    num_columns = max(len(row) for row in split_rows)
    columns = []
    for col_idx in range(num_columns):
        column = [row[col_idx] for row in split_rows if col_idx < len(row)]
        columns.append(column)
    
    return columns


def calculate_from_list(items):
    """
    Takes a list of strings containing numbers followed by a + or *.
    If the last string is a +, returns the sum of the numbers.
    If the last string is a *, returns the product of the numbers.
    """
    if not items:
        return 0
    
    # Get the operator (last element)
    operator = items[-1].strip()
    
    # Extract numbers (all elements except the last one)
    numbers = [int(item) for item in items[:-1]]
    
    if operator == '+':
        return sum(numbers)
    elif operator == '*':
        result = 1
        for num in numbers:
            result *= num
        return result
    else:
        raise ValueError(f"Invalid operator: {operator}. Expected '+' or '*'.")


def calculate_from_list_rtl(items):
    """
    Takes a list of strings containing numbers followed by a + or *.
    Numbers are read from columns right to left.
    If the last string is a +, returns the sum of the numbers.
    If the last string is a *, returns the product of the numbers.
    
    Example: ['123', ' 45', '  6', '*'] should be 356 * 24 * 1 = 8544
    """
    if not items:
        return 0
    
    # Get the operator (last element)
    operator = items[-1].strip()
    
    # Extract number strings (all elements except the last one)
    number_strings = items[:-1]
    
    # Find the maximum length to pad all strings
    max_len = max(len(s) for s in number_strings) if number_strings else 0
    
    # Pad all strings to the same length with spaces on the left
    padded_strings = [s.rjust(max_len) for s in number_strings]
    
    # Read columns from right to left
    numbers = []
    for col_idx in range(max_len - 1, -1, -1):
        # Read each column from top to bottom
        column_digits = ''.join(s[col_idx] for s in padded_strings)
        # Remove spaces and convert to integer
        column_number = int(column_digits.replace(' ', ''))
        numbers.append(column_number)
    
    if operator == '+':
        return sum(numbers)
    elif operator == '*':
        result = 1
        for num in numbers:
            result *= num
        return result
    else:
        raise ValueError(f"Invalid operator: {operator}. Expected '+' or '*'.")


def main():
    columns = read_columns_from_file()
    print("Columns from input.txt:")
    for i, col in enumerate(columns):
        print(f"Column {i}: {col}")
    results = [calculate_from_list(c) for c in columns]
    print(f"Part1: {sum(results)}")
    results2 = [calculate_from_list_rtl(c) for c in columns]
    print(f"Part2: {sum(results2)}")
    


if __name__ == "__main__":
    main()
