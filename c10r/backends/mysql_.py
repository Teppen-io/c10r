import mysql.connector


class Datasource:
    # Requires the mysql-connector-python library
    # https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
    def __init__(self, query, **kwargs):
        self._cnx = mysql.connector.connect(autocommit=True, **kwargs)
        self._cursor = self._cnx.cursor(dictionary=True)
        self._query = query

    @property
    def query(self):
        return self._query

    @property
    def rows(self):
        self._cursor.execute(self._query)
        return list(self._cursor.fetchall())
