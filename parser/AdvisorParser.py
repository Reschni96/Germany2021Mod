import csv


def instances_to_csv(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = file.read().split("\n")

    advisors = []
    for line in data:
        if "new Advisor" in line:
            advisors.append(line[line.find("(") + 1:-2].split(", "))

    headers = ["id", "name", "picture", "description", "lockedDescription", "hireCode", "dismissCode", "status"]

    with open("advisors.csv", "w", newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(advisors)


def csv_to_instances(filename):
    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)

        with open('advisors.txt', 'w', encoding='utf-8') as file:
            for row in reader:
                file.write(f'const advisor{row[1].replace(" ", "")} = new Advisor({", ".join(row)});\n')


if __name__ == '__main__':
    action = input("Enter 'txt_to_csv' to convert txt to csv OR 'csv_to_txt' to convert csv to txt: ")
    if action == "txt_to_csv":
        instances_to_csv('advisors.txt')
        print("Converted txt to csv!")
    elif action == "csv_to_txt":
        csv_to_instances('advisors.csv')
        print("Converted csv to txt!")
    else:
        print("Invalid action!")
