import csv
import psycopg2

# Подключение к базе данных PostgreSQL
conn = psycopg2.connect(
    dbname="krisha_db",
    user="admin",
    password="12345",
    host="localhost",
    port="5432"
)

# Открытие файла CSV и чтение данных
csv_file_path = "/home/ibragim/python_mor/parsing/krisha/flat.csv"

with open(csv_file_path, 'r', newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Пропуск заголовков столбцов, если они есть в CSV-файле
    for row in reader:
        rooms, square, floor, payment, address, city, price, date, image, link = row
        # Здесь происходит вставка данных из CSV в таблицу PostgreSQL
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO krisha (rooms, square, floor, payment, address, city, price, date, image, link) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
            (rooms, square, floor, payment, address, city, price, date, image, link)
        )
        conn.commit()
        cursor.close()

# Закрытие соединения с базой данных PostgreSQL
conn.close()