import csv
import os


def csv_to_js_object(key_column, value_column):
    js_object_lines = []
    script_dir = os.path.dirname(os.path.realpath(__file__))
    csv_file_path = os.path.join(script_dir, 'answers.csv')

    with open(csv_file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            key = row.get(key_column)
            value = row.get(value_column)

            if key and value and key != "0" and value != "0" and key != "-" and value != "-":
                js_object_lines.append(f"        {key}: {value},")

    return "{\n" + "\n".join(js_object_lines) + "\n    }"


if __name__ == '__main__':
    key_column = "PK"
    value_column = "Pivot"

    js_object_str = csv_to_js_object(key_column, value_column)

    script_dir = os.path.dirname(os.path.realpath(__file__))
    output_file_path = os.path.join(script_dir, 'dict.txt')

    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write("const pivotMap = " + js_object_str + ";")

    print(f"The JavaScript object has been saved to {output_file_path}")
