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


"""function downloadCSV(csv, filename) {
    const blob = new Blob([new Uint8Array([0xEF, 0xBB, 0xBF]), csv], { type: 'text/csv;charset=utf-8;' }); // Add UTF-8 BOM
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
}

let parsedJson = campaignTrail_temp.answers_json;

// Initialize an empty array to store the CSV rows
let csvRows = [];

// Add the header to the CSV
csvRows.push("PK,Description");

// Iterate through the parsed JSON array
parsedJson.forEach(item => {
  let pk = item.pk;
  let description = item.fields.description;

  // Escape any quotes in the description by doubling them
  description = description.replace(/"/g, '""');

  // Create a CSV row for this item and add it to the array
  let csvRow = `"${pk}","${description}"`;
  csvRows.push(csvRow);
});

// Join the rows into a single CSV string
let csvString = csvRows.join('\n');

// Trigger download
downloadCSV(csvString, 'output.csv');





function downloadCSV(csv, filename) {
    const blob = new Blob([new Uint8Array([0xEF, 0xBB, 0xBF]), csv], { type: 'text/csv;charset=utf-8;' }); // Add UTF-8 BOM
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
}

let parsedJson = advisorsList;

// Initialize an empty array to store the CSV rows
let csvRows = [];

// Add the header to the CSV
csvRows.push("Name, Description, LockedDescription");

// Iterate through the parsed JSON array
parsedJson.forEach(item => {
  let name = item.name;
  let description = item.description;
  let lockedDescription = item.lockedDescription;

  // Escape any quotes in the description by doubling them
  description = description.replace(/"/g, '""');

  // Create a CSV row for this item and add it to the array
  let csvRow = `"${name}","${description}","${lockedDescription}"`;
  csvRows.push(csvRow);
});

// Join the rows into a single CSV string
let csvString = csvRows.join('\n');

// Trigger download
downloadCSV(csvString, 'output.csv');

"""