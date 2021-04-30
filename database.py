import sqlite3

class DBControls:
    def __init__(self):
        self.db = sqlite3.connect("db.sqlite3")
        self.cursor = self.db.cursor()
        if not self.tableExists("api_informacije"):
            self.createTable("api_informacije", ["id", "INTEGER PRIMARY KEY"], ["client_id", "TEXT"])

        if not self.tableExists("uploadovane_slike"):
            self.createTable("uploadovane_slike", ["id", "TEXT PRIMARY KEY"], ["hash", "TEXT"])

    def uploadovaneSlike(self):
        c = self.cursor.execute("SELECT id, hash FROM uploadovane_slike")
        return c.fetchall()

    def dodajUploadovanuSliku(self, id_, hashdelete):
        self.cursor.execute("INSERT INTO uploadovane_slike(id, hash) VALUES(?, ?)", (id_, hashdelete))
        self.db.commit()

    def izbrisiUploadovanuSliku(self, id_):
        self.cursor.execute("DELETE FROM uploadovane_slike WHERE id = ?", (id_,))

    def clientID(self):  # vraca client_id ili None ako client_id ne postoji
        c = self.cursor.execute("SELECT client_id FROM api_informacije")
        red = c.fetchone()
        return None if not red else red[0]

    def namestiClientID(self, clientID):
        self.cursor.execute("""
                INSERT OR REPLACE INTO api_informacije(id, client_id)
                VALUES (1,
                    COALESCE((SELECT client_id FROM api_informacije WHERE id = 1), ?)
                    )
        """, (clientID,))
        self.db.commit()

    def tableExists(self, tableName):
        c = self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tableName}'")
        if not c.fetchall():
            return False
        return True

    def createTable(self, tableName, *kolone):
        cmd = f"CREATE TABLE {tableName}({ ','.join([f'{k[0]} {k[1]}' for k in kolone]) })"
        self.cursor.execute(cmd)
        self.db.commit()
