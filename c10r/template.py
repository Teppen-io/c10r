import os
import subprocess
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

    def _get_filesystem_state(self, managed_dirs):
        flist = []
        for managed_dir in managed_dirs:
            files = list(Path(managed_dir).glob('*'))
            flist += [
                (
                    f,
                    int(f.stat().st_mtime)
                )
                for f in files
            ]
        return flist

    def _get_datasource_state(self, rows):
        flist, managed_dirs = [], []
        for row in rows:
            dest = Path(Template(self._config['dest']).substitute(**row))
            managed_dirs.append(dest.parent)
            flist.append(
                (
                    dest,
                    int(row[self._config['mtime']])
                )
            )
        return flist, managed_dirs
    
    def _file_names(self, filelist):
        return [ f[0] for f in filelist ]

    def _prune(self, filelist):
        for f in self._file_names(filelist):
            Path(f).unlink()

    def _write(self, rows, to_write):
        for row in rows:
            dest = Path(Template(self._config['dest']).substitute(**row))
            if dest in self._file_names(to_write):
                dest.parent.mkdir(parents=True, exist_ok=True)
                with open(self._config['src']) as f:
                    substituted_template = Template(f.read()).substitute(**row)
                    mtime = int(row[self._config['mtime']])
                    dest.write_text(substituted_template)
                    os.utime(dest, (mtime, mtime))

    def _state_difference(self, ds_rows):
        rowlist, managed_dirs = self._get_datasource_state(ds_rows)
        filelist = self._get_filesystem_state(managed_dirs)
        return [
            list(set(filelist) - set(rowlist)),
            list(set(rowlist) - set(filelist))
        ]

    def sync(self):
        ds_rows = self._datasource.rows
        to_delete, to_write = self._state_difference(ds_rows)

        if self._config['before']:
            subprocess.run(self._config['before'].split(' '))
        if self._config['write']:
            self._write(ds_rows, to_write)
        if self._config.getboolean('prune'):
            self._prune(to_delete)
        if self._config['after']:
            subprocess.run(self._config['after'].split(' '))

    @property
    def config(self):
        return self._config

    @property
    def datasource(self):
        return self._datasource
