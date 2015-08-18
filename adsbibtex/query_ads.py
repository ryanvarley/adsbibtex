""" queries ads using https://github.com/adsabs/adsabs-dev-api
"""

import ads

import adsbibtex_exceptions

try:  # Temp version patch for ads module
    ads.SearchQuery
except AttributeError:
    ads.SearchQuery = ads.query


def bibcode_to_bibtex(bibcode):
    """ queries ads

    :param bibcode:
    :return:
    """

    query_result = ads.SearchQuery(bibcode=bibcode, rows=1)

    papers = list(query_result)

    if len(papers) == 1:  # 0 failed, 2 is ambiguous
        try:
            return papers[0].bibtex
        except ads.exceptions.APIResponseError as e:
            raise e  # TODO (ryan) provide rate limit info

    raise adsbibtex_exceptions.ADSBibtexBibcodeNotFound