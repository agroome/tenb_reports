from dotenv import load_dotenv
from tenable.io import TenableIO
from config import Config
import json
import pandas as pd


def export_vulns(file_path, **kwargs):
    tio = TenableIO()
    vulns = pd.json_normalize(tio.exports.vulns(**kwargs))
    vulns.to_csv(file_path)



def main():
    import pathlib
    
    project_name = 'AWS CSPM'
    folder_path = Config.report_folder / 'exports' / project_name
    folder_path.mkdir(parents=True, exist_ok=True, mode=0o755)
    file_path = folder_path / 'vuln_export.csv'
    print(f'exporting {project_name} to {file_path.absolute()}')
    export_vulns(file_path, tags=[('Project', project_name)])


if __name__ == '__main__':
    main()