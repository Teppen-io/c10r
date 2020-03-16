import subprocess
from pathlib import Path
from string import Template
from template_file import TemplateFile


class TemplateResource:
    def __init__(self, template_config, backend, backend_config):
        self._config = template_config['template']
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

    def _create_template_files(self, fs_state, ds_state):
        template_files = [TemplateFile(tf, self._config, row) for tf, row in ds_state.items()]
        for fpath in fs_state:
            if fpath not in ds_state.keys():
                template_files.append(TemplateFile(fpath, self._config))
        return template_files

    @staticmethod
    def _filesystem_synced(template_files):
        return all([tf.synced for tf in template_files])

    @property
    def _template_files(self):
        return self._create_template_files(
            self._get_filesystem_state(),
            self._get_datasource_state()
        )

    def sync(self):
        if self._config.getboolean('prune') or self._config.getboolean('write'):
            template_files = self._template_files

            if not self._filesystem_synced(template_files):
                if self._config['before']:
                    subprocess.run(self._config['before'].split(' '))
                for tf in template_files:
                    tf.sync()
                if self._config['after']:
                    subprocess.run(self._config['after'].split(' '))
