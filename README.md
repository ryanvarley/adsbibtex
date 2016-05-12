# ADSBibTeX
[![Build Status](https://api.travis-ci.org/ryanvarley/adsbibtex.png?branch=master)](https://travis-ci.org/ryanvarley/adsbibtex)
[![Coverage Status](https://coveralls.io/repos/ryanvarley/adsbibtex/badge.svg?branch=master&service=github)](https://coveralls.io/github/ryanvarley/adsbibtex?branch=master)

ADSBibTeX builds a bibtex file for a LaTeX document using by querying a list of bibcodes with NASA ADS, it was inspired by a similar script by [Alex Merson](http://www.ucl.ac.uk/star/people/amerson).

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

It is also fast after the initial run, entries are cached so they are only fetched from ADS again after they are older than your ttl (time to live) setting in the config. This means you can integrate it into your latex compilation without worrying about it adding a significant overhead to your build.

## Setup and installation

You'll need an ADS API key, the following is from the `ads` [module docs](https://github.com/andycasey/ads)

1. You'll need an API key from NASA ADS labs. Sign up for the newest version of ADS search at https://ui.adsabs.harvard.edu, visit account settings and generate a new API token. The official documentation is available at https://github.com/adsabs/adsabs-dev-api
2. When you get your API key, save it to a file called ``~/.ads/dev_key`` or save it as an environment variable named ``ADS_DEV_KEY``

Then install this package

```bash
pip install adsbibtex
```

or get the latest development version from here with

```bash
git clone https://github.com/ryanvarley/adsbibtex.git
cd adsbibtex
python setup.py install
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
cache_ttl:   168              # hours, 3d = 72, 1w=168, 2w=336
cache_file:  adsbibtex.cache  # location to store cached entries
bibtex_file: example.bib      # location to output bibtex file
---
#   Bibcode          Name          # Optional Comment
2008Natur.452..329S  Swain2008
2006AGUSM.A21A..06T                # no name needed

# You can use comments to divide papers into sections
2013ApJ...766....7W  Waldmann2013  # You could put the paper title or subject here
```

Running `adsbibtex` on this file produces the following output

```bibtex
@ARTICLE{Swain2008,
   author = {{Swain}, M.~R. and {Vasisht}, G. and {Tinetti}, G.},
    title = "{The presence of methane in the atmosphere of an extrasolar planet}",
  journal = {\nat},
     year = 2008,
    month = mar,
   volume = 452,
    pages = {329-331},
      doi = {10.1038/nature06823},
   adsurl = {http://adsabs.harvard.edu/abs/2008Natur.452..329S},
  adsnote = {Provided by the SAO/NASA Astrophysics Data System}
}

@ARTICLE{2006AGUSM.A21A..06T,
   author = {{Tinetti}, G. and {Meadows}, V.~S. and {Crisp}, D. and {Kiang}, N. and 
	{Fishbein}, E. and {Kahn}, B. and {Turnbull}, M.},
    title = "{Detectability of Surface and Atmospheric Signatures in the Disk-averaged Spectra of the Earth}",
  journal = {AGU Spring Meeting Abstracts},
 keywords = {5210 Planetary atmospheres, clouds, and hazes (0343), 5704 Atmospheres (0343, 1060), 0343 Planetary atmospheres (5210, 5405, 5704), 0406 Astrobiology and extraterrestrial materials},
     year = 2006,
    month = may,
    pages = {A6},
   adsurl = {http://adsabs.harvard.edu/abs/2006AGUSM.A21A..06T},
  adsnote = {Provided by the SAO/NASA Astrophysics Data System}
}

@ARTICLE{Waldmann2013,
   author = {{Waldmann}, I.~P. and {Tinetti}, G. and {Deroo}, P. and {Hollis}, M.~D.~J. and 
	{Yurchenko}, S.~N. and {Tennyson}, J.},
    title = "{Blind Extraction of an Exoplanetary Spectrum through Independent Component Analysis}",
  journal = {\apj},
archivePrefix = "arXiv",
   eprint = {1301.4041},
 primaryClass = "astro-ph.EP",
 keywords = {methods: data analysis, methods: observational, methods: statistical, planets and satellites: atmospheres, planets and satellites: individual: HD189733b, techniques: spectroscopic },
     year = 2013,
    month = mar,
   volume = 766,
      eid = {7},
    pages = {7},
      doi = {10.1088/0004-637X/766/1/7},
   adsurl = {http://adsabs.harvard.edu/abs/2013ApJ...766....7W},
  adsnote = {Provided by the SAO/NASA Astrophysics Data System}
}
```
