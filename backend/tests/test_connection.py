import psycopg2

try:
    connection = psycopg2.connect(
        dbname="mygenerator",
        user="lais",
        password="2206",
        host="localhost"
    )
    print("Connection successful")
except Exception as e:
    print(f"Connection failed: {e}")
