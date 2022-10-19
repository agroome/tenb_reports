# tenb_report_distribution

## Overview
Example use of various APIs to export and download information from Tenable.io, Tenable.cs and Tenable.was.


Generate reports based on yaml configuration command located in report_config.yaml file.
'''
REPORTS:
    name: new_report {date}
-   date_fmt: '%Y:%m:%d-%H:%M%S'

    from: sender@example.com
    subject: my report subject
    to: 
    - person_19@example.com 
    - person_4@example.com 
    - person_21@example.com
    body: 'this is a short body'

    tio_tags: 
    - Business Unit: Sales
    
    cspm_projects:
    - AWS CSPM
    - AWS Pipeline
'''

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
TCS_BEARER_TOKEN=8474bb6...
SMTP_SERVER=localhost
SMTP_PORT=1025
```



## Usage

```
(venv)$ python cli.py --help
(venv)$ python cli.py [CMD] --help
```


## Testing email with a debuging smtp server
You can test email functionality by settup up a debuging server that runs on localhost:1025.

Start the email server in a terminal window with the following command. 

```
python3 -m smtpd -c DebuggingServer -n localhost:1025
```

Initialize the mailer with the following parameters when sending to the local server:
```
SMTP_SERVER=localhost
SMTP_PORT=1025
SMTP_USE_SSL=false
```
... more to come
