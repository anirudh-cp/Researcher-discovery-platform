import re

def clean_line(line):
    # Remove non-ASCII characters
    return re.sub(r'[^\x00-\x7F]+', '', line).strip()

def convert_pip_list_to_requirements(input_file, output_file):
    with open(input_file, 'r', encoding='utf-16') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        lines = infile.readlines()
        # Clean and process lines, skipping any malformed header lines
        cleaned_lines = [clean_line(line) for line in lines if line.strip()]
        # Skip header lines
        package_lines = cleaned_lines[2:]
        for line in package_lines:
            # Split by whitespace and remove empty strings
            parts = [part for part in line.split() if part]
            
            if len(parts) == 2:
                package, version = parts
                outfile.write(f"{str(package)}=={str(version)}\n")

# File paths
input_file = 'pip_list.txt'
output_file = 'requirements.txt'

# Convert pip list to requirements.txt
convert_pip_list_to_requirements(input_file, output_file)
print(f"Converted {input_file} to {output_file}")
