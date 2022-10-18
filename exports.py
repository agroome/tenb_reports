import os
from urllib import response
import requests
import pandas as pd
import re
from dotenv import load_dotenv
from functools import partial
from smtp_email import SMTPMailer
from pprint import pprint
from tenable.io import TenableIO

class ScanNotFound(Exception):
    pass

load_dotenv()

access_key=os.getenv('TIO_ACCESS_KEY')
secret_key=os.getenv('TIO_SECRET_KEY')

tio_headers = {
    'X-ApiKeys': f'accessKey={access_key};secretKey={secret_key}',
    'Accept': 'application/json'
}
content_type = {
    "Content-Type": "application/json"
}


def match_field(item, field, pattern):
    return re.match(pattern, item.get(field, '')) is not None


class ScheduledExports:
    base_url = 'https://cloud.tenable.com/api/v3/exports/jobs/schedules'

    def list(self, name_regex=None):
        url = self.base_url
        response = requests.get(url, headers=tio_headers)
        print(f'list export schedules, pattern: "{name_regex}"')
        print(response.status_code, response.reason)
        schedules = response.json()['schedules']
        if name_regex is not None:
            matches_name = partial(match_field, field='name', pattern=name_regex)
            schedules = [s for s in schedules if matches_name(s)]
        
        return schedules

    def details(self, schedule):
        schedule_id = schedule['schedule_id']
        url = f'{self.base_url}/{schedule_id}'
        print(f'details: {schedule_id}')
        response = requests.get(url, headers=tio_headers)
        return response.json()

    def download(self, schedule):
        schedule_id = schedule['schedule_id']
        url = f'{self.base_url}/{schedule_id}/content'
        headers = tio_headers.copy()
        headers.update({'Accept': 'application/octet-stream'})
        response = requests.get(url, headers=headers)
        print(f'download {response.status_code}, {response.reason}')
        return response.text



# class ExportJobs: # beta
#     def get_jobs(self):
#         search_jobs = 'https://cloud.tenable.com/api/v3/exports/jobs/search'
#         response = requests.post(search_jobs, headers={**tio_headers, **content_type})
#         print(response.status_code, response.reason)
#         return response.json()


def find_scan(tio, name_regex, fmt='csv'):
    scans = list(filter(lambda s: re.match(name_regex, s['name']) is not None, tio.scans.list()))
    return scans and scans[0]


def export_scan(tio, scan, fmt='csv', scan_type=None):
    filename = f'{scan["name"]}.csv'
    print(scan)
    with open(filename, 'wb') as fobj:
        tio.scans.export(scan['id'], format=fmt, fobj=fobj)


def find_vuln_scan(tio, scan_name, fmt='csv'):
    for scan in tio.scans.list():
        if scan['name'] == scan_name:
            break
    else:
        raise ScanNotFound(f'scan not found: {scan_name}')
    return scan

    print("exporting scan: {scan_name}")
    export_scan(tio, scan, fmt='csv')


def main():
    schedules = ScheduledExports()
    name_pattern = 'Web Application Vulnerabilities'
    for schedule in schedules.list(name_regex=name_pattern):
        pprint(schedule)
        print('\n*********')
        print('DETAILS: ')
        details = schedules.details(schedule)
        pprint(details)
        print('\n\n***** CONTENT *****')
        filename = 'foo.csv'
        report_data = schedules.download(schedule)
        # with open(filename, 'w') as fobj:
        #     fobj.write(report_data)

        sender = 'agroome@tenable.com'
        subject = 'email test'
        body = 'Hello world'
        recipients = ','.join(['groome.andy@gmail.com', 'scooby@mysteryvan.io'])
        print(f'report_len: {len(report_data)}')
        reports = [
            {'filename': 'foo.csv', 'data': report_data}
        ]

        smtp = SMTPMailer('localhost', port=1025, use_ssl=False)
        smtp.send_email(sender, recipients, subject, body, reports=reports)


if __name__ == '__main__':
    main()

