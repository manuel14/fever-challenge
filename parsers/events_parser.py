from datetime import datetime
import xml.etree.ElementTree as ET
from typing import List, Dict


class XMLParser():
    def parse(self, event_data: str, starts_at: str, ends_at: str) -> List[Dict]:
        xml_tree = ET.fromstring(event_data)
        try:
            starts_at_dt = datetime.now()
            # using a very old datetime as a fallback
            starts_at_dt = starts_at_dt.replace(year=1900)
            if starts_at is not None:
                starts_at_dt = datetime.strptime(
                    starts_at, "%Y-%m-%dT%H:%M:%S")
            ends_at_dt = datetime.now()
            # using a very high datetime for ends at
            ends_at_dt = ends_at_dt.replace(year=3000)
            if ends_at is not None:
                ends_at_dt = datetime.strptime(ends_at, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            error_message = {"error": "Bad request"}
            return [error_message]

        output_elements = xml_tree.find("output")
        results = {"data": {"events": []}, "error": None}
        # using a gen expression not load all events in memory
        base_events = (e for e in output_elements.findall("base_event"))
        for base_event in base_events:
            online_events = (e for e in base_event.findall(
                "event") if base_event.get("sell_mode") == "online")
            for event in online_events:
                event_date = datetime.strptime(
                    event.get("event_start_date"), "%Y-%m-%dT%H:%M:%S")
                if starts_at_dt <= event_date <= ends_at_dt:
                    results["data"]["events"].append(
                        XMLParser._convert_event_to_json(base_event, event))
        return results

    @staticmethod
    def _convert_event_to_json(base_event, event) -> Dict:
        event_json = {
            "title": base_event.get("title"),
            "start_date": event.get("event_start_date"),
            "end_date": event.get("event_end_date"),
            "event_id": event.get("event_id"),
            "sell_from": event.get("sell_from"),
            "sell_to": event.get("sell_to"),
            "sold_out": event.get("sold_out"),
            "zones": []
        }
        for zone in event.findall("zone"):
            event_json["zones"].append({
                "id": zone.get("zone_id"),
                "capacity": zone.get("capacity"),
                "price": zone.get("price"),
                "name": zone.get("name"),
                "numbered": zone.get("numbered")
            })
        return event_json
