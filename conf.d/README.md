# c10r Template Configs

* [Basics](#basics)
* [Example Configuration](#example-configuration)
* [Configuration Options](#configuration-options)
  * [src](#src)
  * [write](#write)
  * [prune](#prune)
  * [dest_dir](#dest_dir)
  * [dest_name](#dest_dir)
  * [mtime](#mtime)
    * [sqlite3](#sqlite3)
  * [query](#query)
* [Template String](#temlate-strings)

## Basics

Template configurations are implemented using [Python Config Parser](https://docs.python.org/3/library/configparser.html) and are generally stored in `c10r/conf.d/*.cfg`

## Example Configuration

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

## Configuration Options

### src

* **Type:** String
* **Desc:** The source template location, usually `c10r/templates/*.tpl`. c10r will use [Python Template Strings](https://docs.python.org/3/library/string.html#template-strings) to inject SQL column values into the source template and then write the file to the filesystem.

### write

* **Type:** Bool
* **Desc:** Write parsed templates to the filesystem

### prune

* **Type:** Bool
* **Desc:** Delete non-existing templates from the filesystem. Any file without a corresonding row in the result set of the SQL query will be deleted.

### dest_dir

* **Type:** String/Template String
* **Desc:** The destination directory on the filesystem to manage. Can also include a [Template String](#template-strings). c10r will [write](#write) and [prune](#prune) files in this directory.

### dest_name

* **Type:** String/Template String
* **Desc:** The destination file on the filesystem to manage. Can also include a [Template String](#template-strings).

### mtime

* **Type:** String
* **Desc:** The name of the SQL column which holds the time that the row was last updated.  The column **must** contain an integer representation of standard Epoch time in seconds.

### query

* **Type:** String
* **Desc:** The SQL query which will return the columns necessary to correctly parse the template and write it to the filesystem.  One of the returned columns **must** contain an integer representation of standard Epoch time in seconds. See: [mtime](#mtime)

#### SQLite3

This can be achieved by using `strftime` to ensure a datetime is returned as an int (seconds since 1970-01-01.)

E.g. `SELECT strftime('%s', last_updated) as last_updated FROM my_table`

## Template Strings

`dest_dir` and `dest_file` can include [Python Template Strings](https://docs.python.org/3/library/string.html#template-strings), which will be substituted for columns returned by your SQL query.

E.g. If your query returns the following:

| name          | root          | type      | last_updated |
| ------------- | ------------- | --------- | ------------ |
| example.com   | /var/www/html | http      | 1571100927   |
| example.com   | /var/www/htm  | https     | 1571100927   |

Then:

```ini
dest_dir=/etc/nginx/sites-enabled/${location}
dest_name=${type}.conf
```

Will become:

> /etc/nginx/sites-enabled/example.com/http.conf  
/etc/nginx/sites-enabled/example.com/https.conf
