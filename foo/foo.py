import logging
import foo1

logfile = 'tenb_reports.log'

# create logger for the app
logger = logging.getLogger('tenb_reports')
logger.setLevel(logging.INFO)
fh = logging.FileHandler(logfile)
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
logger = logging.getLogger('tenb_reports')
fh = logging.FileHandler(logfile)
logger.addHandler(fh)

logger.info("hello world")