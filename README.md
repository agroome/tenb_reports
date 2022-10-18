# tenb_report_distribution

## Overview
Example use of various APIs to export and download information from Tenable.io, Tenable.cs and Tenable.was.

This offered under a MIT license and is not officially supported or provided by Tenable.

## Installation
Clone the repository and setup a virutal environment.

```
# clone the repo
$ git clone https://github.com/agroome/tenb_reports.git

# setup a virtual environment in the project folder
$ cd ./tenb_reports
$ python3 -m venv ./venv

# activate the virtual environment
$ source activate ./venv/bin/activate
```

Using your own API keys and TCS bearer token, create a file in the project directory called .env with the following format:

```
TIO_ACCESS_KEY=d00f0d...
TIO_SECRET_KEY=30061b...
TCS_API_TOKEN=8474bb6...
SMTP_SERVER=localhost
SMTP_PORT=1025
```



## Usage

```
(venv)$ python cli.py --help
(venv)$ python cli.py [CMD] --help
```

Sample configuration for run-reports command located in report_config.yaml file.



... more to come
