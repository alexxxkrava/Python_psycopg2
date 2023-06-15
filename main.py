import psycopg2
from data_login import database, user, password

def create_db(cur):
        cur.execute("""
            CREATE TABLE IF NOT EXISTS client( 
                id SERIAL PRIMARY KEY,
                name VARCHAR(50),
                surname VARCHAR(50),
                email VARCHAR(80)
                );               
            """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS phones( 
                id SERIAL PRIMARY KEY,
                client_id INT NOT NULL REFERENCES client(id),
                phone VARCHAR(100)
                );               
            """)

        print('[INFO] Таблицы успешно созданы!')

def add_client(cur, name, surname, email):
        cur.execute("INSERT INTO client(name, surname, email) VALUES(%s, %s, %s);",(name, surname, email))

        print('[INFO] Данные успешно добавлены!')

def add_phone(cur, client_id, phone):
        cur.execute("INSERT INTO phones(client_id, phone) VALUES(%s, %s);", (client_id, phone))

        print('[INFO] Номер телефона успешно добавлен!')

def change_client(cur, id=None, name=None, surname=None, email=None):
        cur.execute("""
            SELECT * from client
            WHERE id = %s
            """, (id,))
        info = cur.fetchone()
        if name is None:
            name = info[1]
        if surname is None:
            surname = info[2]
        if email is None:
            email = info[3]
        cur.execute("""
            UPDATE client
            SET name = %s, surname = %s, email =%s 
            where id = %s
            """, (name, surname, email, id))
        print('[INFO] Данные успешно изменены!')

def delete_phone(cur, client_id, phone):
        cur.execute("DELETE FROM phones WHERE client_id = %s AND phone = %s", (client_id, phone))

        print('[INFO] Данные успешно удалены!')

def delete_client(cur, client_id):
        cur.execute("DELETE FROM phones WHERE client_id = %s", (client_id,))

        cur.execute("DELETE FROM client WHERE id = %s", (client_id,))

        print('[INFO] Данные успешно удалены!')

def find_client(cur, name=None, surname=None, email=None, phone=None):
    if name is None:
        name = '%'
    else:
        name = '%' + name + '%'
    if surname is None:
        surname = '%'
    else:
        surname = '%' + surname + '%'
    if email is None:
        email = '%'
    else:
        email = '%' + email + '%'
    if phone is None:
        cur.execute("""
            SELECT c.id, c.name, c.surname, c.email, p.phone FROM client c
            LEFT JOIN phones p ON c.id = p.client_id
            WHERE c.name LIKE %s AND c.surname LIKE %s
            AND c.email LIKE %s
            """, (name, surname, email))
    else:
        cur.execute("""
            SELECT c.id, c.name, c.surname, c.email, p.phone FROM client c
            LEFT JOIN phones p ON c.id = p.client_id
            WHERE c.name LIKE %s AND c.surname LIKE %s
            AND c.email LIKE %s AND p.phone LIKE %s
            """, (name, surname, email, phone))
    print(cur.fetchall())

if __name__ == '__main__':
    with psycopg2.connect(database=database, user=user, password=password) as conn:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE phones")
            cur.execute("DROP TABLE client")
            create_db(cur)
            add_client(cur,'Алексей','Кравченко','krava@mail.ru')
            add_client(cur, 'Иван', 'Иванов', 'Ivan@mail.ru')
            add_client(cur, 'Саша', 'Александров', 'Alex@mail.ru')
            add_phone(cur, '1', '89001234567')
            add_phone(cur, '2', '89009999999')
            add_phone(cur, '3', '89007777777')
            change_client(cur, "2","Илона","Саркисян","Илоша@майл.ру")
            change_client(cur, "3", "Женя", None, None)
            delete_phone(cur, '1', '89009999999')
            delete_client(cur, '1')
            find_client(cur, 'Илона')
            find_client(cur, None, 'Саркисян')
            find_client(cur, None, None, 'Илоша@майл.ру')
            find_client(cur, None, None, None,'89009999999')
            find_client(cur, 'Илона', 'Саркисян')
            find_client(cur, None, None, 'Илоша@майл.ру', '89009999999')
            find_client(cur, 'Илона', 'Саркисян', 'Илоша@майл.ру', '89009999999')
