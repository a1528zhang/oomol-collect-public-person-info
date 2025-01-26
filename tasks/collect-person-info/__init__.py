from os import path
from maigret.report import generate_report_context, save_pdf_report
from oocana import Context
import logging
import maigret
from maigret.sites import MaigretDatabase

MAIGRET_DB_FILE = 'data.json' # wget https://raw.githubusercontent.com/soxoj/maigret/main/maigret/resources/data.json
COOKIES_FILE = "cookies.txt"  # wget https://raw.githubusercontent.com/soxoj/maigret/main/cookies.txt
id_type = "username"
USERNAME_REGEXP = r'^[a-zA-Z0-9-_\.]{5,}$'
ADMIN_USERNAME = '@soxoj'

# top popular sites from the Maigret database
TOP_SITES_COUNT = 1500
# Maigret HTTP requests timeout
TIMEOUT = 30

def setup_logger(log_level, name):
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    return logger

async def main(params: dict, context: Context):
    username = params["username"]
    report_dir = params['report_dir']

    logger = context.logger

    db = MaigretDatabase().load_from_path(path.join(path.dirname(__file__), MAIGRET_DB_FILE))

    sites = db.ranked_sites_dict(top=TOP_SITES_COUNT)

    general_results = []

    results = await maigret.search(username=username,
                                    site_dict=sites,
                                    timeout=TIMEOUT,
                                    logger=logger,
                                    id_type=id_type,
                                    cookies=path.join(path.dirname(__file__), COOKIES_FILE),
                                    )
    general_results.append((username, id_type, results))
    report_context = generate_report_context(general_results)

    report_filepath_tpl = path.join(report_dir, 'report_{username}{postfix}')

    filename = report_filepath_tpl.format(username=username, postfix='.pdf')
    save_pdf_report(filename, report_context)

    return { "report_path": report_filepath_tpl }