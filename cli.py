import pathlib
import click
import logging
import textwrap
import yaml

from tio_exports import export_compliance, export_vulns

import web_app 
import vmscan
import report

from config import Config 

log_file = 'tenb_reports.log'
logging.basicConfig(
    filename=log_file,
    format='%(asctime)s [%(funcName)s] %(levelname)s: %(message)s', 
    datefmt='%m/%d/%Y %H:%M:%S', 
    level=logging.INFO)

logging.info('starting cli')

default_config = Config.root_dir / 'report_config.yaml'
default_report_folder = Config.root_dir / 'reports'
default_env_file = Config.root_dir / '.env'

resources = {
    'was': web_app.WebApp(),
    'vmscan': vmscan.Scan()
}

@click.group()
def cli():
    logging.info('starting')

@cli.command('run-report')
@click.option('--config', type=click.File('r'), required=True, 
    help='Location of report configuration file')
@click.option('--output_folder', type=click.Path(exists=True, path_type=pathlib.Path), default=default_report_folder, 
    help='Reports are written to this folder')
@click.option('--send-email', default=False,
    help='When true will send email after downloading files')
def run_report(config, output_folder, send_email):
    click.echo(f'reading from {config.name}')
    report_directives = yaml.safe_load(config)
    click.echo(f'writing to {output_folder}')

    report_meta = report.download(report_directives, output_folder)
    if send_email:
        click.echo(f'sending email')
        report.email(report_meta)


@cli.command(name='list')
@click.argument('resource', type=click.Choice(list(resources)))
def list_(resource):
    print(f"list {resource}")
    obj = resources[resource]
    for output_str in obj.list():
        click.echo(output_str)


@cli.command(name='download')
@click.argument('resource', type=click.Choice(['findings', 'vmscan', 'was']))
@click.option('-n', '--name')
@click.option('-f', '--filename')
def download(resource, name, filename):
    click.echo(f'downloading {name} to {filename}')
    obj = resources[resource]
    obj.download_scan(name, filename)


@cli.command('export')
@click.argument('resource', type=click.Choice(['vulns', 'compliance']))
@click.option('--output-file', type=click.Path(path_type=pathlib.Path), required=True)
def tio_export(resource, output_file):
    click.echo(f'exporting {resource} to {output_file}')
    if resource == 'vulns':
        export_vulns(output_file)
    if resource == 'compliance':
        export_compliance(output_file)
        

@click.command('configure')
@click.option('--env-file', 
    type=click.Path(path_type=pathlib.Path), default=default_env_file, help='Create an environment file'
)
def configure(env_file): 
    tio_access_key = click.prompt('Tenable.io access key', hide_input=True)
    tio_secret_key = click.prompt('Tenable.io secret key', hide_input=True)
    tsc_bearer_token = click.prompt('Tenable.cs bearer token', hide_input=True) 
    smtp_server = click.prompt('SMTP server')
    smtp_port = click.prompt('SMTP port', type=int, default=587)
    smtp_password = click.prompt('SMTP password', default='', hide_input=True)
    smtp_use_ssl = click.prompt('SMTP use_ssl', default=True)
    report_folder = click.prompt('Report folder', default='./reports')

    output = f'''
        TIO_ACCESS_KEY={tio_access_key}
        TIO_SECRET_KEY={tio_secret_key}
        TCS_BEARER_TOKEN={tsc_bearer_token}
        REPORT_FOLDER={report_folder}
        SMTP_SERVER={smtp_server}
        SMTP_PORT={smtp_port}
        SMTP_PASSWORD={smtp_password}
        SMTP_USE_SSL={'true' if smtp_use_ssl else 'false'}
    '''
    click.echo(f'creating file: {env_file.absolute()}') 
    if not env_file.exists() or click.confirm(f'overwrite {env_file.absolute()}'):
        with open(env_file, 'w') as f:
            f.write(textwrap.dedent(output))


if __name__ == '__main__':
    cli()
