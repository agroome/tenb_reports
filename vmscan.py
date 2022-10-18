import logging
import re
from tenable.io import TenableIO


class Scan:
    fmt = '{name:40} {status:12} {id:12}'
    def __init__(self, tio=None):
        self.tio = TenableIO() if tio is None else tio

    def list(self, fmt=None):
        fmt = self.fmt if fmt is None else fmt
        for scan in self.tio.scans.list():
            yield fmt.format(**scan)

    def download_scan(self, name, filename, format='csv'):
        logging.info('downloading %s', name)
        scans = [scan for scan in self.tio.scans.list() if scan['name'] == name]
        try:
            scan = scans[0]
        except IndexError as e:
            raise ValueError(f'scan not found: {name}')

        with open(filename, 'wb') as fobj:
            self.tio.scans.export(scan['id'], fobj=fobj, format=format)

