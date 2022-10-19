from dotenv import load_dotenv
from tenable.io import TenableIO
import json
import pandas as pd


def export_compliance(file_path, **kwargs):
    tio = TenableIO()
    items = pd.json_normalize(tio.exports.compliance(**kwargs))
    items.to_csv(file_path)


def export_vulns(file_path, **kwargs):
    tio = TenableIO()
    items = pd.json_normalize(tio.exports.vulns(**kwargs))
    items.to_csv(file_path)
