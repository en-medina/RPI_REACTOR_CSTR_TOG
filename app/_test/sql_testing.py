import sqlite3
from time import sleep
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

cursor.execute('SELECT name FROM sqlite_master WHERE type =\'table\' AND name NOT LIKE \'sqlite_%\'')
print([temp[0] for temp in cursor])


cursor.execute('''
CREATE TABLE IF NOT EXISTS hola (
id INTEGER PRIMARY KEY AUTOINCREMENT,
value REAL NOT NULL,
date_created DATETIME DEFAULT (datetime('now','localtime')) 
)                        
''')
conn.commit()
cursor.execute('INSERT INTO {} (value) VALUES ({})'.format('hola', 12.2))
sleep(1.5)
cursor.execute('INSERT INTO {} (value) VALUES ({})'.format('hola', 13.2))
sleep(1.5)
cursor.execute('INSERT INTO {} (value) VALUES ({})'.format('hola', 14.2))

conn.commit()

cursor.execute('SELECT name FROM sqlite_master WHERE type =\'table\' AND name NOT LIKE \'sqlite_%\'')
print([temp[0] for temp in cursor])

cursor.execute(''' 
SELECT value, date_created FROM {} 
ORDER BY date_created DESC LIMIT 1 
'''.format('hola')
)
print(cursor.fetchone())