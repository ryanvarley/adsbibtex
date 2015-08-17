import unittest

from hypothesis import given, assume
from hypothesis.strategies import text

from .. import adsbibtex


class Test_parse_config_file(unittest.TestCase):
    def test_parses_correct_file(self):
        document_list = ["# YAML front matter\n",
                         "cache_ttl: 24\n",
                         "cache_file:     adsbibtex.cache\n",
                         "bibtex_file:  test.tex",
                         "---\n",
                         "# Bibcode Name # Comment\n",
                         "2008Natur.452..329S Swain2008\n",
                         "2006AGUSM.A21A..06T # no name\n",
                         ]

        yaml_front_matter, bibcode_lines = adsbibtex.parse_config_file(document_list)

        yaml_front_matter_answer = ''.join(document_list[:4])
        bibcode_lines_answer = document_list[5:]

        self.assertEqual(yaml_front_matter, yaml_front_matter_answer)
        self.assertItemsEqual(bibcode_lines, bibcode_lines_answer)

    def test_raises_ADSBibtexConfigError_if_yaml_missing(self):
        document_list = ["cache_length: 24", "2006AGUSM.A21A..06T # no name\n"]

        with self.assertRaises(adsbibtex.ADSBibtexConfigError):
            adsbibtex.parse_config_file(document_list)

    def test_raises_ADSBibtexConfigError_if_empty(self):
        document_list = []

        with self.assertRaises(adsbibtex.ADSBibtexConfigError):
            adsbibtex.parse_config_file(document_list)


class Test_parse_bibcode_lines(unittest.TestCase):

    def test_parses_correctly(self):
        bibcode_list = ["# Bibcode Name # Comment\n",
                        "2008Natur.452..329S Swain2008",
                        "2006AGUSM.A21A..06T # no name\n",
                        "    # indented comment",
                        "    2013ApJ...766....7W",
                        "2015ExA...tmp....5V  Varley2015 # hi"  # double spaced gap
                        ]

        bibcode_list = adsbibtex.parse_bibcode_lines(bibcode_list)

        bibcode_list_answer = [{'cite_name': 'Swain2008',           'bibcode': '2008Natur.452..329S'},
                               {'cite_name': '2006AGUSM.A21A..06T', 'bibcode': '2006AGUSM.A21A..06T'},
                               {'cite_name': '2013ApJ...766....7W', 'bibcode': '2013ApJ...766....7W'},
                               {'cite_name': 'Varley2015',          'bibcode': '2015ExA...tmp....5V'},
                               ]

        self.assertEqual(bibcode_list, bibcode_list_answer)


class Test_parse_bibcode_line(unittest.TestCase):

    def test_comment_line_returns_None(self):
        bibcode_line = "# comment\n"
                        # "2008Natur.452..329S Swain2008",
                        # "2006AGUSM.A21A..06T # no name\n",
                        # "    # indented comment",
                        # "    2013ApJ...766....7W",
                        # "2015ExA...tmp....5V  Varley2015 # hi"

        result = adsbibtex.parse_bibcode_line(bibcode_line)
        self.assertTrue(result is None)

    def test_space_indented_comment_line_returns_None(self):
        bibcode_line = "    # spam\n"
        result = adsbibtex.parse_bibcode_line(bibcode_line)
        self.assertTrue(result is None)

    def test_tab_indented_comment_line_returns_None(self):
        bibcode_line = "    # eggs\n"
        result = adsbibtex.parse_bibcode_line(bibcode_line)
        self.assertTrue(result is None)

    def test_single_bibcode_works(self):
        bibcode_line = "2008Natur.452..329S\n"
        cite_name, bibcode = adsbibtex.parse_bibcode_line(bibcode_line)
        self.assertEqual(cite_name, '2008Natur.452..329S')
        self.assertEqual(bibcode, '2008Natur.452..329S')

    def test_single_bibcode_with_comment_works(self):
        bibcode_line = "2008Natur.452..329S # spam"
        cite_name, bibcode = adsbibtex.parse_bibcode_line(bibcode_line)
        self.assertEqual(cite_name, '2008Natur.452..329S')
        self.assertEqual(bibcode, '2008Natur.452..329S')

    def test_bibcode_citename_works(self):
        bibcode_line = "2008Natur.452..329S Swain2008"
        cite_name, bibcode = adsbibtex.parse_bibcode_line(bibcode_line)
        self.assertEqual(cite_name, 'Swain2008')
        self.assertEqual(bibcode, '2008Natur.452..329S')

    def test_bibcode_citename_with_comment_works(self):
        bibcode_line = "2008Natur.452..329S Swain2008 # spam"
        cite_name, bibcode = adsbibtex.parse_bibcode_line(bibcode_line)
        self.assertEqual(cite_name, 'Swain2008')
        self.assertEqual(bibcode, '2008Natur.452..329S')

    def test_bibcode_citename_double_spaced(self):
        bibcode_line = "2008Natur.452..329S  Swain2008"
        cite_name, bibcode = adsbibtex.parse_bibcode_line(bibcode_line)
        self.assertEqual(cite_name, 'Swain2008')
        self.assertEqual(bibcode, '2008Natur.452..329S')


class Test_is_comment(unittest.TestCase):
    def test_normal_comment_with_space(self):
        self.assertTrue(adsbibtex.is_comment('# spam'))

    def test_normal_comment_without_space(self):
        self.assertTrue(adsbibtex.is_comment('#spam'))

    def test_space_indented_comment(self):
        self.assertTrue(adsbibtex.is_comment(' # spam'))

    def test_space_multiple_indented_comment(self):
        self.assertTrue(adsbibtex.is_comment("    # spam\n"))

    def test_tab_indented_comment(self):
        self.assertTrue(adsbibtex.is_comment('\t# spam'))

    def test_string_with_comment_is_false(self):
        self.assertFalse(adsbibtex.is_comment('spam # eggs'))

    def test_string_with_comment_no_space_is_false(self):
        self.assertFalse(adsbibtex.is_comment('spam#eggs'))

    @given(text())
    def test_normal_string(self, s):
        assume('#' not in s)
        self.assertFalse(adsbibtex.is_comment(s))
