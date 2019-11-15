import os
from string import Template


class TemplateFile:
    def __init__(self, fpath, config, row={}):
        self._file = fpath
        self._row = row
        self._config = config
        self._template = Template(open(self._config['src']).read()).substitute(**row)

    @property
    def _prune_required(self):
        return self._config['prune'] and not self._row

    @property
    def _write_required(self):
        if self._config['write']:
            return any([
                not self._file.exists(),
                self._file.exists() and not int(self._file.stat().st_mtime) == self._mtime
            ])

    def _write(self):
        if self._write_required:
            self._file.write_text(self._template)
            mtime = int(self._row.get(self._config['mtime']))
            os.utime(self._file, (mtime, mtime))

    def _prune(self):
        if self._prune_required:
            self._file.unlink()

    def sync(self):
        self._prune()
        self._write()

    @property
    def synced(self):
        return not self._prune_required and not self._write_required
