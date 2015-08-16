""" Main file
"""

import yaml
import re


def run_adsbibtex(config_file):
    config_document = load_config_file(config_file)
    yaml_front_matter, bibcode_lines = parse_config_file(config_document)

    config = parse_yaml_front_matter(yaml_front_matter)
    print yaml_front_matter, bibcode_lines


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
        raise ADSBibtexConfigError("YAML Front matter not found")

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
    """ Cleans up the bibcode line list, removing comments and returning a dict of "cite_name": {"bibcode": bibcode} pairs

    :param bibcode_lines: lists of bibcode lines
    :return:
    """

    bibcode_dict = {}

    for bibcode_line in bibcode_lines:
        try:
            cite_name, bibcode = parse_bibcode_line(bibcode_line)
            bibcode_dict[cite_name] = {'bibcode': bibcode}
        except TypeError:  # None was returned
            pass

    return bibcode_dict


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


class ADSBibtexBaseException(Exception):
    pass


class ADSBibtexConfigError(ADSBibtexBaseException):
    pass

