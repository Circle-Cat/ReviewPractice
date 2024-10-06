import re

def validate_format(input_string):
    # Regular expression pattern
    pattern = r'(\d+)\.\s([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)'
    
    lines = input_string.splitlines()  # Split input string into lines

    # Check the introductory text
    if lines[0] != "This is a list of people who knows how to use Gerrit, Yay!":
        raise ValueError('Introductory text is missing or incorrect')
    
    # Check the empty line
    if lines[1] != "":
        raise ValueError('Expected an empty line after the introductory text')
    
    # Create a set to store email addresses
    emails = set()
    
    # The expected line number starts at 0
    expected_num = 0

    # Check the rest of the lines
    for i, line in enumerate(lines[2:], start=2):
        # If we reach the last two lines, break the loop
        if i >= len(lines) - 2:
            break

        # Match the pattern
        match = re.fullmatch(pattern, line)
        if match is None:
            raise ValueError(f'Line {i+1} is invalid')
        
        num, email = int(match.group(1)), match.group(2)

        # Check the line number
        if num != expected_num:
            raise ValueError(f'Expected line number {expected_num}, but got {num}')

        # Check the email
        if email in emails:
            raise ValueError(f'Duplicate email found: {email}')
        
        emails.add(email)
        expected_num += 1  # Increment the expected line number
    
    # Check the last empty line
    if lines[-2] != "":
        raise ValueError('Expected an empty line before the NextId line')
    
    # Check the NextId line
    next_id_line = f'NextId: {expected_num}'
    if lines[-1] != next_id_line:
        raise ValueError(f'Expected {next_id_line}, but got {lines[-1]}')

# Read the README.md file and validate its content
with open('README.md', 'r') as file:
    content = file.read()

validate_format(content)
print("All lines are valid.")
