import unittest
import pytest
from datetime import datetime
from xml.etree.ElementTree import ParseError
from unittest.mock import patch
from unittest.mock import MagicMock

from parsers.parser import Parser
from tests.mocked_responses import MOCKED_RESPONSE


class TestXMLParser(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_parse_xml_success(self):
        result = self.parser.parse(MOCKED_RESPONSE, None, None)
        self.assertEqual(len(result['data']['events']), 3)

    @patch('xml.etree.ElementTree.fromstring')
    def test_parse_non_xml_failure(self, mock_fromstring):
        mock_fromstring.side_effect = ParseError()
        with pytest.raises(NotImplementedError):
            self.parser.parse("This is not XML", None, None)


if __name__ == '__main__':
    unittest.main()
