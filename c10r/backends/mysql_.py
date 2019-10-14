import mysql.connector

class Datasource:
    # https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
    def __init__(self, query, **kwargs):
        self._cnx = mysql.connector.connect(**kwargs)
        self._cursor = self._cnx.cursor()
        self._query = query

    @property
    def query(self):
        return self._query

    @property
    def rows(self):
        return list(self._cursor.fetchall(self.query))
