def parse_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        lines = infile.read().split('\n')

        outfile.write("tooltipList = [\n")

        for i in range(0, len(lines), 3):  # skip 3 lines (phrase, explanation, and empty line)
            phrase = lines[i].replace('"', '\\"')  # Escape any double quotes
            explanation = lines[i + 1].replace('"', '\\"') if i + 1 < len(lines) else ""
            outfile.write(f'    {{searchString: "{phrase}", explanationText: "{explanation}"}},\n')

        outfile.write("];\n")


parse_file('input.txt', 'output.txt')
