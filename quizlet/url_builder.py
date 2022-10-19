from logging import warn
import urllib.parse as urlparse
from urllib.parse import urlencode

from logging import warn

from typing import Union


class URLBuilder:
    @staticmethod
    def cardset_page(
        id: int, per_page: int, page: int, paging_token: Union[str, None] = None
    ) -> str:
        assert isinstance(id, int), "id must be an integer"
        assert isinstance(per_page, int), "per_page must be an integer"
        assert isinstance(page, int), "page must be an integer"

        if paging_token is not None:
            assert isinstance(
                paging_token, str
            ), "paging_token must be a string if provided"

        if page > 1 and paging_token is None:
            warn(
                "Page number is greater than 1 yet no paging token is provided. This may cause a 400 error."
            )

        url = "https://quizlet.com/webapi/3.4/studiable-item-documents?filters[studiableContainerType]=1"
        url_fragments = list(urlparse.urlparse(url))

        query = dict(urlparse.parse_qsl(url_fragments[4]))

        params = {
            "filters[studiableContainerId]": str(id),
            "perPage": str(per_page),
            "page": str(page),
        }

        if paging_token is not None:
            params["pagingToken"] = paging_token

        query.update(params)
        url_fragments[4] = urlencode(query)

        return urlparse.urlunparse(url_fragments)
