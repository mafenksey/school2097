import csv
import os
import json
import pathlib
import time


def write_to_csv(path: str, csv_file: str, fieldnames: list, values: json):
    path = os.path.join(path, csv_file)
    data = json.loads(values)
    if not os.path.exists(path):
        with open(csv_file, mode='w', newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for key in data.keys():
                writer.writerow(data[key])
                print("new data has been written")
    else:
        with open(csv_file, mode='a+', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            for key in data.keys():
                writer.writerow(data[key])
                print("new data has been written")


def write_to_csv_2(path: str, csv_file: str, fieldnames: list, values: json):
    path = os.path.join(path, csv_file)
    data = json.loads(values)
    mode = "w" if not os.path.exists(path) else "a+"
    with open(csv_file, mode=mode, newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if mode == "w":
            writer.writeheader()
        for key in data.keys():
            writer.writerow(data[key])
            print("new data has been written")


def read_from_csv(csv_file, ):
    with open(csv_file) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)  # пропускаем заголовок
        for row in reader:
            print(row)


def _main():
    path = pathlib.Path(__file__).parent.absolute()
    # print(path)
    for _ in range(2):
        data = json.dumps({i: i + 2 for i in range(1, 17)})
        fieldnames = list(map(str, range(1, 17)))
        print("new data has been received")
        write_to_csv(path, "city_temps", fieldnames, data)
        time.sleep(5)


if __name__ == "__main__":
    _main()
