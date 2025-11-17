import sqlite3, os

DB = os.path.join(os.path.dirname(__file__), "store.db")
conn = sqlite3.connect(DB)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS products (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  disease TEXT,
  product TEXT,
  description TEXT,
  price REAL
)
""")

samples = [
  ("Tomato___Early_blight","Fungicide A","Effective for early blight",199.0),
  ("Tomato___Early_blight","Organic Spray B","Organic alternative",149.0),
  ("Potato___Early_blight","Fungicide P","Potato blight control",220.0),
  ("Tomato___healthy","Fertilizer X","Supports healthy growth",99.0)
]

c.executemany("INSERT INTO products (disease,product,description,price) VALUES (?,?,?,?)", samples)
conn.commit()
conn.close()

print("Database created:", DB)
