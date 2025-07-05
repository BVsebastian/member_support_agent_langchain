import psycopg2
from psycopg2 import sql

# Replace with your actual connection details
connection = psycopg2.connect(
    dbname="postgres",
    user="postgres.xmyxcptjyvtrazvwknjy",
    password="-z*UgciLEz%v9z&",
    host="aws-0-us-west-1.pooler.supabase.com",
    port="5432"
)

try:
    cursor = connection.cursor()
    cursor.execute("SELECT 1;")
    print("Database connection successful!")
except Exception as e:
    print("Error connecting to the database:", e)
finally:
    cursor.close()
    connection.close() 