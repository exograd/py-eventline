# Copyright (c) 2022 Exograd SAS.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
# SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR
# IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""The eventline.client module contains the client for the Eventline API."""

import logging
from typing import Any, Optional
import urllib.parse

import requests


log = logging.getLogger(__name__)


class ClientError(Exception):
    """An error encountered by the client."""


class RequestError(ClientError):
    """An error signaled when a request failed."""

    def __init__(self, method: str, uri: str, status: int) -> None:
        msg = f"{method} {uri}: request failed with status {status}"
        super().__init__(msg)

        self.method = method
        self.uri = uri
        self.status = status


class Client:
    """A client for the Eventline API."""

    default_endpoint = "https://api.eventline.net/v0"

    def __init__(self, endpoint: str = default_endpoint) -> None:
        self.endpoint = endpoint
        self.endpoint_components = urllib.parse.urlparse(self.endpoint)

    def send_request(
        self, method: str, path: str, /, body: Optional[Any] = None
    ) -> requests.Response:
        """Send a HTTP request and return the response."""
        uri = self.build_uri(path)
        return requests.request(method, uri, json=body)

    def build_uri(self, path: str) -> str:
        """Construct the URI for an Eventline API route."""
        scheme, address, base_path, _, _, _ = self.endpoint_components
        full_path = base_path
        if full_path.endswith("/"):
            full_path = full_path[:-1]  # String.removesuffix is 3.9+
        full_path += path
        query = ""
        fragment = ""
        components = (scheme, address, full_path, "", query, fragment)
        return urllib.parse.urlunparse(components)
