from datetime import datetime
from typing import List, Dict

from utils import file_encoding_detect
import csv
import re
import json


class Task1:
    path = "../data/info"
    file_number = 3

    def __init__(self):
        self.main_data = ["Изготовитель системы",
                          "Название ОС",
                          "Код продукта",
                          "Тип системы",
                          ]
        self.os_prod_list = []
        self.os_name_list = []
        self.os_code_list = []
        self.os_type_list = []

    def get_data(self) -> List:
        data = []
        for i in range(1, self.file_number + 1):
            file_name = self.path + '_' + str(i) + '.txt'
            encoding = file_encoding_detect(file_name)
            with open(file_name, encoding=encoding) as f_n:
                f_n_reader = csv.reader(f_n)
                for row in f_n_reader:
                    self.find_values(row[0])
        data.append(self.main_data)
        for i in range(len(self.os_prod_list)):
            item = [self.os_prod_list[i], self.os_name_list[i], self.os_code_list[i], self.os_type_list[i]]
            data.append(item)
        return data

    def find_values(self, _row):
        for key in self.main_data:
            pattern = key + r':(\s*)([\s\S]+.?)'
            match = re.search(pattern, _row)
            if match:
                match = match.group(2)
                if key == self.main_data[0]:
                    self.os_prod_list.append(match)
                elif key == self.main_data[1]:
                    self.os_name_list.append(match)
                elif key == self.main_data[2]:
                    self.os_code_list.append(match)
                elif key == self.main_data[3]:
                    self.os_type_list.append(match)
                else:
                    print("Check Data")

    def write_to_csv(self):
        _data = self.get_data()
        out_file_name = "../data/main_data.csv"

        with open(out_file_name, 'w', encoding='utf-8') as f_n:
            f_n_writer = csv.writer(f_n)
            for row in _data:
                f_n_writer.writerow(row)


class Task2:
    path = '../data/orders.json'

    def write_order_to_json(self):
        with open(self.path, "r") as f_n:
            objs = json.load(f_n)
        while True:
            data = self.get_data()
            if data:
                objs["orders"].append(data)
            else:
                with open(self.path, "w") as f_n:
                    json.dump(objs, f_n, ensure_ascii=False, indent=4)
                break

    def get_data(self):
        now = datetime.today().strftime('%m/%d/%Y')
        test_data = {"item": "Телевизор",
                     "quantity": 1,
                     "price": 15000,
                     "buyer": "Петров",
                     "date": now}
        print(
            "Введите данные для записи. Для использования тестового"
            " набора введите test, для окончания введите end")
        item = input("Введите название товара: ")
        if item == "test":
            return test_data
        elif item == "end":
            return
        try:
            quantity = int(input("Введите количество товара: "))
            price = float(input("Введите цену товара: "))
        except:
            print("Попробуйте снова")
            return
        buyer = input("Введите фамилию покупателя: ")
        data = {"item": item,
                "quantity": quantity,
                "price": price,
                "buyer": buyer,
                "date": now}
        return data


class Task3:
    def a_task(self):
        pass

    def b_task(self):
        pass


def main():
    # task = Task1()
    # task.write_to_csv()
    task = Task2()
    task.write_order_to_json()


if __name__ == "__main__":
    main()
