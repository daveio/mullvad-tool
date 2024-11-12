from json import loads

from requests import get


def get_servers(url="https://api.mullvad.net/app/v1/relays"):
    resp = get(url, timeout=30).content
    return loads(resp)
