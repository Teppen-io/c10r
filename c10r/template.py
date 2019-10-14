import os
from pathlib import Path
from string import Template


class TemplateResource:
    def __init__(self, backend, backend_config, template_config):
        self._config = template_config
        self._datasource = self._set_backend(backend, backend_config)
    
    def _set_backend(self, backend, backend_config):
        if backend == 'mysql':
            from backends.mysql_ import Datasource
        elif backend == 'sqlite3':
            from backends.sqlite3_ import Datasource
        return Datasource(self._config['query'], **backend_config)

    def _get_filesystem_state(self):
        flist = list(Path(self._config['dest_dir']).glob('*'))
        return [
            (
                file.relative_to(self._config['dest_dir']),
                int(file.stat().st_mtime)
            )
            for file in flist
        ]

    def _get_datasource_state(self, rows):
        rlist = []
        for row in rows:
            rlist.append((
                Path(Template(self._config['dest_name']).substitute(**row)),
                int(row[self._config['mtime']])
            ))
        return rlist

    def _not_found_filesystem(self, filelist, rowlist):
        return list(set(rowlist) - set(filelist))

    def _not_found_datasource(self, filelist, rowlist):
        return list(set(filelist) - set(rowlist))
    
    def _file_names(self, filelist):
        return [ file[0] for file in filelist ]

    def _prune(self, filelist):
        for file in filelist:
            Path(self._config['dest_dir']).joinpath(file[0]).unlink()

    def _write(self, rows, to_write):
        for row in rows:
            file_name = Path(Template(self._config['dest_name']).substitute(**row))
            if file_name in self._file_names(to_write):
                with open(self._config['src']) as f:
                    substituted_template = Template(f.read()).substitute(**row)
                    mtime = int(row[self._config['mtime']])
                    destination = Path(self._config['dest_dir']).joinpath(file_name)
                    destination.write_text(substituted_template)
                    os.utime(destination, (mtime, mtime))

    def sync(self):
        ds_rows = self._datasource.rows
        filelist = self._get_filesystem_state()
        rowlist = self._get_datasource_state(ds_rows)
        to_delete = self._not_found_datasource(filelist, rowlist)
        to_write = self._not_found_filesystem(filelist, rowlist)

        if self._config['write']:
            self._write(ds_rows, to_write)
        if self._config.getboolean('prune'):
            self._prune(to_delete)

    @property
    def config(self):
        return self._config

    @property
    def datasource(self):
        return self._datasource
