import json
import sqlite3


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

                result = {table_name: data}
                return result
            except sqlite3.OperationalError:
                print(f'В вашей базе данных нет таблицы \"{table_name}\"')



def main(db_file, table_name):
    db = DataBase(db_file)
    data = db.get_data(table_name)

    data = json.dumps(data, indent=2, ensure_ascii=False)
    with open(f'{table_name}.json', 'w', encoding='utf-8') as f:
        f.write(data)


if __name__ == "__main__":
    db_file = input('Введите название базы данных: ')
    table_name = input('Введите название таблицы: ')
    main(db_file, table_name)
