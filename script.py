import csv
import statistics
import argparse
from tabulate import tabulate
from datetime import datetime


# Find median in coffee spent by each student
def get_median_by_coffee_spent_each_student(raw_data: list):
    median_data, data = {}, {}

    for row in raw_data:
        if row[0] not in data.keys():
            data[row[0]] = [row[2]]
        else:
            data[row[0]].append(row[2])

    for name, volues in data.items():
        median_data[name] = statistics.median(volues)

    return dict(sorted(median_data.items(), key=lambda item: item[1], reverse=True))


# Take raw row and convert elements of row to right types
def do_correct_row(row: list, file):
    try:
        try:
            row[1] = datetime.strptime(row[1], "%Y-%m-%d")
        except ValueError:
            print(f"Значение {row[1]} не соответствует формату yy-mm-dd в файле {file}")

        try:
            row[2] = int(row[2])
        except ValueError:
            print(f"Значение {row[2]} не соответствует формату для Int в файле {file}")

        try:
            row[3] = float(row[3])
        except ValueError:
            print(f"Значение {row[3]} не соответствует формату для Float в файле {file}")

        try:
            row[4] = int(row[4])
        except:
            print(f"Значение {row[4]} не соответствует формату для Int в файле {file}")

        return row
    
    except:
        print(f"Пустая строка !")

# Read CSV files from --files
def read_csv(files: list):
    data = []

    for file in files:
        try:
            with open(("storage/"+file), 'r') as f:
                reader = csv.reader(f)

                next(reader, None)

                for row in reader:
                    correct_row = do_correct_row(row, file)

                    data.append(correct_row)
        
        except FileNotFoundError:
            print(f"Файл {file} не найден !")

    return data


# Main space 
def main():
    reports = {
        "median-coffee": get_median_by_coffee_spent_each_student,
    }

    parser = argparse.ArgumentParser()

    parser.add_argument('--files', nargs='+', required=True, help="take chosen files for report")
    parser.add_argument('--report', choices=reports.keys(), required=True, help="Choose a report")

    args = parser.parse_args()

    files = args.files
    data = read_csv(files)
    
    selected_func = reports[args.report]
    result = selected_func(data) 
    
    print(tabulate(result.items(), headers=["Student", "Median-coffee-spent"], tablefmt="grid"))


if __name__ == "__main__":
    main()
