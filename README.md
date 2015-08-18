# ADSBibTeX
[![Build Status](https://api.travis-ci.org/ryanvarley/adsbibtex.png?branch=master)](https://travis-ci.org/ryanvarley/adsbibtex)
[![Coverage Status](https://coveralls.io/repos/ryanvarley/adsbibtex/badge.svg?branch=master&service=github)](https://coveralls.io/github/ryanvarley/adsbibtex?branch=master)

Builds a bibtex file for a LaTeX document using by querying a list of bibcodes with NASA ADS

## Why?

Two main reasons

1. If you cite a preprint paper, this will automatically update the entry to the published version, when it is published
2. For really long bibtex files, its much easier to manage a list of bibcodes than bibtex entries, and you can divide
 them into sections with comments i.e.

```bash
# Transmission Spectroscopy
2008Natur.452..329S  Swain2008  # The presence of methane in the atmosphere of an extrasolar planet
2006AGUSM.A21A..06T  Tinetti2006

# Detrending Techniques
2013ApJ...766....7W  Waldmann2013
```

It is also fast, entries are cached so they are only fetched from ADS again after they are older than your ttl (time to live) setting in the config. This means you can integrate it into your latex compilation without worrying about it adding a significant overhead to your build.

## Setup and installation
You'll need the latest version of the ads module in python from [here](https://github.com/adsabs/adsabs-dev-api)

to install

```bash
git clone https://github.com/adsabs/adsabs-dev-api.git
cd adsabs-dev-api
python setup.py install
```

And you'll need an ADS API key, read the **getting started** section [here](https://github.com/adsabs/adsabs-dev-api)

Then install this package from here

```bash
git clone https://github.com/ryanvarley/adsbibtex.git
cd adsabs-dev-api
python setup.py install
```

or with

```bash
pip install adsbibtex
```

## Usage

```bash
adsbibtex <config_file>
```

config_file defaults to `config.adsbib`, see the next section for an example file

## Example config file

The config file consists of a top section of `yaml` where the config is stored and a list of bibcode citename entries
(after `---`). Comments can be entered with `#`.

All entries must have a valid bibcode, if no citename is given then the bibcode will be the citename

```bash
# YAML front matter (config)
cache_ttl:   24  # hours
cache_file:  adsbibtex_cache
bibtex_file: example.tex
---
#   Bibcode          Name          # Optional Comment
2008Natur.452..329S  Swain2008
2006AGUSM.A21A..06T                # no name needed

# You can use comments to divide papers into sections
2013ApJ...766....7W  Waldmann2013  # You could put the paper title or subject here
```