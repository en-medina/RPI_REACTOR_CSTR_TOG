import sqlite3
from time import sleep
from datetime import datetime
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
cursor.execute('INSERT INTO {} (value) VALUES ({})'.format('hola', 11.2))
sleep(1.5)
init = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
cursor.execute('INSERT INTO {} (value) VALUES ({})'.format('hola', 12.2))
sleep(1.5)
cursor.execute('INSERT INTO {} (value) VALUES ({})'.format('hola', 13.2))
sleep(1.5)
cursor.execute('INSERT INTO {} (value) VALUES ({})'.format('hola', 14.2))

conn.commit()

cursor.execute('SELECT name FROM sqlite_master WHERE type =\'table\' AND name NOT LIKE \'sqlite_%\'')
print([temp[0] for temp in cursor])


print(init)
cursor.execute(''' 
SELECT value, date_created FROM {0} 
WHERE date_created >= '{1}' and
date_created <= '2020-07-11 22:00:00'
ORDER BY date_created DESC
'''.format('hola', init)
)
print(cursor.fetchall())