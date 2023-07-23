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
        def _query_countries(limit, page, sort, order_by):
            params = {
                "limit": limit,
                "page": page,
                "sort": sort,
                "order_by": order_by,
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
        @st.cache_data(ttl=ttl)
        def _get_locations_measurements(
            country_id, limit, page, offset, sort, radius, order_by, dumpRaw
        ):
            params = {
                "limit": limit,
                "page": page,
                "offset": offset,
                "sort": sort,
                "radius": radius,
                "order_by": order_by,
                "dumpRaw": dumpRaw,
            }
            if country_id is not None:
                params["country_id"] = country_id
            with self._resource as s:
                response = s.get("https://api.openaq.org/v2/locations", params=params)
            return response.json()

        return _get_locations_measurements(
            country_id, limit, page, offset, sort, radius, order_by, dumpRaw
        )
