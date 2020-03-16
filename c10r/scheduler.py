#!/usr/bin/env python3
import time
import sched
import configparser
from pathlib import Path
from template_resource import TemplateResource


CONFIG_PATH = Path.joinpath(Path(__file__).parent.resolve(), '../c10r.cfg')
CONFD_PATH = Path.joinpath(Path(__file__).parent.resolve(), '../conf.d')


class Scheduler:
    def __init__(self, **kwargs):
        self._config = self._read_config(kwargs.get('config', CONFIG_PATH))
        self._scheduler = sched.scheduler(time.time, time.sleep)
        self._template_resources = self._parse_template_configs(kwargs.get('confd', CONFD_PATH))

    def _read_config(self, location):
        config = configparser.ConfigParser(interpolation=None)
        with open(Path(location).expanduser()) as f:
            config.read_file(f)
        return config

    def _parse_template_configs(self, location):
        template_resources = []
        for template_config in list(Path(location).glob('*.cfg')):
            parsed_config = self._read_config(template_config)
            template_resource = TemplateResource(
                parsed_config,
                self._config['scheduler']['backend'],
                self._config[self._config['scheduler']['backend']]
            )
            template_resources.append(template_resource)
        return template_resources

    def _run_forever(self):
        for template_resource in self._template_resources:
            template_resource.sync()
        self._scheduler.enter(int(self._config['scheduler']['interval']), 1, self._run_forever)

    def run(self):
        self._scheduler.enter(int(self._config['scheduler']['interval']), 1, self._run_forever)
        self._scheduler.run()

    @property
    def config(self):
        return self._config

    @property
    def template_resources(self):
        return self._template_resources


def main():
    Scheduler().run()


if __name__ == "__main__":
    main()
