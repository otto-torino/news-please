import json
import logging
import logging.handlers
import os
from concurrent.futures import ThreadPoolExecutor

import requests

logger = logging.getLogger(__name__)
handler = logging.handlers.WatchedFileHandler(
    os.environ.get("LOGFILE", ".pyfeedchecker.log"))
formatter = logging.Formatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
logger.setLevel(os.environ.get("LOGLEVEL", "INFO"))
logger.addHandler(handler)


class Checker():
    def __init__(self, input, output, request_timeout=10, timeout_is_bad=True):
        self.json_path = input
        self.output_path = output
        self.request_timeout = request_timeout
        self.timeout_is_bad = timeout_is_bad
        self.total = 0
        self.totals = {}
        self.bad_results = 0
        self.corrected_json = []

    def fetch_site(self, site):
        print('Checking %s' % site.get('url'))
        try:
            response = requests.head(
                site.get('url'),
                allow_redirects=True,
                timeout=self.request_timeout)
            # log stuff
            logger.info('Result for %s' % site.get('url'))
            logger.info('Final URL: %s' % response.url)
            logger.info(
                'Elapsed Time: %.2f' % response.elapsed.total_seconds())
            logger.info('Status Code: %d' % response.status_code)
            # keep only 200 <= codes < 400
            if (response.status_code < 400):
                self.corrected_json.append(site)
            # for summary info
            self.total += 1
            if self.totals.get(response.status_code):
                self.totals[response.status_code] += 1
            else:
                self.totals[response.status_code] = 1
            if response.status_code >= 400:
                self.bad_results += 1
        except Exception as e:
            logger.info('Result for %s' % site.get('url'))
            logger.info('Timeout %s' % e)
            logger.info('Considered %s result' %
                        'BAD' if self.timeout_is_bad else 'GOOD')
            if self.totals.get(408):
                self.totals[408] += 1
            else:
                self.totals[408] = 1
            if self.timeout_is_bad:
                self.bad_results += 1
            else:
                self.corrected_json.append(site)

        return response

    def run(self):
        with open(self.json_path) as f:
            sites = json.load(f)

        with ThreadPoolExecutor(max_workers=50) as pool:
            pool.map(self.fetch_site, sites.get('base_urls'))

        logger.info('Summary')
        logger.info('Total Requests: %d' % self.total)
        logger.info('Bad Responses: %d' % self.bad_results)
        for sc in self.totals:
            logger.info('Status Code %d: %d' % (sc, self.totals[sc]))

        logger.info('JSON correction')
        self.write_corrected_json()

    def write_corrected_json(self):
        with open(self.output_path, 'w') as outfile:
            json.dump({
                'base_urls': self.corrected_json
            },
                      outfile,
                      sort_keys=True,
                      indent=4,
                      ensure_ascii=False)

    def get_corrected_json(self):
        return self.corrected_json
