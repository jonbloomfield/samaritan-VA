print('importing sqlite3')
import sqlite3 as lite

def testy():
	conn=lite.connect('word_funct_db.db')
	cur=conn.cursor()
	cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
	print(cur.fetchall())
testy()