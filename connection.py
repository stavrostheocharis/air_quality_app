from streamlit.connections import ExperimentalBaseConnection
import requests
import streamlit as st


class OpenAQConnection(ExperimentalBaseConnection[requests.Session]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._resource = self._connect(**kwargs)

    def _connect(self, **kwargs) -> requests.Session:
        session = requests.Session()

        return session

    def cursor(self):
        return self._resource

    def query_countries(
        self, limit=100, page=1, sort="asc", order_by="name", ttl: int = 3600
    ):
        @st.cache_data(ttl=ttl)
        def _query_countries(_limit, _page, _sort, _order_by):
            params = {
                "limit": _limit,
                "page": _page,
                "sort": _sort,
                "order_by": _order_by,
            }
            with self._resource as s:
                response = s.get("https://api.openaq.org/v2/countries", params=params)
            return response.json()

        return _query_countries(limit, page, sort, order_by)

    def query(
        self,
        country_id,
        limit=1000,
        page=1,
        offset=0,
        sort="desc",
        radius=1000,
        order_by="lastUpdated",
        dumpRaw="false",
        ttl: int = 3600,
    ):
        # @st.cache_data(ttl=ttl)
        def _get_locations_measurements(
            _country_id, _limit, _page, _offset, _sort, _radius, _order_by, _dumpRaw
        ):
            params = {
                "limit": _limit,
                "page": _page,
                "offset": _offset,
                "sort": _sort,
                "radius": _radius,
                "order_by": _order_by,
                "dumpRaw": _dumpRaw,
            }
            if _country_id is not None:
                params["country_id"] = _country_id
            with self._resource as s:
                response = s.get("https://api.openaq.org/v2/locations", params=params)
            return response.json()

        return _get_locations_measurements(
            country_id, limit, page, offset, sort, radius, order_by, dumpRaw
        )
