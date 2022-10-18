import csv
import arrow 
import yaml

from dotenv import load_dotenv
from tenable.io import TenableIO
from pprint import pprint

load_dotenv()


def get_group_members(tio: TenableIO, group_name: str) -> list:
    """return info for each user in a given group"""
    print(f"searching for {group_name}")
    groups = tio.groups.list()
    for group in groups:
        if group['name'] == group_name:
            break
    else:
        raise ValueError(f'group not found {group_name}')
    user_list = tio.groups.list_users(group['id'])
    return [user for user in user_list if user['enabled']]



def main():
    tio = TenableIO()
    project_name = 'AWS CSPM'

    users = get_group_members(tio, project_name)
    for user in users:
        print('{username} {email}'.format(**user))


if __name__ == '__main__':
    main()
