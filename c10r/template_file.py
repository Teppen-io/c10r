import os
from string import Template


class TemplateFile:
    def __init__(self, f, metadata, config):
        self._file = f
        self._metadata = metadata
        self._config = config
        self._mtime = int(self._metadata[self._config['mtime']])
        self._template = Template(open(self._config['src']).read()).substitute(**metadata)

    def sync(self):
        if not self.synced:
            self._file.write_text(self._template)
            os.utime(self._file, (self._mtime, self._mtime))

    @property
    def synced(self):
        return self._file.exists() and int(self._file.stat().st_mtime) == self._mtime
