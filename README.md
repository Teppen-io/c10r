# c10r

Keeps config files in sync with a SQL db (sqlite3, mysql)

* [Installation](#installation)
* [Configuration](#configuration)
  * [Base Configuration](#base-configuration)
    * [Configuration Options](#configuration-options)
      * [backend](#backend)
      * [interval](#interval)
      * [confd](#confd)
      * [templates](#templates)
      * [sqlite3](#sqlite3)
      * [mysql](#mysql)
  * [Template Configuration](#template-configuration)
  * [Template Files](#template-files)
* [Run as a service](#run-as-a-service)
  * [Credit](#credit)

## Installation

```shell
wget https://github.com/Teppen-io/c10r/archive/master.zip && \
unzip master.zip && mv c10r-master /etc/c10r
```

## Configuration

### Base Configuration

The c10r base configuration is implemented using [Python Config Parser](https://docs.python.org/3/library/configparser.html) and is generally stored in `c10r/c10r.cfg`:

```ini
[c10r]
backend=sqlite3
interval=10
confd=/etc/c10r/conf.d/
templates=/etc/c10r/templates/

[sqlite3]
file=/home/dbuser/db.sqlite3

[mysql]
# Requires the mysql-connector-python library
## ARGS: https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
user=db_user
password=db_pass
db=nginx_config
host=127.0.0.1
port=3306
```

#### Configuration Options

##### backend

* **Type:** String
* **Desc:** Which database backend to load. c10r expects to find a dedicated config section named appropriately for the database backend.

##### interval

* **Type:** Int
* **Desc:** The number of seconds between database checks.

##### confd

* **Type:** String
* **Desc:** The filesystem path that contains the template configurations.

##### templates

* **Type:** String
* **Desc:** The filesystem path that contains the source template files.

##### sqlite3

* **Type:** Config Section
* **Desc:** Required if you have specified `backend=sqlite3`. Only contains one configuration option (`file`), the location of the database.

##### mysql

* **Type:** Config Section
* **Desc:** Required if you have specified `backend=mysql`. All specified options will be passed through to the `python-mysql-connector` library.

### Template Configuration

Template configurations are implemented using [Python Config Parser](https://docs.python.org/3/library/configparser.html) and are generally stored in `c10r/conf.d/*.cfg`

See: [Template Configuration](conf.d/)

### Template Files

Templates are parsed using [Python Template Strings](https://docs.python.org/3/library/string.html#template-strings) and are generally sourced from `c10r/templates/*.tpl`

See: [Templates](templates/)

## Run as a service

Create a systemd service config `/etc/systemd/system/c10r.service`:

```ini
[Unit]
Description=c10r Configuration Service

[Install]
WantedBy=default.target

[Service]
Environment=PYTHONUNBUFFERED=1
User=www-data
ExecStart=/etc/c10r/c10r/c10r.py
Restart=on-failure
```

Enable the service:

```shell
systemctl enable c10r.service
systemctl start c10r.service
```

### Credit

Florian Brucker [torfsen/python-systemd-tutorial](https://github.com/torfsen/python-systemd-tutorial)
