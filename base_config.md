# c10r Base Config

* [Base Configuration](#base-configuration)
  * [Configuration Options](#configuration-options)
    * [backend](#backend)
    * [interval](#interval)
    * [confd](#confd)
    * [sqlite3](#sqlite3)
    * [mysql](#mysql)

## Basics

The c10r base configuration is implemented using [Python Config Parser](https://docs.python.org/3/library/configparser.html) and is generally stored in `c10r/c10r.cfg`

## Example Configuration

```ini
[scheduler]
backend = sqlite3
interval = 10
confd = /etc/c10r/conf.d/
templates = /etc/c10r/templates/

[sqlite3]
file = /home/dbuser/db.sqlite3

[mysql]
# Requires the mysql-connector-python library
## ARGS: https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
user = db_user
password = db_pass
db = nginx_config
host = 127.0.0.1
port = 3306
```

## Configuration Options

### backend

* **Type:** String
* **Desc:** Which database backend to load. c10r expects to find a dedicated config section named appropriately for the database backend.

### interval

* **Type:** Int
* **Desc:** The number of seconds between database checks.

### confd

* **Type:** String
* **Desc:** The filesystem path that contains the template configurations.

### sqlite3

* **Type:** Config Section
* **Desc:** Required if you have specified `backend = sqlite3`. Only contains one configuration option (`file`), the location of the database.

### mysql

* **Type:** Config Section
* **Desc:** Required if you have specified `backend = mysql`. All specified options will be passed through to the `python-mysql-connector` library.
