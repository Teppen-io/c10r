# c10r

Keeps config files in sync with a SQL db (sqlite3, mysql)

* [Installation](#installation)
* [Configuration](#configuration)
  * [Base Configuration](#base-configuration)
  * [Template Configuration](#template-configuration)
  * [Template Files](#template-files)
* [Run as a service](#run-as-a-service)

## Installation

```shell
wget https://github.com/Teppen-io/c10r/archive/master.zip && \
unzip master.zip && mv c10r-master /etc/c10r
```

## Configuration

### Base Configuration

The c10r base configuration is implemented using [Python Config Parser](https://docs.python.org/3/library/configparser.html) and is generally stored in `c10r/c10r.cfg`

See: [Base Configuration](base_config.md)

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

**Credit:** Florian Brucker [torfsen/python-systemd-tutorial](https://github.com/torfsen/python-systemd-tutorial)
