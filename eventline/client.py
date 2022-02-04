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

import hashlib
import json
import json.decoder
import logging
import time
from typing import Any, Dict, Optional
import urllib.parse

import OpenSSL.crypto
import urllib3

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


class Response:
    """A representation of a successful response returned by Eventline."""

    def __init__(self, response: urllib3.HTTPResponse) -> None:
        self.status = response.status
        self.header = response.headers
        self.raw_body = response.data
        self.body = self._decode_body()

    def _decode_body(self) -> Any:
        content_type = self.header.get("Content-Type")
        if content_type == "application/json":
            return self._decode_json_body()
        raise ClientError(f"unhandle content type '{content_type}'")

    def _decode_json_body(self) -> Any:
        try:
            return json.loads(self.raw_body)
        except json.decoder.JSONDecodeError as ex:
            raise ClientError(f"cannot decode response body: {ex}") from ex


class Client:
    """The low level HTTP client for the Eventline API."""

    default_endpoint = "https://api.eventline.net/v0"

    def __init__(
        self,
        /,
        endpoint: str = default_endpoint,
        timeout: float = 10.0,
        api_key: Optional[str] = None,
        project_id: Optional[str] = None,
    ) -> None:
        self.endpoint = urllib.parse.urlparse(endpoint)
        if self.endpoint.scheme.lower() != "https":
            raise ClientError("invalid non-https endpoint uri scheme")

        self.api_key = api_key
        if self.api_key is None:
            self.api_key = eventline.environment.api_key()

        self.project_id = project_id
        if self.project_id is None:
            self.project_id = eventline.environment.project_id()

        host = self.endpoint.hostname
        port = self.endpoint.port
        if port is None:
            port = 443  # we only support https

        self.pool = HTTPSConnectionPool(
            host,
            port=port,
            ca_certs=eventline.ca_bundle_path,
            timeout=timeout,
            retries=0,
        )

    def send_request(
        self, method: str, path: str, /, body: Optional[Any] = None
    ) -> Response:
        """Send a HTTP request and return the response.

        Raise an APIError exception if the status code of the response
        indicates an error.
        """
        uri = self.build_uri(path)
        try:
            headers = self._build_headers(body)
            body_data = None
            if body is not None:
                body_data = json.dumps(body)
            start = time.monotonic()
            response = self.pool.urlopen(
                method,
                uri,
                headers=headers,
                body=body_data,
            )
            end = time.monotonic()
        except Exception as ex:
            raise ClientError(ex) from ex
        status = response.status
        time_string = format_request_time(end - start)
        log.debug(f"{method} {path} {status} {time_string}")
        self._check_response(method, uri, response)
        return Response(response)

    def build_uri(self, path: str) -> str:
        """Construct the URI for an Eventline API route."""
        scheme, address, base_path, _, _, _ = self.endpoint
        full_path = base_path
        if full_path.endswith("/"):
            full_path = full_path[:-1]  # String.removesuffix is 3.9+
        full_path += path
        query = ""
        fragment = ""
        components = (scheme, address, full_path, "", query, fragment)
        return urllib.parse.urlunparse(components)

    def _build_headers(self, /, body: Optional[Any]) -> Dict[str, str]:
        """Build the set of header fields for a request."""

        headers = {}

        if self.api_key is not None:
            headers["Authorization"] = "Bearer " + self.api_key

        if self.project_id is not None:
            headers["X-Eventline-Project-Id"] = self.project_id

        if body is not None:
            headers["Content-Type"] = "application/json"

        return headers

    def _check_response(
        self, method: str, uri: str, response: urllib3.HTTPResponse
    ) -> None:
        """Check if a response indicates success or failure, and signal an
        APIError exception if it is a failure."""

        status = response.status
        if 200 <= status < 300:
            return

        message = response.reason
        code = None

        try:
            error = json.loads(response.data)
            message = error["error"]
            code = error["code"]
        except json.decoder.JSONDecodeError:
            pass
        raise APIError(
            method,
            uri,
            response.status,
            error_message=message,
            error_code=code,
        )


def format_request_time(seconds: float) -> str:
    """Format and return the time used to send a request and obtain the
    response."""
    if seconds < 0.001:
        return f"{seconds*1_000_000:.0f}μs"
    if seconds < 1.0:
        return f"{seconds*1_000:.0f}ms"
    return f"{seconds:0.1f}s"


class HTTPSConnectionPool(urllib3.HTTPSConnectionPool):
    """An urllib3 connection pool which performs public key pinning."""

    def _validate_conn(self, conn: urllib3.connection.HTTPConnection) -> None:
        # Ignore mypy error: "_validate_conn" undefined in superclass.
        # This is obviously wrong.
        super()._validate_conn(conn)  # type: ignore
        if not conn.is_verified:
            return

        cert_data = conn.sock.getpeercert(binary_form=True)
        cert = OpenSSL.crypto.load_certificate(
            OpenSSL.crypto.FILETYPE_ASN1, cert_data
        )

        key = cert.get_pubkey()
        key_data = OpenSSL.crypto.dump_publickey(
            OpenSSL.crypto.FILETYPE_ASN1, key
        )

        pin = hashlib.sha256(key_data).hexdigest()

        if pin not in eventline.public_key_pins:
            raise ClientError(
                f"invalid server certificate: unknown public key (pin {pin})"
            )
