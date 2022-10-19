#!/usr/bin/env python3

import os #For environment
import requests #for API interaction
import json #API returns JSON, usually

bearer = os.getenv('TCS_BEARER_TOKEN', '')
headers = {
    "accept": "application/json",
    "authorization": f"Bearer {bearer}"
}
offset = 0 #Record offset for API
limit = 1000 #Record limit for API

base_url = 'https://cloud.tenable.com/cns/api/v1'

def get_projects():
    url = f"{base_url}/projects?offset={str(offset)}&limit={str(limit)}"
    response = requests.get(url, headers=headers)
    #TODO: Error checking logic, e.g. HTTP 403/404

    # projects=[]
    # project_names={}

    projects=json.loads(response.text)
    # for response in responses:
        # projects.append(response.get('id'))
        # project_names[response.get('id')]=response.get('name')
    return projects


def download_project_violations(project, target_folder):
    url = f"{base_url}/violations?project_id={project['id']}&csv_format=true"
    file_path = os.path.join(target_folder, f"{project['name']}.csv")

    response = requests.get(url, headers=headers)
    with open(file_path, 'w') as f:
        f.write(response.text)


def download_projects(project_names, target_folder):
    projects = {p['name']: p for p in get_projects()}
    for project_name in project_names:
        project = projects[project_name]
        download_project_violations(project, target_folder)


def main():
    import pathlib
    project_names = ['AWS CSPM', 'AWS Pipeline']
    target_folder = pathlib.Path('./reports/test')
    target_folder.mkdir(parents=True, exist_ok=True)
    download_projects(project_names, target_folder)


if __name__ == '__main__':
    main()