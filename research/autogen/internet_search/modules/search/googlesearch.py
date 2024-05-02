from requests import Session
from typing import Any, List

from .exception import ApiNotEnabledException


from dataclasses import dataclass

@dataclass
class Item:
    """This is return a item."""

    def __init__(self, data: dict):
        self.data: dict = data

    @property
    def kind(self) -> str:
        "This is the kind of the item."
        return self.data["kind"]

    @property
    def title(self) -> str:
        "This is the title of the item."
        return self.data["title"]

    @property
    def url(self) -> str:
        "This is the url of the item."
        return self.data["link"]

    @property
    def display_url(self) -> str:
        "This is the display url of the item."
        return self.data["displayLink"]

    @property
    def html_title(self) -> str:
        "This is the html title of the item."
        return self.data["htmlTitle"]

    @property
    def snippet(self) -> str:
        "This is the snippet of the item."
        return self.data["snippet"]


class CustomSearch():
    """Customsearch google.

    Args:
        apikey (str): Insert google custom search api key.
        engine_id (str): Insert google custom search engine id.

    Attributes:
        APIURL (str): Google Custom Search API URL
    """

    APIURL = "https://www.googleapis.com/customsearch/v1"
    session: Any = None

    def __init__(self, apikey: str, engine_id: str):
        self.apikey = apikey
        self.engine_id = engine_id
        self.__session = Session()

    def request(self, method: str, path: str, *args, **kwargs) -> dict:

        return self.__session.request(
            method, self.APIURL + path, *args, **kwargs
        ).json()

    def search(self, *args, **kwargs) -> List[Item]:
        return self._from_dict(
            self.request(
                "GET", "/", params=self._payload_maker(*args, **kwargs)
            )
        )

    def _from_dict(self, data: dict) -> List[Item]:
        if data.get('error'):
            raise ApiNotEnabledException(
                data['error']['code'], data['error']['message'])
        else:
            return [Item(i) for i in data["items"]]

    def _payload_maker(
        self, query: str, *,
        safe: bool = False,
        filter_: bool = False
    ) -> dict:
        payload = {
            "key": self.apikey,
            "cx": self.engine_id,
            "q": query
        }
        if safe:
            payload["safe"] = "active"
        if not filter_:
            payload["filter"] = 0
        return payload


