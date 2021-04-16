import sqlite3

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS errors (ID INTEGER PRIMARY KEY, ConversionFailed integer, UnsupportedAttachments integer,
        BatchValidationFailed integer,NotRecieved integer, AttachmentNoExtension integer,InvalidFilename integer, Date text)""")
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM errors")
        rows = self.cur.fetchall()
        return rows

    def insert(self, ConversionFailed, UnsupportedAttachments, BatchValidationFailed, NotRecieved, AttachmentNoExtension, InvalidFilename, date):
        self.cur.execute("""INSERT INTO errors VALUES (NULL, ?, ?, ?,?,?,?,?)""", (ConversionFailed, UnsupportedAttachments,BatchValidationFailed, NotRecieved, AttachmentNoExtension, InvalidFilename, date))
        self.conn.commit()

    def remove(self, id):
        self.cur.execute("DELETE FROM errors WHERE id=?", (id,))
        self.conn.commit()

    def update(self, id, ConversionFailed, UnsupportedAttachments, BatchValidationFailed, NotRecieved, AttachmentNoExtension, InvalidFilename, date):
        self.cur.execute("UPDATE errors SET ConversionFailed = ?, UnsupportedAttachments = ?, BatchValidationFailed = ?, NotRecieved = ?, AttachmentNoExtension = ?, InvalidFilename = ?, date = ? WHERE id = ?", (ConversionFailed, UnsupportedAttachments, BatchValidationFailed, NotRecieved, AttachmentNoExtension, InvalidFilename, date, id))
        self.conn.commit()

    def get_average(self):
        self.cur.execute("SELECT MIN(ConversionFailed), MAX(NotRecieved) FROM errors")
        average = self.cur.fetchall()
        return average

    def erase_data(self):
        self.cur.execute("DELETE FROM errors WHERE id > 0 ")

    def __del__(self):
        self.conn.close()


db = Database("errors.db")

#db.erase_data()

# db.insert(1,2,3,4,5,6, "12/01/2021")
# db.insert(3,6,1,7,5,3, "13/01/2021")
# db.insert(5,4,0,3,3,5, "14/01/2021")
# db.insert(5,9,1,2,1,7, "15/01/2021")
# db.insert(2,5,1,1,2,1, "16/01/2021")
# db.insert(6,2,6,7,4,9, "17/01/2021")
# db.insert(0,6,7,1,7,2, "18/01/2021")
# db.insert(2,8,4,9,2,3, "19/01/2021")
# db.insert(9,0,11,0,4,8, "20/01/2021")
# db.insert(8,6,4,2,5,2, "21/01/2021")
# db.insert(3,6,4,8,4,0, "12/01/2021")
# db.insert(3,6,4,8,4,0, "12/01/2021")
# db.insert(3,6,4,8,4,0, "12/01/2021")
# db.insert(3,6,4,8,4,0, "12/01/2021")
# db.insert(3,6,4,8,4,0, "12/01/2021")
# db.insert(3,6,4,8,4,0, "12/01/2021")
# db.insert(3,6,4,8,4,0, "12/01/2021")
# db.insert(3,6,4,8,4,0, "12/01/2021")
# db.insert(3,6,4,8,4,0, "12/01/2021")
# db.insert(3,6,4,8,4,0, "12/01/2021")