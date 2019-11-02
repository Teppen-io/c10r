import subprocess
from pathlib import Path
from string import Template
from template_file import TemplateFile


class TemplateResource:
    def __init__(self, template_config, backend, backend_config):
        self._config = template_config
        self._datasource = self._get_backend(backend, backend_config)

    def _get_backend(self, backend, backend_config):
        if backend == 'mysql':
            from backends.mysql_ import Datasource
        elif backend == 'sqlite3':
            from backends.sqlite3_ import Datasource
        return Datasource(self._config['query'], **backend_config)

    def _get_filesystem_state(self):
        return list(Path(self._config['dest']).parent.glob('*'))

    def _get_datasource_state(self):
        return {
            Path(Template(self._config['dest']).substitute(**row)): row
            for row in self._datasource.rows
        }

    def sync(self):
        if self._config.getboolean('prune') or self._config.getboolean('write'):
            ds_state = self._get_datasource_state()

            if self._config['before']:
                subprocess.run(self._config['before'].split(' '))
            if self._config['write']:
                for f, metadata in ds_state:
                    TemplateFile(f, metadata, self._config['src']).sync()
            if self._config.getboolean('prune'):
                for f in self._get_filesystem_state():
                    if f not in ds_state.keys():
                        f.unlink()
            if self._config['after']:
                subprocess.run(self._config['after'].split(' '))

    @property
    def config(self):
        return self._config

    @property
    def datasource(self):
        return self._datasource
