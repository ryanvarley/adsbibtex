#!/usr/bin/env python
""" Converts a ADSBibTeX config file to a BibTeX file

Usage:
  runbench.py [<config>]

Options:
    config    config file location
"""

import docopt
import adsbibtex


if __name__ == '__main__':

    arguments = docopt.docopt(__doc__)
    config_path = arguments['<config>']

    if config_path is None:  # use default
        config_path = 'config.adsbib'

    adsbibtex.run_adsbibtex(config_path)