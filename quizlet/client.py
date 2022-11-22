try:
    from url_builder import URLBuilder
except ImportError:
    from quizlet.url_builder import URLBuilder

import random
import urllib.parse as urlparse
from datetime import datetime
from json.decoder import JSONDecodeError
from logging import warn
from typing import Union
from urllib.parse import urlencode

import requests


class APIException(Exception):
    pass


USER_AGENTS = [  # a list of real user agents to allow the API to work. thanks to DavidWittman/requests-random-user-agent
    "Mozilla/5.0 (Linux; U; Android 8.0.0; zh-cn; Mi Note 2 Build/OPR1.170623.032) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.128 Mobile Safari/537.36 XiaoMi/MiuiBrowser/10.1.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:103.0) Gecko/20100101 Firefox/103.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:104.0) Gecko/20100101 Firefox/104.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.101 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.167 YaBrowser/22.7.4.960 Yowser/2.5 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 OPR/89.0.4447.83",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.63",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.70",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.54",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.47",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Windows NT 10.0; rv:103.0) Gecko/20100101 Firefox/103.0",
    "Mozilla/5.0 (Windows NT 10.0; rv:104.0) Gecko/20100101 Firefox/104.0",
    "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) QtWebEngine/5.15.5 Chrome/87.0.4280.144 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0",
]


"""Selects a random user agent from the list

Returns:
    str: A random user agent
"""


def random_user_agent() -> str:
    return random.choice(USER_AGENTS)


"""Generic get method without any headers

Parameters:
    url (str): The url to get
    qlts_token (optional str): The qlts token extracted from the Quizlet cookie. Used to access private sets.
    raise_error_identifiers (optional bool): raise the computer readable error identifier instead of the human readable error message. Defaults to False.

Returns:
    dict: The response
"""


def generic_get(
    url: str, qlts_token: Union[str, None], raise_error_identifiers=False
) -> dict:
    if not isinstance(url, str):
        raise AssertionError("url must be a string")

    headers = {"User-Agent": random_user_agent()}

    if qlts_token:
        headers["Cookie"] = f"qlts={qlts_token}"

    res = requests.get(url, headers=headers)

    try:
        json_res = res.json()
    except JSONDecodeError:
        raise APIException("Invalid JSON received from API")

    if res.status_code == 200:
        return json_res
    else:
        try:
            if raise_error_identifiers:
                raise APIException(json_res["error"]["identifier"])
            else:
                raise APIException(json_res["error"]["message"])
        except KeyError:
            raise APIException(
                "Request failed with status code " + str(res.status_code)
            )


class Card:
    def __init__(
        self,
        id: int,
        studiableContainerType: Union[int, None],
        studiableContainerId: int,
        rank: int,
        creatorId: int,
        timestamp: int,
        lastModified: int,
        isDeleted: bool,
        cardSides: list,
    ) -> None:
        self.id = id
        self.studiableContainerType = studiableContainerType
        self.studiableContainerId = studiableContainerId
        self.rank = rank
        self.creatorId = creatorId
        self.timestamp = timestamp
        self.lastModified = lastModified
        self.isDeleted = isDeleted
        self.cardSides = cardSides

    def __str__(self) -> str:
        return f"Card(id={self.id}, studiableContainerType={self.studiableContainerType}, studiableContainerId={self.studiableContainerId}, rank={self.rank}, creatorId={self.creatorId}, timestamp={self.timestamp}, lastModified={self.lastModified}, isDeleted={self.isDeleted}, cardSides={self.cardSides})"

    def get_id(self) -> int:
        return self.id

    def get_set_id(self) -> int:
        return self.studiableContainerId

    def get_rank(self) -> int:
        return self.rank

    def get_creator_id(self) -> int:
        return self.creatorId

    def get_timestamp(self) -> int:
        return self.timestamp

    def get_utc_time(self) -> datetime:
        return datetime.utcfromtimestamp(self.timestamp)

    def get_last_modified(self) -> int:
        return self.lastModified

    def is_deleted(self) -> bool:
        return self.isDeleted

    def get_side(self, side: int) -> str:
        return self.cardSides[side]


