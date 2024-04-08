import requests
from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from parsers.parser import Parser

API_URL = "https://provider.code-challenge.feverup.com/api/events"

app = FastAPI()

# Cache for events
event_cache = {}


def update_event_cache():
    print("update going on")
    try:
        response = requests.get(API_URL, timeout=30)
        response.raise_for_status()
        starts_at = response.headers.get("starts_at")
        ends_at = response.headers.get("ends_at")
        parser = Parser()
        events_parsed = parser.parse(
            response.content, starts_at, ends_at)
        event_cache.clear()
        event_cache.update(events_parsed)
    except requests.exceptions.RequestException as e:
        print(f"Error updating event cache: {str(e)}")


@app.get("/events")
async def events(starts_at: str = None, ends_at: str = None):
    if event_cache:
        print("using cache")
        return event_cache
    else:
        try:
            response = requests.get(API_URL, timeout=30)
            response.raise_for_status()
            parser = Parser()
            parsed_events = parser.parse(response.content, starts_at, ends_at)
            return parsed_events
        except requests.exceptions.RequestException as e:
            print(str(e))
            return {
                "data": {
                    "events": []
                },
                "error": "Failed to fetch events"
            }


# Schedule the periodic task to update event cache every minute
scheduler = AsyncIOScheduler()
scheduler.add_job(update_event_cache, "interval", minutes=1)
scheduler.start()

#  2021-02-01T21:00:00
#  2022-07-03T21:00:00
