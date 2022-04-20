import sqlite3 as sql

# Create db named database.db
conn = sql.connect('database.db')

# Create urls table with columns: original, shortened
conn.execute('CREATE TABLE urls (original TEXT, shortened TEXT)')
print("Table created successfully")
conn.close()