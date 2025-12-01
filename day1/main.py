from devtools import debug


def readFile() -> list[str]:
    """Reads input.txt and returns an array of strings of each line in the file."""
    with open("input.txt", "r") as file:
        return [line.strip() for line in file.readlines()]


def main():
    print("Hello from day1!")
    lines: list[str] = readFile()
    print(f"Read {len(lines)} lines from input.txt")
    password: int = turnDial(instructions=lines)
    print(f"Part1 password: {turnDial(instructions=lines)}")
    print(f"Part2 password: {turnDial2(instructions=lines)}")

def turnDial(instructions: list[str]) -> int:
    dialPos: int = 50
    password: int = 0
    for line in instructions:
        direction = line[0]
        amount = int(line[1:])
        debug(dialPos, direction, amount)
        if direction == 'L':
            dialPos -= amount 
        elif direction == 'R':
            
            dialPos += amount
        dialPos %= 100
        if dialPos == 0:
            password += 1
    return password

def turnDial2(instructions: list[str]) -> int:
    dialPos: int = 50
    password: int = 0

    for line in instructions:
        direction = line[0]
        amount = int(line[1:])
        password += int(amount / 100)
        if direction == 'L':
            if dialPos != 0 and amount % 100 > dialPos:
                password += 1
            dialPos -= amount % 100
        elif direction == 'R':
            if dialPos != 0 and amount % 100  > 100 - dialPos:
                password += 1
            dialPos += amount % 100
        
        dialPos %= 100
        if dialPos == 0:
            password += 1
        debug(direction, amount, dialPos, password)
        
    return password

if __name__ == "__main__":
    main()
