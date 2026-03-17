import csv
import statistics
import argparse
from tabulate import tabulate
from datetime import datetime


def get_median_by_coffee_spent_each_student(raw_data: list):
    median_data, data = {}, {}

    for row in raw_data:
        if row[0] not in data.keys():
            data[row[0]] = [row[2]]
        else:
            data[row[0]].append(row[2])

    for name, volues in data.items():
        median_data[name] = statistics.median(volues)

    return median_data

def read_csv(files: list):
    data = []

    for file in files:
        with open(("storage/"+file), 'r') as f:
            reader = csv.reader(f)

            next(reader, None)

            for row in reader:
                row[1] = datetime.strptime(row[1], "%Y-%m-%d")
                row[2] = int(row[2])
                row[3] = float(row[3])
                row[4] = int(row[4])

                data.append(row)

    return data


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
    raw_result = selected_func(data)

    result = dict(sorted(raw_result.items(), key=lambda item: item[1], reverse=True))
    
    print(tabulate(result.items(), headers=["Student", "Median-coffee-spent"], tablefmt="grid"))


if __name__ == "__main__":
    main()
