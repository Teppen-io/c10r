# c10r Templates

* [Basics](#basics)
* [Example Template](#example-template)
  * [Parsed Template](#parsed-template)

## Basics

Templates are parsed using [Python Template Strings](https://docs.python.org/3/library/string.html#template-strings) and are generally sourced from `c10r/templates/*.tpl`

## Example Template

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

### Parsed Template

A query that returns the following:

| name          | root          | type      | last_updated |
| ------------- | ------------- | --------- | ------------ |
| example.com   | /var/www/html | http      | 1571100927   |

Will result in the following template:

```nginx
##
# example.com:80 - Last Updated: 1571100927
##

server {
    server_name    example.com www.example.com;
    access_log     logs/example.com.access.log main;
    root           /var/www/html;
}
```
