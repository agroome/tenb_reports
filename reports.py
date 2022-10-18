import yaml
from pprint import pprint
import os
import pathlib
import time
import consec
import cspm
import v2export
from smtp_email import SMTPMailer

app_dir = pathlib.Path('.')


time_fmt = '%Y:%m:%d-%H:%M:%S'


def download(report_directives, output_folder):
    # with open(config_path) as f:
    #     report_definitions = yaml.safe_load(f)['REPORTS']
    print(f'output: {output_folder}')
    for report in report_directives['REPORTS']: 
        report_folder =  output_folder / report['name']
        report_folder.mkdir(parents=True, exist_ok=True, mode=0o755)

        report['attachments'] = []
        
        if 'tio_tags' in report:
            # convert list of single item dicts to a list of tuple
            tag_filter = [next(iter(tag.items())) for tag in report['tio_tags']]
            folder_path = report_folder 
            folder_path.mkdir(parents=True, exist_ok=True, mode=0o755)
            file_path = folder_path / 'vulns.csv' 
            print(f'exporting vulns to {file_path.absolute()}')
            v2export.export_vulns(file_path, tags=tag_filter)
            report['attachments'].append(file_path.absolute())

        if 'repositories' in report:
            folder_path = report_folder / 'consec' 
            folder_path.mkdir(parents=True, exist_ok=True, mode=0o755)
            consec.run_reports(folder_path)

        if 'cspm_projects' in report: 
            target_folder = report_folder / 'cspm' 
            target_folder.mkdir(parents=True, exist_ok=True, mode=0o755)
            cspm.download_projects(report['cspm_projects'], target_folder)
            for file_path in target_folder.glob('*.csv'):
                report['attachments'].append(file_path.absolute())
            
        return report_directives['REPORTS']


def email(report_definitions):
    mailer = SMTPMailer(server='localhost', port=1025, use_ssl=False)
    for report in report_definitions:
        print(f"sending email to {report['to']}")
        print(f'attachments: {report["attachments"]}')
        mailer.send_email(
            sender=report['from'], recipients=report['to'],
            subject=report.get('subject', ''), body=report.get('body'),
            attachments=report['attachments']
        )

def main():
    from smtp_email import SMTPMailer

    file_path = app_dir / 'test.yaml'
    email(download(config_path=file_path))



if __name__ == '__main__':
    main()
