import mysql.connector
def conn():
    # Kết nối đến cơ sở dữ liệu MySQL
    connection = mysql.connector.connect(
        host="mysql_server",
        user="root",
        password="220503",
        database="tikiDB"
    )
    return connection