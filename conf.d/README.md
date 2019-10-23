# c10r Template Configs

* [Basics](#basics)
* [Example Configuration](#example-configuration)
* [Configuration Options](#configuration-options)
  * [src](#src)
  * [dest](#dest)
  * [before](#before)
  * [after](#after)
  * [write](#write)
  * [prune](#prune)
  * [mtime](#mtime)
  * [query](#query)
    * [sqlite3 epoch](#sqlite3-epoch-time)
    * [mysql epoch](#mysql-epoch-time)
* [Template String](#temlate-strings)

## Basics

Template configurations are implemented using [Python Config Parser](https://docs.python.org/3/library/configparser.html) and are generally stored in `c10r/conf.d/*.cfg`

## Example Configuration

```ini
[template]
src=/etc/c10r/templates/nginx.conf.tpl
dest=/etc/nginx/sites-enabled/${name}.conf
before=
after=/usr/sbin/nginx -s reload
write=yes
prune=no
mtime=last_updated
query=SELECT id, name, root,
      strftime('%s', last_updated) as last_updated
      FROM api_domain
```

## Configuration Options

### src

* **Type:** String
* **Desc:** The source template location, generally `c10r/templates/*.tpl`. c10r will use [Python Template Strings](https://docs.python.org/3/library/string.html#template-strings) to inject SQL column values into the source template and then write the file to the filesystem.

### dest

* **Type:** String/Template String
* **Desc:** The destination filepath on the filesystem to manage. Can also include a [Template String](#template-strings). If enabled, c10r will also [prune](#prune) files in the parent directory.

### before

* **Type:** String
* **Desc:** The command to run before [writing](#write) templates and/or [pruning](#prune) files.

### after

* **Type:** String
* **Desc:** The command to run before [writing](#write) templates and/or [pruning](#prune) files.

### write

* **Type:** Bool
* **Desc:** Write parsed templates to the filesystem.

### prune

* **Type:** Bool
* **Desc:** Delete non-existing templates from the filesystem. Any file without a corresonding row in the result set of the SQL query will be deleted.

### mtime

* **Type:** String
* **Desc:** The name of the SQL column which holds the time that the row was last updated.  The column **must** contain an integer representation of standard Epoch time in seconds.

### query

* **Type:** String
* **Desc:** The SQL query which will return the columns necessary to correctly parse the template and write it to the filesystem.  One of the returned columns **must** contain an integer representation of Epoch time. See: [mtime](#mtime)

#### SQLite3 Epoch Time

Use `strftime` to ensure a datetime is returned as the seconds since 1970-01-01 (Unix Epoch).

E.g. `SELECT strftime('%s', last_updated) as last_updated FROM my_table`

#### MySQL Epoch Time

Use `UNIX_TIMESTAMP` to ensure a datetime is returned as the seconds since 1970-01-01 (Unix Epoch).

E.g. `SELECT UNIX_TIMESTAMP(last_updated) as last_updated FROM my_table`

## Template Strings

`dest` can include [Python Template Strings](https://docs.python.org/3/library/string.html#template-strings), which will be substituted for columns returned by your SQL query.

E.g. If your query returns the following:

| name          | root          | type      | last_updated |
| ------------- | ------------- | --------- | ------------ |
| example.com   | /var/www/html | http      | 1571100927   |
| example.com   | /var/www/htm  | https     | 1571100927   |

Then:

```ini
dest=/etc/nginx/sites-enabled/${name}/${type}.conf
```

Will become:

> /etc/nginx/sites-enabled/example.com/http.conf  
/etc/nginx/sites-enabled/example.com/https.conf
