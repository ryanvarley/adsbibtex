""" Main file
"""


def run_adsbibtex(config_file):
    config_document = load_config_file(config_file)
    yaml_front_matter, bibcode_lines = parse_config_file(config_document)
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
    i=0
    for i, line in enumerate(config_document):
        if line.startswith('---'):
            break
        else:
            yaml_front_matter.append(line)

    if not yaml_front_matter:
        raise ADSBibtexBaseException("YAML Front matter not found")

    yaml_front_matter = ''.join(yaml_front_matter)

    bibcode_lines = config_document[i + 1:]

    return yaml_front_matter, bibcode_lines


class ADSBibtexBaseException(Exception):
    pass


class ADSBibtexConfigError(ADSBibtexBaseException):
    pass

