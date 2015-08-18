""" Main file
"""

import yaml
import re

import query_ads
import adsbibtex_cache
import adsbibtex_exceptions


def run_adsbibtex(config_file):
    config_document = load_config_file(config_file)
    yaml_front_matter, bibcode_lines = parse_config_file(config_document)

    config = parse_yaml_front_matter(yaml_front_matter)

    bibcode_list = parse_bibcode_lines(bibcode_lines)

    cache = adsbibtex_cache.load_cache(config['cache_file'])
    cache_ttl = config['cache_ttl'] * 3600  # to seconds

    for i, bibcode_entry in enumerate(bibcode_list):
        bibcode = bibcode_entry['bibcode']
        try:
            bibtex = adsbibtex_cache.read_key(cache, bibcode, cache_ttl)
            print '{} successfully fetched from cache'.format(bibcode)
        except KeyError:  # bibcode not cached or old
            try:
                bibtex = query_ads.bibcode_to_bibtex(bibcode)
                adsbibtex_cache.save_key(cache, bibcode, bibtex)
                print '{} successfully fetched from ADS'.format(bibcode)
            except adsbibtex_exceptions.ADSBibtexBibcodeNotFound:
                print '{} not found on ADS, skipping'.format(bibcode)
                continue

        bibcode_entry['bibtex'] = bibtex

    cache.close()

    bibtex_ouput = generate_bibtex_output(bibcode_list)

    save_bibtex_output(bibtex_ouput, out_path=config['bibtex_file'])


def load_config_file(config_file):
    """ Loads the given file into a list of lines

    :param config_file: file name of the config file
    :type config_file: str

    :return: config file as a list (one item per line) as returned by open().readlines()
    """
    with open(config_file, 'r') as f:
        config_document = f.readlines()
    return config_document


def parse_config_file(config_document):
    """ Parses the config file into a yaml front matter and a list of bibcode lines

    :param config_file: config file as a list (one item per line) as returned by open().readlines()
    :type config_file: [str, str, ...]

    :return: yaml_front_matter, bibcode_lines
    :rtype: str, list
    """

    yaml_front_matter = []
    i = 0
    yaml_front_matter_found = False
    for i, line in enumerate(config_document):
        if line.startswith('---'):
            yaml_front_matter_found = True
            break
        else:
            yaml_front_matter.append(line)

    if not yaml_front_matter_found:
        raise adsbibtex_exceptions.ADSBibtexConfigError("YAML Front matter not found")

    yaml_front_matter = ''.join(yaml_front_matter)

    bibcode_lines = config_document[i + 1:]

    return yaml_front_matter, bibcode_lines


def parse_yaml_front_matter(yaml_front_matter):
    """ Parses the YAML front matter and checks for essential config params

    :param yaml_front_matter:
    :return: config
    :rtype: dict
    """

    config = yaml.load(yaml_front_matter)

    # TODO check essential config params / set defaults

    return config


def parse_bibcode_lines(bibcode_lines):
    """ Cleans up the bibcode line list, removing comments and returning a list of
    {"cite_name": cite_name, "bibcode": bibcode} pairs

    :param bibcode_lines: lists of bibcode lines
    :return:
    """

    bibcode_list = []

    for bibcode_line in bibcode_lines:
        try:
            cite_name, bibcode = parse_bibcode_line(bibcode_line)
            bibcode_list.append({'cite_name': cite_name, 'bibcode': bibcode})
        except TypeError:  # None was returned
            pass

    return bibcode_list


def parse_bibcode_line(bibcode_line):
    """ Parses a single bibcode line into cite_name, bibcode

    :param bibcode_line: a line containing bibcode [cite_name] [# comment]
    :return: cite_name, bibcode
    """
    # TODO (ryan) think about replacing with regex
    if not is_comment(bibcode_line):  # line is just a comment
        bibcode_line = bibcode_line.replace('\t', ' ')
        bibcode_line = bibcode_line.replace('\n', '')
        bibcode_line = ' '.join(bibcode_line.split())
        # replace multiple whitespace with single space

        bibcode_split = bibcode_line.split(' ', 2)
        num_splits = len(bibcode_split)
        if num_splits == 1:
            bibcode = cite_name = bibcode_split[0]
        elif num_splits > 1:
            bibcode, cite_name = bibcode_split[:2]
            if is_comment(cite_name):
                cite_name = bibcode
        else:
            return None

        if bibcode and cite_name:
            return cite_name, bibcode
        else:
            return None
    else:
        return None


def is_comment(s):
    """ Checks if a string looks like a comment line (first non whitespace char is #)
    :param s: string to check
    :return: True/False
    """
    if re.match(r'(\s+|)#(.*?)', s):
        return True
    else:
        return False


def replace_bibtex_cite_name(bibtex, current_name, new_name):
    """replaces the cite_name in a bibtex file with something else

    :param: string of bibtex to do the replacing on
    :param current_name: current cite name in the bibtex
    :param new_name: name to replace it with
    """

    new_bibtex = bibtex.replace(current_name, new_name, 1)

    return new_bibtex


def generate_bibtex_output(bibcode_list):
        output = []
        for bibcode_item in bibcode_list:
            try:
                bibtex = bibcode_item['bibtex']
            except KeyError:  # Bibcode not found
                continue

            bibcode = bibcode_item['bibcode']
            cite_name = bibcode_item['cite_name']
            new_bibtex = replace_bibtex_cite_name(bibtex, bibcode, cite_name)

            output.append(new_bibtex)

        return ''.join(output)


def save_bibtex_output(bibtex_output, out_path):
    with open(out_path, 'w') as f:
        f.write(bibtex_output)
