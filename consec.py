import pandas as pd
import pathlib
from tenable.io import TenableIO 
import logging


class FileWriter:
    def __init__(self, output_folder, create_folder=True, file_type='csv'):
        self.output_folder = pathlib.Path(output_folder)
        self.create_folder = create_folder

    def write(self, filename, records, fieldnames=None):
        file_path = self.output_folder / filename
        logging.info(f'writing to: {file_path}')
        if self.create_folder:
            self.output_folder.mkdir(parents=True, exist_ok=True)
        if fieldnames is None:
            df = pd.DataFrame.from_records(records)
        else:
            df = pd.DataFrame.from_records(records)[fieldnames]

        df.to_csv(file_path, index=False) 


class ConSec:
    def __init__(self) -> None:
        self.tio = TenableIO()

    def records(self):
        for image in self.tio.cs.images.list():
            repo_name, name, tag = image.get('repoName'), image.get('name'), image.get('tag')
            report = self.tio.cs.reports.report(repo_name, name, tag)
            for finding in report['findings']:
                record = finding['nvdFinding']
                record['packages'] = ','.join([f'{p.name}:{p.version}' for p in finding['packages']])
                record['repo'] = repo_name
                record['name'] = name
                record['tag'] = tag
                record['image'] = f'{repo_name}/{name}:{tag}' if tag else f'{repo_name}/{name}'
                record['docker_image_id'] = report['docker_image_id']
                record['created_at'] = report['created_at']
                record['updated_at'] = report['updated_at']
                yield record


def main():

    output_folder = './reports'
    output_file = 'consecreport.csv'

    report_columns = [
        'image', 'repo', 'name', 'tag', 'created_at', 'updated_at', 
        'packages', 'remediation', 'description', 
        'published_date', 'modified_date', 'cvss_score', 'cvss_vector',
        'access_vector', 'access_complexity', 'auth', 'availability_impact', 'confidentiality_impact',
        'references', 'docker_image_id',
    ]
    
    writer = FileWriter(output_folder)
    writer.write(output_file, ConSec().records(), report_columns)

if __name__ == '__main__':
    main()
