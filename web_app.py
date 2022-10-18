#!/usr/bin/env python3
"""
    Installation: 
        # install the dotenv python module
        $ pip install python-dotenv

    API Keys:
        Store your API keys in a file called '.env', to load the keys into your environment.
        The file should look like this using your own API Keys:

        TIO_ACCESS_KEY=f2027e2bd4c06cf417c781becb377118b2cd3ab14e5d7cb571c92237efed42a2
        TIO_SECRET_KEY=968b18bd37c947dd1a98bb2a26022538104da9a81f92bd2d1c891d6bfaef2ff1

    Usage:
        This script will download results of a web application scan from Tenable.io. 

        # the script will export to CSV by default
        $ webapp_report.py --name <name_of_scan> --filename <name_of_export_file>
   
   This script uses the following API calls:

   Search the web app scan configurations:
   POST https://cloud.tenable.com/was/v2/configs/search
    search_payload = {
            "field": "configs.name",
            "operator": "eq",
            "value": args.name
    } if args.name else None
   link to doc: https://developer.tenable.com/reference/was-v2-config-search

   Search the scan history associated with the specified config_id
   POST https://cloud.tenable.com/was/v2/configs/{config_id}/scans/search
   link to doc: https://developer.tenable.com/reference/was-v2-scans-search

   Request an export for the specified scan_id
   PUT https://cloud.tenable.com/was/v2/scans/{scan_id}/report
   link to doc: https://developer.tenable.com/reference/was-v2-scans-export

   Download the exported scan:
   GET https://cloud.tenable.com/was/v2/scans/{scan_id}/report
   link to doc: https://developer.tenable.com/reference/was-v2-scans-download-export

   This script is an example only to illustrate use of the API.  Use care and at 
   your own risk if used in production environments. 
"""
import argparse
import os
import json
import requests
from tenable.io import TenableIO
from urllib.parse import quote
from dotenv import load_dotenv
from time import sleep

load_dotenv()

class WebApp:
    base_url = 'https://cloud.tenable.com/was/v2'
    def __init__(self, tio=None):
        self.tio = TenableIO() if tio is None else tio
        self.session = self.tio._session

    def list(self):
        for config in self.search_configs():
            yield config['name']
            
    def search_configs(self, limit=200, filters=None):
        total = 0
        offset = 0
        while True:
            url = f'{self.base_url}/configs/search?limit={limit}&offset={offset}'
            # url = f'https://cloud.tenable.com/was/v2/configs/search?limit={limit}&offset={offset}'
            result = self.session.post(url=url, json=filters)
            if result.ok: 
                results = result.json() 
                pagination = results['pagination']
                for item in results['items']:
                    yield item
                total += len(results['items'])
                offset += limit
                if total == pagination['total']:
                    break
            else:
                raise SystemExit(f'search_config: {result.reason}')

    def search_scans(self, config_id, filters=None):
        url = f'{self.base_url}/configs/{config_id}/scans/search'
        return self.session.post(url=url, json=filters)

    def request_and_download(self, scan_id, filename, content_type='text/csv'):
        export_url = f'{self.base_url}/scans/{scan_id}/report'
        headers = self.session.headers.copy()
        headers.update({"Content-Type": f"{content_type}"})

        while True:
            # request export and wait for completion
            result = self.session.put(export_url, headers=headers)
            # sleep if we are waiting for export, otherwise break
            if result.status_code == 202:
                sleep(2)
            else:
                break

        if result.status_code == 200:
            # successful export, download report
            result = self.session.get(export_url, headers=headers)
            if result.status_code == 200:
                print(f"downloading to {filename}")
                with open(filename, 'w', newline='') as fp:
                    if result.headers['Content-Type'] == 'application/json':
                        json.dump(result.json(), fp, indent=4)
                    else:
                        fp.write(result.text)

        else:
            raise SystemExit(f'download report: error: {result.status_code}, reason: {result.reason}')


    def _request_and_download(self, scan_id, filename, format='csv'):
        with open(filename, 'wb') as fobj:
            self.tio.scans.export(scan_id, fobj=fobj, format=format, scan_type='web-app')


    def download_scan(self, name, filename, format='csv'):
        # create a filter payload if --name is specified
        search_payload = {
                "field": "configs.name",
                "operator": "eq",
                "value": name
        } if name else None

        if format == 'csv':
            content_type = 'text/csv' 
        elif format == 'json':
            content_type = 'application/json' 

        # search for the config with 'name', take the first result
        scan_configs = list(self.search_configs(filters=search_payload))
        config = scan_configs and scan_configs[0]
        if config:
            # get the scans for this config
            scans = self.search_scans(config['config_id']).json()['items']

            # if there are scans, download the most recent
            scan = scans and scans[0]
            if scan:
                self.request_and_download(scan['scan_id'], filename=filename, content_type=content_type)
                # self._request_and_download(scan['scan_id'], filename=filename, format='csv')
            else:
                print(f'no scan results to export for {config["name"]}')
        else:
            print(f'no matching scan: {name}')

        
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', type=str, required=False, help='name of scan to export')
    parser.add_argument('-f', '--filename', type=str, required=False, help='write results to this file')
    args = parser.parse_args()

    name = args.name or 'Gruyere PCI Scan'
    filename = args.filename or 'gruyere1.csv'

    was = WebApp()
    was.download_scan(name, filename)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        raise SystemExit(repr(e))