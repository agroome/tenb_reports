import dotenv
import os
import pathlib

dotenv.load_dotenv()

class Config:
    root_dir = pathlib.Path('.')
    report_folder = pathlib.Path('./reports')

    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = int(os.getenv('SMTP_PORT', 587))
