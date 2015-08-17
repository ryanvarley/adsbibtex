#!/usr/bin/env python
""" Converts a ADSBibTeX config file to a BibTeX file

Usage:
  adsbibtex [<config_file>]

Options:
    config    config file location
"""

import docopt
import adsbibtex


def run():
    arguments = docopt.docopt(__doc__)
    config_path = arguments['<config_file>']

    if config_path is None:  # use default
        config_path = 'config.adsbib'

    adsbibtex.run_adsbibtex(config_path)


if __name__ == '__main__':
    run()
