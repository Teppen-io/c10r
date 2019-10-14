# c10r

Keeps config files in sync with a SQL db (sqlite3, mysql)

## Usage

### Installalation

```shell
wget https://github.com/Teppen-io/c10r/archive/master.zip
unzip master.zip && mv c10r-master /etc/c10r
```

### Configuration

#### Base Configuration

The c10r base configuration is stored in `/etc/c10r/c10r.cfg`:

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

#### Template Configuration

Template confiurations are stored in `conf.d/*.cfg`:

```ini
[template]
src=/etc/c10r/templates/nginx.conf.tpl
write=yes
prune=yes
dest_dir=/etc/nginx/sites-enabled
dest_name=${name}.conf
mtime=last_updated
query=SELECT id, name, root
      strftime('%s', last_updated) as last_updated
      FROM http_servers
```

#### Template files

Templates are stored in `/etc/c10r/templates/*.tpl`:

```nginx
##
# ${name}:80 - Last Updated: ${last_updated}
##

server {
    server_name    ${name} www.${name};
    access_log     logs/${name}.access.log main;
    root           ${root};
}
```

## Run as a service

Create a systemd service config `/etc/systemd/system/c10r.service`:

```ini
[Unit]
Description=c10r keeps config files in sync with a SQL db (sqlite3, mysql)

[Install]
WantedBy=default.target

[Service]
Environment=PYTHONUNBUFFERED=1
User=www-data
ExecStart=/etc/c10r/c10r.py
Restart=on-failure
```

Enable the service:

```shell
systemctl enable c10r.service
systemctl start c10r.service
```

### Credit

Florian Brucker [torfsen/python-systemd-tutorial](https://github.com/torfsen/python-systemd-tutorial)
