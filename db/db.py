import pymysql.cursors

def get_database_connection():
    connection = pymysql.connect(host='127.0.0.1',
                                user='test',
                                password='123',
                                db='meg_crk',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)

    try:
        yield connection
    finally:
        connection.close()