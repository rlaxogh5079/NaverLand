from connection import connection
import pymysql

def create_database(connection: pymysql.connections.Connection) -> None:
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE NaverLand;")
    except:
        pass
    cursor.execute("USE NaverLand;")

def create_user() -> None:
    connection = pymysql.connect(
        host="localhost",
        port=3306
    )
    cursor = connection.cursor()
    cursor.execute("CREATE USER 'user'@'%' IDENTIFIED BY 'password';")
    cursor.execute("GRANT ALL PRIVILEGES ON *.* TO 'user'@'%' WITH GRANT OPTION;")
    cursor.execute("flush privileges;")


def create_table(connection: pymysql.connections.Connection) -> None:
    cursor = connection.cursor()
    pass

conn = connection()
create_database(conn)
create_table(conn)