class CardSide:
    def __init__(self, sideId: int, label: str, media: list, distractors: list):
        self.sideId = sideId
        self.label = label
        self.media = media
        self.distractors = distractors

    def __str__(self) -> str:
        return f"CardSide(sideId={self.sideId}, label={self.label}, media={self.media}, distractors={self.distractors})"

    def get_side_id(self) -> int:
        return self.sideId

    def get_label(self) -> str:
        return self.label

    def get_media(self) -> list:
        return self.media


class TextMedia:
    def __init__(
        self,
        plainText: str,
        languageCode: str,
        ttsUrl: str,
        ttsSlowUrl: str,
        richText: Union[str, None],
    ) -> None:
        self.plainText = plainText
        self.languageCode = languageCode
        self.ttsUrl = ttsUrl
        self.ttsSlowUrl = ttsSlowUrl
        self.richText = richText

    def __str__(self) -> str:
        return f"TextMedia(plainText={self.plainText}, languageCode={self.languageCode}, ttsUrl={self.ttsUrl}, ttsSlowUrl={self.ttsSlowUrl}, richText={self.richText})"

    def get_plain_text(self) -> str:
        return self.plainText

    def get_language_code(self) -> str:
        return self.languageCode

    def get_tts_url(self, absolute=False, slow=False) -> str:
        url = self.ttsUrl

        if slow:
            url = self.ttsSlowUrl

        if absolute:
            if not url.startswith("/"):
                raise APIException("TTS URL is not relative, unsafe to make absolute")

            return urlparse.urljoin("https://quizlet.com", url)

        return url

    def get_tts_url_at_speed(self, speed: int, absolute=False) -> str:
        url = self.ttsUrl
        url_fragments = list(urlparse.urlparse(url))

        query = dict(urlparse.parse_qsl(url_fragments[4]))

        params = {
            "speed": str(speed),
        }

        query.update(params)
        url_fragments[4] = urlencode(query)

        url = urlparse.urlunparse(url_fragments)

        if absolute:
            if not url.startswith("/"):
                raise APIException("TTS URL is not relative, unsafe to make absolute")

            return urlparse.urljoin("https://quizlet.com", url)

        return url

    def get_rich_text(self) -> Union[str, None]:
        return self.richText


class ImageMedia:
    def __init__(self, code: str, url: str, width: int, height: int) -> None:
        self.code = code
        self.url = url
        self.width = width
        self.height = height

    def __str__(self) -> str:
        return f"ImageMedia(code={self.code}, url={self.url}, width={self.width}, height={self.height})"

    def get_code(self) -> str:
        return self.code

    def get_url(self) -> str:
        return self.url

    def get_width(self) -> int:
        return self.width

    def get_height(self) -> int:
        return self.height


