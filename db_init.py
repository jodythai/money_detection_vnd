import psycopg2

def db_get_connection():
  """ Return a database connection or None if error occurs
  """
  try:
    connection = psycopg2.connect(user="duong",
                                  password="P@ssw0rd",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="snoopy_kitty")
    return connection

  except Exception as error:
    print(error)
    return None

def create_tables():
  """ Create tables
  """
  try:
    connection = db_get_connection()
    if not connection:
        print('ERROR: Connection db fail')
        return
    cur = connection.cursor()

    query = """
            CREATE TABLE IF NOT EXISTS predict_correction (
              id SERIAL NOT NULL PRIMARY KEY,
              upload_file_path TEXT NOT NULL,
              label INTEGER NOT NULL,
              created_on TIMESTAMP
              );
            """
    cur.execute(query)
    connection.commit()
  except Exception as error:
    print('ERROR: Create table fail -', error)
    connection.rollback()

  finally:
    cur.close()
    connection.close()

def insert_row(data, table_name, default=True):
  """Insert data into table_name
  """
  # print("INFO: Insert data into {}".format(table_name))

  try:
    connection = db_get_connection()
    if not connection:
        print('ERROR: Connection db fail')
        return
    cur = connection.cursor()

    cols = 'DEFAULT,' if default else ''
    for i in range(len(data)-1):
        cols = cols + '%s,'
    cols = cols + '%s'

    query = 'INSERT INTO ' + table_name + ' VALUES (' + cols + ');'
    cur.execute(query, data)

    connection.commit()

  except Exception as error:
    print('ERROR: Insert into DB fail -', error)
    connection.rollback()

  finally:
    cur.close()
    connection.close()