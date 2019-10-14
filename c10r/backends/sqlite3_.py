import sqlite3

class Datasource:
    # https://docs.python.org/3/library/sqlite3.html
    def __init__(self, query, **kwargs):
        self._con = sqlite3.connect(kwargs['file'])
        self._con.row_factory = sqlite3.Row
        self._query = query

    @property
    def query(self):
        return self._query

    @property
    def rows(self):
        return list(self._con.execute(self._query))
