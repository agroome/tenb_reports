import dotenv
import os
import pathlib

dotenv.load_dotenv()

ROOT_DIR = pathlib.Path('.')

class Config:
    root_dir = ROOT_DIR
    report_folder = pathlib.Path(os.getenv('REPORT_FOLDER', ''))
    cspm_reports = 'cspm'

    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = int(os.getenv('SMTP_PORT', 587))

class CSPMConfig:
    report_path = Config.report_folder  / 'cspm'