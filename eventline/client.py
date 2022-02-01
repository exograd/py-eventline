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

import json.decoder
import logging
from typing import Any, Optional
import urllib.parse

import requests

import eventline.environment

log = logging.getLogger(__name__)


class ClientError(Exception):
    """An error encountered by the client."""


class APIError(ClientError):
    """An error signaled when a request failed due to an API error."""

    def __init__(
        self,
        method: str,
        uri: str,
        status: int,
        /,
        error_message: Optional[str],
        error_code: Optional[str],
    ) -> None:
        message = f"{method} {uri}: request failed with status {status}"
        if error_message is not None:
            message += f": {error_message}"

        super().__init__(message)

        self.method = method
        self.uri = uri
        self.status = status
        self.error_code = error_code
        self.error_message = error_message


class Client:
    """A client for the Eventline API."""

    default_endpoint = "https://api.eventline.net/v0"

    def __init__(
        self,
        /,
        endpoint: str = default_endpoint,
        timeout: float = 10.0,
        api_key: Optional[str] = None,
    ) -> None:
        self.endpoint = endpoint
        self.endpoint_components = urllib.parse.urlparse(self.endpoint)
        self.timeout = timeout
        self.api_key = api_key
        if self.api_key is None:
            self.api_key = eventline.environment.api_key()

    def send_request(
        self,
        method: str,
        path: str,
        /,
        body: Optional[Any] = None,
        project_id: Optional[str] = None,
    ) -> requests.Response:
        """Send a HTTP request and return the response.

        Raise an APIError exception if the status code of the response
        indicates an error.
        """
        uri = self.build_uri(path)
        headers = {}
        if self.api_key is not None:
            headers["Authorization"] = f"Bearer {self.api_key}"
        if project_id is None:
            project_id = eventline.environment.project_id()
        if project_id is not None:
            headers["X-Eventline-Project-Id"] = project_id
        try:
            response = requests.request(
                method, uri, headers=headers, json=body, timeout=self.timeout
            )
        except Exception as ex:
            raise ClientError(ex) from ex
        if not (response.status_code >= 200 and response.status_code < 300):
            message = response.reason
            code = None
            try:
                error = response.json()
                message = error["error"]
                code = error["code"]
            except json.decoder.JSONDecodeError:
                pass
            raise APIError(
                method,
                uri,
                response.status_code,
                error_message=message,
                error_code=code,
            )
        return response

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
