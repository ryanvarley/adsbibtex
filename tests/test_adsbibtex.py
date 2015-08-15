import unittest

import adsbibtex


class TestParseConfigFile(unittest.TestCase):

    def test_parses_correct_file(self):
        document_list = ["# YAML front matter\n",
                         "cache_length: 24              # hours, 3d = 72, 1w=168, 2w=336\n",
                         "cache_db:     adsbibtex.cache # location to store cached entries\n",
                         "bibtex_file:  test.tex        # location to output bibtex file\n",
                         "---\n",
                         "# Bibcode Name # Comment\n",
                         "2008Natur.452..329S Swain2008   # The presence of methane in the atmosphere of an extrasolar planet\n",
                         "2006AGUSM.A21A..06T # no name\n",
                         ]

        yaml_front_matter, bibcode_lines = adsbibtex.parse_config_file(document_list)

        yaml_front_matter_answer = ''.join(document_list[:4])
        bibcode_lines_answer = document_list[5:]

        self.assertEqual(yaml_front_matter, yaml_front_matter_answer)
        self.assertItemsEqual(bibcode_lines, bibcode_lines_answer)
