from email.policy import default
import click
import logging
import yaml

import web_app 
import vmscan
import email_util
import smtp_email
import config as cfg

logging.basicConfig(
    # filename='cli.log',
    format='%(asctime)s [%(funcName)s] %(levelname)s: %(message)s', 
    datefmt='%m/%d/%Y %H:%M:%S', 
    level=logging.INFO)


def read_config(filename):
    with open(filename) as fobj:
        distribution = yaml.safe_load(fobj.read())
    return distribution


resources = {
    'was': web_app.WebApp(),
    'vmscan': vmscan.Scan()
}

@click.group()
def cli():
    logging.info('starting')


@cli.group('cspm')
def cspm():
    """"""

@cspm.command('download')
def download_cspm():
    logging.info("download cspm")


@cspm.command('distribute')
@click.option('--report-folder', default='./reports')
def distribute_cspm(report_folder):
    logging.info("distribute cspm")
    report_path = cfg.Config.report_folder / cfg.Config.cspm_reports 
    yaml_config = cfg.Config.root_dir / 'config.yaml'
    address_table = read_config(yaml_config)




def email_reports():
    smtp_server = 'localhost'
    smtp_port = 1025

    mailer = smtp_email.SMTPMailer(smtp_server, port=smtp_port, use_ssl=False)


def process_report_folder(report_folder, address_book, mailer):
    report_meta = {
        'subject': "CSPM report",
        'body': "This is an email report from Tenable CSPM",
        'sender': "my@gmail.com"
    }
    subject = "CSPM report",
    body = "This is an email report from Tenable CSPM",
    sender = "my@gmail.com"

    distribution: list = email_util.create_distribution(report_folder, address_book)


    for report in distribution.emails:
        click.echo(report)
        files = [report['attachment']]

        mailer.send_email(sender, report['to'], subject, body, attachments=files)



@cli.group('scans')
def scans():
    """"""

@scans.command('list')
def list_scans():
    click.echo("listing scans")

@cli.command(name='list')
@click.argument('resource')
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
