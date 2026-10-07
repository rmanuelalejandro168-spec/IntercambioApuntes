import sqlite3

db = sqlite3.connect("intercambio_apuntes.db")

db.execute(
    "ALTER TABLE materiales ADD COLUMN archivo TEXT NOT NULL DEFAULT ''"
)

db.commit()
db.close()

print("Columna archivo agregada correctamente")