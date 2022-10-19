import os #For environment
import requests #for API interaction
import json #API returns JSON, usually
import pandas as pd
from config import Config

import logging
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)

accessKey = os.getenv('TIO_ACCESS_KEY')
secretKey = os.getenv('TIO_SECRET_KEY')

base_url = "https://cloud.tenable.com/container-security/api/v2"

headers = {
    "accept": "application/json",
    "X-ApiKeys": "accessKey=" + accessKey + ";secretKey=" + secretKey
}

def parse_report(item):
    repo_name = item.get('repoName')
    name = item.get('name')
    tag = item.get('tag')
    image_name = f'{repo_name}/{name}:{tag}'
    report_url = f"{base_url}/reports/{item.get('repoName')}/{item.get('name')}/{item.get('tag')}"
    responses= requests.get(report_url, headers=headers)
    response = json.loads(responses.text)
    for finding in response['findings']:
        record = finding['nvdFinding']
        package = finding['packages'][0]
        record['repo'] = repo_name
        record['image'] = image_name
        record['docker_image_id'] = response['docker_image_id']
        record['created_at'] = response['created_at']
        record['updated_at'] = response['updated_at']
        record['package_name'] = package['name']
        record['package_version'] = package['version']
        record['package_type'] = package['type']
        yield record


report_columns = [
    'repo', 'image', 'created_at', 'updated_at', 'package_name', 'package_version', 'package_type',
    'remediation', 'description', 'published_date', 'modified_date', 'cvss_score', 'cvss_vector',
    'access_vector', 'access_complexity', 'auth', 'availability_impact', 'confidentiality_impact',
    'integrity_impact', 'cwe', 'cpe', 'references', 'docker_image_id'
]

def image_report_filepath(image):
    tag_str = f':{image["tag"]}' if 'tag' in image else ''
    return f'{image.get("repoName")}__{image.get("name")}{tag_str}.csv'

def run_reports(target_folder):
    images_url = f'{base_url}/images'
    logging.info('opening images url %s', images_url)
    response = requests.get(images_url, headers=headers)
    images = json.loads(response.text)['items']
    for image in images:
        file_path = os.path.join(target_folder, image_report_filepath(image))
        logging.info('writing to file %s', file_path)

        df = pd.DataFrame.from_records(parse_report(image), index='cve')
        df[report_columns].to_csv(file_path)

if __name__ == '__main__':
    run_reports('./reports/consec')

