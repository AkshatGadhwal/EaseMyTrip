import psycopg2

def connect():
    params = {
    'database': 'group_44',
    'user': 'group_44',
    'password': '0I5nnozTfCaEaw',
    'host': '10.17.50.87',
    'port': 5432
    }
    c = psycopg2.connect(**params)
    return c

def commit(query, params):
    c = connect()
    cur = c.cursor()
    cur.execute(query, params)
    c.commit()
    cur.close()
    c.close()

def fetch(query, params):
    c = connect()
    cur = c.cursor()
    cur.execute(query, params)
    result = cur.fetchall()
    cur.close()
    c.close()
    return result