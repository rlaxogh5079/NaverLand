import pymysql

def connection() -> pymysql.connections.Connection:
    conn = pymysql.connect(
        host="localhost",
        user="user",
        password="password",
        port=3306,
    )
    print("데이터베이스에 성공적으로 연결되었습니다.")
    return conn
