import sqlite3
import xlrd


class Database:
    def __init__(self, name):
        self._conn = sqlite3.connect(name)
        self._cursor = self._conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        self.commit()
        return self.fetchall()

    def create_table(self):
        self.query("""CREATE TABLE IF NOT EXISTS data(id TEXT, income_active TEXT ,
        income_passive TEXT , debet TEXT , credit TEXT , outcome_active TEXT , outcome_passive TEXT );""")

    def insert_data(self):
        workbook = xlrd.open_workbook("upload/xls")
        worksheet = workbook.sheets()
        sheet = worksheet[0]
        nrows = sheet.nrows
        for i in range(nrows):
            row = sheet.row_values(i)
            self.query("""INSERT INTO data (id, income_active, income_passive, debet, credit,
             outcome_active,outcome_passive ) VALUES(?,?,?,?,?,?,?);""", row)

    def display_table(self):
        return self.query("SELECT * FROM data")
