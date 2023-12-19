import json
import sqlite3
import pandas as pd


class DataBase():

    def __init__(self, db_file):
        self.connect = sqlite3.connect(db_file)
        self.cursor = self.connect.cursor()

    def get_data(self, table_name):
        with self.connect:
            try:
                self.cursor.execute(f"""
                    SELECT * FROM {table_name}""")

                rows = self.cursor.fetchall()
                data = []

                for row in rows:
                    row_dict = {}
                    for i, column_name in enumerate(self.cursor.description):
                        row_dict[column_name[0]] = row[i]
                    data.append(row_dict)

                # result = {table_name: data}
                return data
            except sqlite3.OperationalError:
                print(f'В вашей базе данных нет таблицы \"{table_name}\"')
                input()



def main(db_file: str, table_name: str):
    print("""
          1. Форматировать в json
          2. Форматировать в csv
        """)
    
    while True:
        try:
            question = int(input("Введите номер команды: "))
            break
        except ValueError:
            print("Вы ввели букву, нужно ввести номер команды")
    
    db = DataBase(db_file)
    data = db.get_data(table_name)

    if question == 1:
        data = json.dumps(data, indent=2, ensure_ascii=False)
        with open(f'{table_name}.json', 'w', encoding='utf-8') as f:
            f.write(data)
        print(f"Таблица \"{table_name}\" преобразована в json формат")
        input()
            
    elif question == 2:
        df = pd.DataFrame(data)
        df.to_csv(f"{table_name}.csv", encoding="utf-8", index=False)
        print(f"Таблица \"{table_name}\" преобразована в csv формат, с кодировкой utf-8")
        input()
    
    else:
        print("Такой команды нет")
        input()


if __name__ == "__main__":
    db_file = input('Введите название базы данных: ')
    table_name = input('Введите название таблицы: ')
    main(db_file, table_name)
