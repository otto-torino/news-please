try:
    import urllib2
except ImportError:
    import urllib.request as urllib2
import logging

import scrapy


class DirectRssCrawler(scrapy.Spider):
    name = "DirectRssCrawler"
    ignored_allowed_domains = None
    start_urls = None
    original_url = None

    log = None

    config = None
    helper = None

    def __init__(self, helper, url, config, ignore_regex, *args, **kwargs):
        self.log = logging.getLogger(__name__)

        self.config = config
        self.helper = helper

        self.original_url = url

        self.ignored_allowed_domain = self.helper.url_extractor \
            .get_allowed_domain(url)
        self.start_urls = [url]  # [self.helper.url_extractor.get_start_url(url)]

        super(DirectRssCrawler, self).__init__(*args, **kwargs)

    def parse(self, response):
        """
        Parse the Rss Feed

        :param obj response: The scrapy response
        """
        return self.rss_parse(response)

    def rss_parse(self, response):
        """
        Extracts all article links and initiates crawling them.

        :param obj response: The scrapy response
        """
        for item in response.xpath('//item'):
            for url in item.xpath('link/text()').extract():
                yield scrapy.Request(url, lambda resp: self.article_parse(
                    resp, item.xpath('title/text()').extract()[0]))

    def article_parse(self, response, rss_title=None):
        """
        Checks any given response on being an article and if positiv,
        passes the response to the pipeline.

        :param obj response: The scrapy response
        :param str rss_title: Title extracted from the rss feed
        """
        if not self.helper.parse_crawler.content_type(response):
            return

        yield self.helper.parse_crawler.pass_to_pipeline_if_article(
            response, self.ignored_allowed_domain, self.original_url,
            rss_title)

    @staticmethod
    def only_extracts_articles():
        """
        Meta-Method, so if the heuristic "crawler_contains_only_article_alikes"
        is called, the heuristic will return True on this crawler.
        """
        return True

    @staticmethod
    def supports_site(url):
        """
        Rss Crawler is supported if the url is a valid rss feed

        Determines if this crawler works on the given url.

        :param str url: The url to test
        :return bool: Determines wether this crawler work on the given url
        """

        # TODO: check if the url is a valid RSS feed
        return True
