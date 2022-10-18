from email.policy import default
import pathlib
import click
import logging
import yaml

import web_app 
import vmscan
import reports

from config import Config 

logging.basicConfig(
    # filename='cli.log',
    format='%(asctime)s [%(funcName)s] %(levelname)s: %(message)s', 
    datefmt='%m/%d/%Y %H:%M:%S', 
    level=logging.INFO)


default_config = Config.root_dir / 'report_config.yaml'
default_report_folder = Config.root_dir / 'reports'

resources = {
    'was': web_app.WebApp(),
    'vmscan': vmscan.Scan()
}

@click.group()
def cli():
    logging.info('starting')

@cli.command('run-report')
@click.option('--config', 
    type=click.File('r'), default=default_config, help='Location of report configuration file'
)
@click.option('--output_folder', 
    type=click.Path(exists=True, path_type=pathlib.Path), default=default_report_folder, 
    help='Reports will be generated in this folder'
)
@click.option('--send-email', default=False,
    help='When true will send email after downloading files'
)
def run_report(config, output_folder, send_email):
    click.echo(f'reading from {config.name}')
    report_directives = yaml.safe_load(config)
    click.echo(f'writing to {output_folder}')

    report_meta = reports.download(report_directives, output_folder)
    if send_email:
        click.echo(f'sending email')
        reports.email(report_meta)


@cli.command(name='list')
@click.argument('resource', type=click.Choice(list(resources)))
def list_(resource):
    print(f"list {resource}")
    obj = resources[resource]
    for output_str in obj.list():
        click.echo(output_str)


@cli.command(name='download')
@click.argument('resource')
@click.option('-n', '--name')
@click.option('-f', '--filename')
def download(resource, name, filename):
    click.echo(f'downloading {name} to {filename}')
    obj = resources[resource]
    obj.download_scan(name, filename)

if __name__ == '__main__':
   cli()
