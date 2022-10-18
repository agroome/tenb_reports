import logging
import os
import pandas as pd
import pathlib
import yaml
from config import Config
from pprint import pprint

print(f"{__file__}")
yaml_config = 'config.yaml'


def read_config(filename):
    with open(filename) as fobj:
        distribution = yaml.safe_load(fobj.read())
    return distribution


def create_distribution(report_path, member_dict):
    distribution = []
    print(f'building for {report_path.absolute()}') 
    for file_path in report_path.iterdir(): 
        print(f'file: {file_path.name}') 
        if file_path.suffix != '.csv':
            break
        project_name = file_path.stem
        print(f"**** {project_name} ***")
        print(f"    {file_path.absolute()}")
        try:
            addresses = ','.join(member_dict[project_name])
        except KeyError as e:
            logging.warn(f'distribution not found for {project_name}')

        distribution.append({
            'to': addresses, 
            'attachment': file_path}
        )

    return distribution
            


class Mailer:
    def __init__(self, report_path, distribution) -> None:
        self.report_path = report_path
        self.distribution = distribution
        self.emails = self._build()

    def _build(self):
        emails = []
        print(f'building for {self.report_path.absolute()}')
        for file_path in self.report_path.iterdir():
            print(f'file: {file_path.name}')
            if file_path.suffix != '.csv':
                break
            project_name = file_path.stem
            print(f"**** {project_name} ***")
            print(f"    {file_path.absolute()}")
            try:
                addresses = ','.join(self.distribution[project_name])
                emails.append({'to': addresses, 'attachment': file_path})
            except KeyError as e:
                logging.warn(f'distribution not found for {project_name}')
        return emails
            

# def email_cspm(report_path, distribution):
#     print(f'reporting from dir: {report_path.absolute()}')
#     for file_path in report_path.iterdir():
#         project_name = file_path.stem
#         print(f"**** {project_name} ***")
#         print(f"    {file_path.absolute()}")
#         try:
#             addresses = ','.join(distribution[project_name])
#         except KeyError as e:
#             raise ValueError(f'email distribuiton not found for project: {project_name}')

#         # print(f"To: {addresses}")


# def run_test():
#     report_path = Config.report_folder / Config.cspm_reports 
#     distribution = read_config(yaml_config)

#     mailer = Mailer(report_path, distribution)
#     for email in mailer.emails:
#         pprint(email)


# if __name__ == '__main__':
#     run_test()

