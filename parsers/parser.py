from typing import List, Dict
from parsers.events_parser import XMLParser
import xml.etree.ElementTree as ET


class Parser:

    def _is_xml(self, input_string):
        try:
            # Try parsing the string as an XML document
            ET.fromstring(input_string)
            return True
        except ET.ParseError:
            # If an error occurs during parsing, it's not XML
            return False

    def parse(self, event_data: str, starts_at: str, ends_at: str) -> List[Dict]:
        if self._is_xml(event_data):
            return XMLParser().parse(event_data, starts_at, ends_at)
        else:
            raise NotImplementedError("parser not found")
