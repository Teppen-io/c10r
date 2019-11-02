import os
from string import Template


class TemplateFile:
    def __init__(self, f, metadata, template_path):
        self._file = f
        self._metadata = metadata
        self._template = Template(open(template_path).read()).substitute(**metadata)

    def sync(self):
        if not self.synced:
            self._file.write_text(self._template)
            os.utime(self._file, (int(self._metadata['mtime']), int(self._metadata['mtime'])))

    @property
    def synced(self):
        return self._file.exists() and int(self._file.stat().st_mtime) == int(self._metadata['mtime'])
