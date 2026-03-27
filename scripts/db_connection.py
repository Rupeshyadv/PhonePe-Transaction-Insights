import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="RRyy1234@$",
        database="phonepe_db",
    )
    return conn