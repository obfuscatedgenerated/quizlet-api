import urllib.parse as urlparse
from logging import warn
from typing import Union
from urllib.parse import urlencode


class URLBuilder:
    """Builds a URL for a single page of a Quizlet set.

    Parameters:
        id (int): The ID of the set to build a URL for.
        per_page (int): The results per page.
        page (int): The page number to build a URL for.
        paging_token (optional str): The paging token to use pages after the first.

    Returns:
        str: The URL for the page of the set.
    """

    @staticmethod
    def cardset_page(
        id: int, per_page: int, page: int, paging_token: Union[str, None] = None
    ) -> str:
        if not isinstance(id, int):
            raise TypeError("id must be an integer")
        if not isinstance(per_page, int):
            raise TypeError("per_page must be an integer")
        if not isinstance(page, int):
            raise TypeError("page must be an integer")

        if (
            paging_token is not None
            and not isinstance(paging_token, str)
        ):
            raise TypeError("paging_token must be a string if provided")

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

    """Builds a URL for a full Quizlet set.

    Parameters:
        id (int): The ID of the set to build a URL for.

    Returns:
        str: The URL for the set.
    """

    @staticmethod
    def cardset_full(id: int) -> str:
        if not isinstance(id, int):
            raise TypeError("id must be an integer")

        url = "https://quizlet.com/webapi/3.4/studiable-item-documents?filters[studiableContainerType]=1"
        url_fragments = list(urlparse.urlparse(url))

        query = dict(urlparse.parse_qsl(url_fragments[4]))

        params = {
            "filters[studiableContainerId]": str(id),
        }

        query.update(params)
        url_fragments[4] = urlencode(query)

        return urlparse.urlunparse(url_fragments)