class QuizletAPIClient:
    def __init__(self, qlts_token=None):
        if not (not qlts_token or isinstance(qlts_token, str)):
            raise AssertionError("qlts_token must be a string if provided")

        self.qlts_token = qlts_token

    def set_qlts_token(self, qlts_token):
        if not isinstance(qlts_token, str):
            raise AssertionError("qlts_token must be a string")
        self.qlts_token = qlts_token

    def cardset_page(
        self,
        id: int,
        per_page: int,
        page: int,
        paging_token: Union[str, None] = None,
        raise_error_identifiers=False,
    ) -> dict:
        try:
            return generic_get(
                URLBuilder.cardset_page(id, per_page, page, paging_token),
                qlts_token=self.qlts_token,
                raise_error_identifiers=raise_error_identifiers,
            )
        except APIException as e:
            raise (e)

    def cardset_page_range(
        self, id: int, per_page: int, page_range: range, raise_error_identifers=False
    ) -> list:
        if not isinstance(id, int):
            raise AssertionError("id must be an integer")
        if not isinstance(per_page, int):
            raise AssertionError("per_page must be an integer")
        if not isinstance(page_range, range):
            raise AssertionError("page_range must be a range")

        if page_range.start < 1:
            raise ValueError("Page range must start at 1 or greater")

        if page_range.step < 1:
            raise ValueError("Page range must have a step of 1 or greater")

        if page_range.stop < page_range.start:
            raise ValueError(
                "Page range must have a stop value greater than or equal to the start value"
            )

        if (
            page_range.start != int(page_range.start)
            or page_range.stop != int(page_range.stop)
            or page_range.step != int(page_range.step)
        ):
            raise ValueError("Page range values must be integers")

        results = []
        paging_token = None

        for i in page_range:
            current = self.cardset_page(
                id, per_page, i, paging_token, raise_error_identifers
            )
            results.append(current)

            paging_token = current["responses"][0]["paging"]["token"]

        return results

    def cardset_full(self, id: int, raise_error_identifiers=False) -> dict:
        if not isinstance(id, int):
            raise AssertionError("id must be an integer")

        try:
            return generic_get(
                URLBuilder.cardset_full(id),
                qlts_token=self.qlts_token,
                raise_error_identifiers=raise_error_identifiers,
            )
        except APIException as e:
            raise (e)

    @staticmethod
    def parse_card(card_data: dict) -> Union[Card, None]:
        if not isinstance(card_data, dict):
            raise AssertionError("card_data must be a dictionary")

        if not ("isDeleted" in card_data and isinstance(card_data["isDeleted"], bool)):
            raise AssertionError(
                "card_data must contain a isDeleted and it must be a boolean"
            )

        if card_data["isDeleted"]:
            warn("Card is deleted, skipping (could be a private set)")
            return None

        if not ("id" in card_data and isinstance(card_data["id"], int)):
            raise AssertionError(
                "card_data must contain an id and it must be an integer"
            )
        if not "studiableContainerType" in card_data:
            warn("card_data does not contain a studiableContainerType")
        if not (
            "studiableContainerId" in card_data
            and isinstance(card_data["studiableContainerId"], int)
        ):
            raise AssertionError(
                "card_data must contain a studiableContainerId and it must be an integer"
            )
        if not ("rank" in card_data and isinstance(card_data["rank"], int)):
            raise AssertionError(
                "card_data must contain a rank and it must be an integer"
            )
        if not ("creatorId" in card_data and isinstance(card_data["creatorId"], int)):
            raise AssertionError(
                "card_data must contain a creatorId and it must be an integer"
            )
        if not ("timestamp" in card_data and isinstance(card_data["timestamp"], int)):
            raise AssertionError(
                "card_data must contain a timestamp and it must be an integer"
            )
        if not (
            "lastModified" in card_data and isinstance(card_data["lastModified"], int)
        ):
            raise AssertionError(
                "card_data must contain a lastModified and it must be an integer"
            )
        if not ("cardSides" in card_data and isinstance(card_data["cardSides"], list)):
            raise AssertionError(
                "card_data must contain a cardSides and it must be a list"
            )

        effective_card_sides = []

        for i, side in enumerate(card_data["cardSides"]):
            if not ("sideId" in side and isinstance(side["sideId"], int)):
                raise AssertionError(
                    f"cardSides[{i}] must contain a sideId and it must be an integer"
                )
            if not ("label" in side and isinstance(side["label"], str)):
                raise AssertionError(
                    f"cardSides[{i}] must contain a label and it must be a string"
                )
            if not ("media" in side and isinstance(side["media"], list)):
                raise AssertionError(
                    f"cardSides[{i}] must contain a media and it must be a list"
                )
            if not ("distractors" in side and isinstance(side["distractors"], list)):
                raise AssertionError(
                    f"cardSides[{i}] must contain a distractors and it must be a list"
                )

            effective_media = []

            for j, media in enumerate(side["media"]):
                if not ("type" in media and isinstance(media["type"], int)):
                    raise AssertionError(
                        f"cardSides[{i}].media[{j}] must contain a type and it must be an integer"
                    )

                media_type = media["type"]

                if media_type == 1:  # text
                    if not (
                        "plainText" in media and isinstance(media["plainText"], str)
                    ):
                        raise AssertionError(
                            f"cardSides[{i}].media[{j}] must contain plainText and it must be a string"
                        )
                    if not (
                        "languageCode" in media
                        and isinstance(media["languageCode"], str)
                    ):
                        raise AssertionError(
                            f"cardSides[{i}].media[{j}] must contain languageCode and it must be a string"
                        )
                    if not ("ttsUrl" in media and isinstance(media["ttsUrl"], str)):
                        raise AssertionError(
                            f"cardSides[{i}].media[{j}] must contain ttsUrl and it must be a string"
                        )
                    if not (
                        "ttsSlowUrl" in media and isinstance(media["ttsSlowUrl"], str)
                    ):
                        raise AssertionError(
                            f"cardSides[{i}].media[{j}] must contain ttsSlowUrl and it must be a string"
                        )
                    if not (
                        "richText" in media
                        and (
                            media["richText"] is None
                            or isinstance(media["richText"], str)
                        )
                    ):
                        raise AssertionError(
                            f"cardSides[{i}].media[{j}] must contain richText and it must be a string or None (null)"
                        )

                    effective_media.append(
                        TextMedia(
                            media["plainText"],
                            media["languageCode"],
                            media["ttsUrl"],
                            media["ttsSlowUrl"],
                            media["richText"],
                        )
                    )
                elif media_type == 2:  # image
                    if not ("code" in media and isinstance(media["code"], str)):
                        raise AssertionError(
                            f"cardSides[{i}].media[{j}] must contain code and it must be a string"
                        )
                    if not ("url" in media and isinstance(media["url"], str)):
                        raise AssertionError(
                            f"cardSides[{i}].media[{j}] must contain url and it must be a string"
                        )
                    if not ("width" in media and isinstance(media["width"], int)):
                        raise AssertionError(
                            f"cardSides[{i}].media[{j}] must contain width and it must be an integer"
                        )
                    if not ("height" in media and isinstance(media["height"], int)):
                        raise AssertionError(
                            f"cardSides[{i}].media[{j}] must contain height and it must be an integer"
                        )

                    effective_media.append(
                        ImageMedia(
                            media["code"],
                            media["url"],
                            media["width"],
                            media["height"],
                        )
                    )
                elif media_type == 3:  # audio
                    raise NotImplementedError("Audio media is not yet supported")
                else:
                    raise ValueError(f"Unknown media type: {media_type}")

            effective_card_sides.append(
                CardSide(
                    **{
                        "sideId": side["sideId"],
                        "label": side["label"],
                        "media": effective_media,
                        "distractors": [],
                    }
                )
            )

        return Card(
            id=card_data["id"],
            studiableContainerType=card_data["studiableContainerType"],
            studiableContainerId=card_data["studiableContainerId"],
            rank=card_data["rank"],
            creatorId=card_data["creatorId"],
            timestamp=card_data["timestamp"],
            lastModified=card_data["lastModified"],
            isDeleted=card_data["isDeleted"],
            cardSides=sorted(effective_card_sides, key=lambda x: x.sideId),
        )

    def get_parsed_cardset(self, id: int, raise_error_identifiers=False):
        res = self.cardset_full(id, raise_error_identifiers)
        cards = res["responses"][0]["models"]["studiableItem"]

        parsed = []

        for i, card in enumerate(cards):
            parse_res = QuizletAPIClient.parse_card(card)
            if parse_res:
                parsed.append(parse_res)

        return sorted(parsed, key=lambda x: x.get_rank())
