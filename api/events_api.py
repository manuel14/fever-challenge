import requests

from flask import Flask, request
from flask_caching import Cache
from flask_swagger_ui import get_swaggerui_blueprint

from parsers.events_parser import parse_event

SWAGGER_URL = "/api/docs"
SWAGGER_FILE_PATH = "/static/swagger.json"
API_URL = "https://provider.code-challenge.feverup.com/api/events"

app = Flask(__name__)
# Swagger Config
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, SWAGGER_FILE_PATH, config={"app_name": "Events Api"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Cache and App Config
config = {"DEBUG": True, "CACHE_TYPE": "SimpleCache",
          "CACHE_DEFAULT_TIMEOUT": 300}
app.config.from_mapping(config)
cache = Cache(app)


def _cache_key(request):
    args = str(hash(frozenset(request.args.items())))
    return request.path + args


@app.route("/events")
@cache.cached(timeout=10, query_string=True)
def events():
    """
    Endpoint that searches for events from external api

    Args:
        starts_at: str
        ends_at: str

    Returns:
        dict: containing events information   
    """
    params = {
        "starts_at": request.args.get("starts_at"),
        "ends_at": request.args.get("ends_at"),
    }
    try:
        response = requests.get(
            API_URL, params=params, timeout=30)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        cached_response = cache.get(_cache_key(request))
        if cached_response:
            return cached_response
        else:
            return []
    starts_at = request.args.get("starts_at")
    ends_at = request.args.get("ends_at")
    results = parse_event(response.content, starts_at, ends_at)

    return results
