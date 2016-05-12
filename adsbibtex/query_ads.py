""" queries ads using https://github.com/adsabs/adsabs-dev-api
"""

import ads.exceptions
from ads.export import ExportQuery


def bibcode_to_bibtex(bibcode):
    """Queries ads for the bibtex"""

    try:
        bibtex = ExportQuery(bibcodes=bibcode, format="bibtex").execute()
        return bibtex
    except ads.exceptions.APIResponseError as e:
        raise e  # TODO (ryan) provide rate limit info